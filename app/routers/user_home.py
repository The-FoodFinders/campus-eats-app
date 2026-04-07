from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import status, Form, Query
from sqlmodel import select
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.review import Review
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, OptionalUser
from app.utilities.flash import flash
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: OptionalUser,
    db: SessionDep,
    search: str = Query(None),
    category: str = Query(None)
):
    query = select(Restaurant)

    if search:
        query = query.where(Restaurant.name.ilike(f"%{search}%"))

    if category:
        query = query.where(Restaurant.category == category)

    restaurants = db.exec(query).all()

    all_restaurants = db.exec(select(Restaurant)).all()
    categories = sorted(set(r.category for r in all_restaurants if r.category))

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "restaurants": restaurants,
            "categories": categories,
            "selected_category": category,
        }
    )

@router.get("/search-restaurants")
async def search_restaurants(
    db: SessionDep,
    search: str = ""
):
    query = select(Restaurant)

    if search:
        query = query.where(Restaurant.name.ilike(f"%{search}%"))

    restaurants = db.exec(query).all()

    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "location": r.location
        }
        for r in restaurants
    ]


@router.get("/restaurant/{restaurant_id}", response_class=HTMLResponse)
async def restaurant_menu(
    request: Request,
    restaurant_id: int,
    user: OptionalUser,
    db: SessionDep
):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    menu_items = db.exec(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    ).all()

    reviews_raw = db.exec(
        select(Review).where(Review.restaurant_id == restaurant_id)
    ).all()

    reviews = []
    for r in reviews_raw:
        u = db.get(User, r.user_id)
        reviews.append({
            "id": r.id,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at,
            "username": u.username if u else "Unknown",
            "user_id": r.user_id
        })

    avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else None

    user_already_reviewed = False
    if user:
        existing = db.exec(
            select(Review).where(
                Review.restaurant_id == restaurant_id,
                Review.user_id == user.id
            )
        ).first()
        user_already_reviewed = existing is not None

    return templates.TemplateResponse(
        request=request,
        name="restaurant_menu.html",
        context={
            "user": user,
            "restaurant": restaurant,
            "menu_items": menu_items,
            "reviews": reviews,
            "avg_rating": avg_rating,
            "user_already_reviewed": user_already_reviewed
        }
    )


@router.post("/restaurant/{restaurant_id}/review", response_class=HTMLResponse)
async def submit_review(
    request: Request,
    restaurant_id: int,
    user: AuthDep,
    db: SessionDep,
    rating: int = Form(),
    comment: str = Form(default="")
):
    existing = db.exec(
        select(Review).where(
            Review.restaurant_id == restaurant_id,
            Review.user_id == user.id
        )
    ).first()

    if existing:
        flash(request, "You have already reviewed this place.", "danger")
        return RedirectResponse(
            url=request.url_for("restaurant_menu", restaurant_id=restaurant_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    if not (1 <= rating <= 5):
        flash(request, "Rating must be between 1 and 5.", "danger")
        return RedirectResponse(
            url=request.url_for("restaurant_menu", restaurant_id=restaurant_id),
            status_code=status.HTTP_303_SEE_OTHER
        )

    review = Review(
        restaurant_id=restaurant_id,
        user_id=user.id,
        rating=rating,
        comment=comment
    )
    db.add(review)
    db.commit()

    flash(request, "Review submitted successfully!", "success")
    return RedirectResponse(
        url=request.url_for("restaurant_menu", restaurant_id=restaurant_id),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/restaurant/{restaurant_id}/review/{review_id}/delete")
async def delete_review(
    request: Request,
    restaurant_id: int,
    review_id: int,
    user: AuthDep,
    db: SessionDep
):
    review = db.get(Review, review_id)
    if not review or (review.user_id != user.id and user.role != "admin"):
        flash(request, "Not authorized to delete this review.", "danger")
    else:
        db.delete(review)
        db.commit()
        flash(request, "Review deleted.", "success")

    return RedirectResponse(
        url=request.url_for("restaurant_menu", restaurant_id=restaurant_id),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/map/{restaurant_id}", response_class=HTMLResponse)
async def view_map(
    request: Request,
    restaurant_id: int,
    user: OptionalUser,
    db: SessionDep
):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return templates.TemplateResponse(
        request=request,
        name="map.html",
        context={
            "user": user,
            "restaurant": restaurant
        }
    )


@router.post("/order/add/{menu_item_id}")
async def add_to_order(
    request: Request,
    menu_item_id: int,
    user: OptionalUser,  # Changed from AuthDep to OptionalUser
    db: SessionDep,
    quantity: int = Form(...)
):
    menu_item = db.get(MenuItem, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # For guest users, store cart in session
    if not user:
        # Get or create guest cart in session
        guest_cart = request.session.get("guest_cart", [])
        
        # Check if item already in cart
        found = False
        for item in guest_cart:
            if item["menu_item_id"] == menu_item_id:
                item["quantity"] += quantity
                found = True
                break
        
        if not found:
            guest_cart.append({
                "menu_item_id": menu_item_id,
                "name": menu_item.name,
                "price": menu_item.price,
                "quantity": quantity,
                "restaurant_id": menu_item.restaurant_id,
                "restaurant_name": db.get(Restaurant, menu_item.restaurant_id).name
            })
        
        request.session["guest_cart"] = guest_cart
        flash(request, f"{menu_item.name} added to cart!", "success")
        
        return RedirectResponse(
            url=request.url_for("restaurant_menu", restaurant_id=menu_item.restaurant_id),
            status_code=status.HTTP_303_SEE_OTHER
        )
    
    # For logged-in users, use database
    order = db.exec(
        select(Order).where(
            Order.user_id == user.id,
            Order.status == "pending"  
        )
    ).first()

    if not order:
        order = Order(
            user_id=user.id,
            status="pending"
        )
        db.add(order)
        db.commit()
        db.refresh(order)

    order_item = OrderItem(
        order_id=order.id,
        menu_item_id=menu_item.id,
        quantity=quantity,
        price=menu_item.price
    )

    db.add(order_item)
    db.commit()

    flash(request, f"{menu_item.name} added to order!", "success")

    return RedirectResponse(
        url=request.url_for("restaurant_menu", restaurant_id=menu_item.restaurant_id),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/cart", response_class=HTMLResponse)
async def view_cart(
    request: Request,
    user: OptionalUser,
    db: SessionDep
):
    items_by_place = {}
    grand_total = 0.0
    
    # Handle guest cart from session
    if not user:
        guest_cart = request.session.get("guest_cart", [])
        
        for item in guest_cart:
            place_name = item.get("restaurant_name", "Unknown Place")
            
            if place_name not in items_by_place:
                # Get real phone from database for guest cart too
                restaurant = db.get(Restaurant, item.get("restaurant_id"))
                # Safely get phone attribute, handle if column doesn't exist
                phone = None
                if restaurant:
                    try:
                        phone = getattr(restaurant, 'phone', None)
                    except:
                        phone = None
                
                items_by_place[place_name] = {
                    "cart_items": [], 
                    "subtotal": 0.0,
                    "phone": phone
                }
            
            subtotal = item["quantity"] * item["price"]
            
            items_by_place[place_name]["cart_items"].append({
                "name": item["name"],
                "quantity": item["quantity"],
                "price": item["price"],
                "subtotal": subtotal,
                "menu_item_id": item["menu_item_id"]
            })
            
            items_by_place[place_name]["subtotal"] += subtotal
            grand_total += subtotal
        
        return templates.TemplateResponse(
            request=request,
            name="cart.html",
            context={
                "user": user,
                "items_by_place": items_by_place,
                "grand_total": grand_total,
                "is_guest": True
            }
        )
    
    # Handle logged-in user cart from database
    order = db.exec(
        select(Order).where(
            Order.user_id == user.id,
            Order.status == "pending"
        )
    ).first()

    if order:
        order_items = db.exec(
            select(OrderItem).where(OrderItem.order_id == order.id)
        ).all()

        for item in order_items:
            menu_item = db.get(MenuItem, item.menu_item_id)
            if not menu_item:
                continue

            restaurant = db.get(Restaurant, menu_item.restaurant_id)
            place_name = restaurant.name if restaurant else "Unknown Place"

            if place_name not in items_by_place:
                # Safely get phone attribute
                phone = None
                if restaurant:
                    try:
                        phone = getattr(restaurant, 'phone', None)
                    except:
                        phone = None
                    
                items_by_place[place_name] = {
                    "cart_items": [], 
                    "subtotal": 0.0,
                    "phone": phone
                }

            subtotal = item.quantity * item.price

            items_by_place[place_name]["cart_items"].append({
                "name": menu_item.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": subtotal,
                "order_item_id": item.id
            })

            items_by_place[place_name]["subtotal"] += subtotal
            grand_total += subtotal

    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "user": user,
            "items_by_place": items_by_place,
            "grand_total": grand_total,
            "is_guest": False
        }
    )


@router.post("/order/checkout")
async def checkout(
    user: AuthDep,
    db: SessionDep
):
    order = db.exec(
        select(Order).where(
            Order.user_id == user.id,
            Order.status == "pending"
        )
    ).first()

    if not order:
        raise HTTPException(status_code=400, detail="No active order")

    order.status = "placed"
    db.add(order)
    db.commit()

    return RedirectResponse("/cart", status_code=303)

@router.get("/map", response_class=HTMLResponse)
async def campus_map_view(
    request: Request,
    user: OptionalUser,
    db: SessionDep
):
    restaurants = db.exec(select(Restaurant)).all()
    return templates.TemplateResponse(
        request=request,
        name="map.html",
        context={"user": user, "restaurants": restaurants}
    )

@router.post("/cart/clear")
async def clear_cart(
    request: Request,
    user: OptionalUser,  # Changed from AuthDep to OptionalUser
    db: SessionDep
):
    # Handle guest cart
    if not user:
        request.session["guest_cart"] = []
        return JSONResponse({"success": True, "message": "Cart cleared successfully"})
    
    # Handle logged-in user
    order = db.exec(
        select(Order).where(
            Order.user_id == user.id,
            Order.status == "pending"
        )
    ).first()
    
    if order:
        order_items = db.exec(
            select(OrderItem).where(OrderItem.order_id == order.id)
        ).all()
        
        for item in order_items:
            db.delete(item)
        
        db.delete(order)
        db.commit()
    
    return JSONResponse({"success": True, "message": "Cart cleared successfully"})


@router.post("/cart/remove/{item_id}")
async def remove_cart_item(
    request: Request,
    item_id: int,
    user: OptionalUser,
    db: SessionDep
):
    # Handle guest cart removal
    if not user:
        guest_cart = request.session.get("guest_cart", [])
        guest_cart = [item for item in guest_cart if item.get("menu_item_id") != item_id]
        request.session["guest_cart"] = guest_cart
        return JSONResponse({"success": True, "message": "Item removed from cart"})
    
    # Handle logged-in user removal
    order_item = db.get(OrderItem, item_id)
    if order_item:
        db.delete(order_item)
        db.commit()
    
    return JSONResponse({"success": True, "message": "Item removed from cart"})

@router.post("/cart/change/{item_id}")
async def change_cart_item_quantity(
    request: Request,
    item_id: int,
    user: OptionalUser,
    db: SessionDep,
    delta: int = Query(0),
    new_quantity: int = Query(0)
):
    # Handle guest cart
    if not user:
        guest_cart = request.session.get("guest_cart", [])
        
        for idx, item in enumerate(guest_cart):
            if item.get("menu_item_id") == item_id:
                if new_quantity > 0:
                    # Set to specific quantity
                    item["quantity"] = new_quantity
                elif delta != 0:
                    # Change by delta amount
                    item["quantity"] += delta
                else:
                    return JSONResponse({"success": False, "message": "Invalid operation"}, status_code=400)
                
                # Remove item if quantity becomes 0 or less
                if item["quantity"] <= 0:
                    guest_cart.pop(idx)
                break
        
        request.session["guest_cart"] = guest_cart
        return JSONResponse({"success": True, "message": "Quantity updated"})
    
    # Handle logged-in user
    order_item = db.get(OrderItem, item_id)
    if order_item:
        if new_quantity > 0:
            # Set to specific quantity
            order_item.quantity = new_quantity
        elif delta != 0:
            # Change by delta amount
            order_item.quantity += delta
        else:
            return JSONResponse({"success": False, "message": "Invalid operation"}, status_code=400)
        
        if order_item.quantity <= 0:
            db.delete(order_item)
        else:
            db.add(order_item)
        db.commit()
    
    return JSONResponse({"success": True, "message": "Quantity updated"})