from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import AdminDep, SessionDep
from app.repositories.restaurant import RestaurantRepository
from app.repositories.menu import MenuRepository
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.review import Review
from app.models.user import User
from app.utilities.flash import flash
from . import router, templates
from sqlmodel import select

admin_router = APIRouter(prefix="/admin", tags=["admin"])

# ====================== PLACES ======================

@admin_router.get("/places", response_class=HTMLResponse, name="admin_places_list")
async def admin_places_list(request: Request, user: AdminDep, db: SessionDep):
    repo = RestaurantRepository(db)
    places = repo.get_all()
    return templates.TemplateResponse(
        request=request,
        name="admin/places_list.html",
        context={"places": places, "user": user}
    )

@admin_router.get("/places/new", response_class=HTMLResponse)
async def admin_place_new_form(request: Request, user: AdminDep):
    return templates.TemplateResponse(
        request=request,
        name="admin/place_form.html",
        context={"user": user, "place": None}
    )

@admin_router.post("/places/new")
async def admin_place_create(
    request: Request,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(),
    location: str = Form(),
    description: str = Form(default=""),
    latitude: float = Form(),
    longitude: float = Form()
):
    repo = RestaurantRepository(db)
    new_place = Restaurant(
        name=name,
        location=location,
        description=description,
        latitude=latitude,
        longitude=longitude
    )
    repo.create(new_place)
    flash(request, f"✅ {name} created successfully!", "success")
    return RedirectResponse(url=request.url_for("admin_places_list"), status_code=status.HTTP_303_SEE_OTHER)

@admin_router.get("/places/{place_id}/edit", response_class=HTMLResponse)
async def admin_place_edit_form(request: Request, place_id: int, user: AdminDep, db: SessionDep):
    repo = RestaurantRepository(db)
    place = repo.get_by_id(place_id)
    if not place:
        flash(request, "Place not found", "danger")
        return RedirectResponse(url=request.url_for("admin_places_list"))
    return templates.TemplateResponse(
        request=request,
        name="admin/place_form.html",
        context={"user": user, "place": place}
    )

@admin_router.post("/places/{place_id}/edit")
async def admin_place_update(
    request: Request,
    place_id: int,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(),
    location: str = Form(),
    description: str = Form(default=""),
    latitude: float = Form(),
    longitude: float = Form()
):
    repo = RestaurantRepository(db)
    updated = repo.update(place_id, {
        "name": name,
        "location": location,
        "description": description,
        "latitude": latitude,
        "longitude": longitude
    })
    flash(request, f"{name} updated successfully!", "success")
    return RedirectResponse(url=request.url_for("admin_places_list"), status_code=status.HTTP_303_SEE_OTHER)

@admin_router.post("/places/{place_id}/delete")
async def admin_place_delete(
    request: Request,
    place_id: int,
    user: AdminDep,
    db: SessionDep
):
    repo = RestaurantRepository(db)
    repo.delete(place_id)
    flash(request, "Place deleted successfully!", "success")
    return RedirectResponse(url=request.url_for("admin_places_list"), status_code=status.HTTP_303_SEE_OTHER)

# ====================== MENU ITEMS ======================

@admin_router.get("/places/{place_id}/menu", response_class=HTMLResponse, name="admin_menu_list")
async def admin_menu_list(request: Request, place_id: int, user: AdminDep, db: SessionDep):
    restaurant_repo = RestaurantRepository(db)
    menu_repo = MenuRepository(db)
    place = restaurant_repo.get_by_id(place_id)
    if not place:
        flash(request, "Place not found", "danger")
        return RedirectResponse(url=request.url_for("admin_places_list"))
    menu_items = menu_repo.get_by_restaurant(place_id)
    return templates.TemplateResponse(
        request=request,
        name="admin/menu_list.html",
        context={"place": place, "menu_items": menu_items, "user": user}
    )

@admin_router.get("/places/{place_id}/menu/new", response_class=HTMLResponse)
async def admin_menu_new_form(request: Request, place_id: int, user: AdminDep, db: SessionDep):
    restaurant_repo = RestaurantRepository(db)
    place = restaurant_repo.get_by_id(place_id)
    if not place:
        flash(request, "Place not found", "danger")
        return RedirectResponse(url=request.url_for("admin_places_list"))
    return templates.TemplateResponse(
        request=request,
        name="admin/menu_form.html",
        context={"place": place, "item": None, "user": user}
    )

@admin_router.post("/places/{place_id}/menu/new")
async def admin_menu_create(
    request: Request,
    place_id: int,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(),
    price: float = Form(),
    description: str = Form(default=""),
    is_available: bool = Form(default=True)
):
    repo = MenuRepository(db)
    new_item = MenuItem(
        name=name,
        price=price,
        description=description,
        is_available=is_available,
        restaurant_id=place_id
    )
    repo.create(new_item)
    flash(request, f"{name} added to menu!", "success")
    return RedirectResponse(url=f"/admin/places/{place_id}/menu", status_code=status.HTTP_303_SEE_OTHER)

@admin_router.get("/places/{place_id}/menu/{item_id}/edit", response_class=HTMLResponse)
async def admin_menu_edit_form(request: Request, place_id: int, item_id: int, user: AdminDep, db: SessionDep):
    menu_repo = MenuRepository(db)
    item = menu_repo.get_by_id(item_id)
    if not item or item.restaurant_id != place_id:
        flash(request, "Menu item not found", "danger")
        return RedirectResponse(url=f"/admin/places/{place_id}/menu")
    return templates.TemplateResponse(
        request=request,
        name="admin/menu_form.html",
        context={"place": None, "item": item, "user": user}
    )

@admin_router.post("/places/{place_id}/menu/{item_id}/edit")
async def admin_menu_update(
    request: Request,
    place_id: int,
    item_id: int,
    user: AdminDep,
    db: SessionDep,
    name: str = Form(),
    price: float = Form(),
    description: str = Form(default=""),
    is_available: bool = Form(default=True)
):
    repo = MenuRepository(db)
    repo.update(item_id, {
        "name": name,
        "price": price,
        "description": description,
        "is_available": is_available
    })
    flash(request, f"{name} updated!", "success")
    return RedirectResponse(url=f"/admin/places/{place_id}/menu", status_code=status.HTTP_303_SEE_OTHER)

@admin_router.post("/places/{place_id}/menu/{item_id}/toggle")
async def admin_menu_toggle_availability(
    request: Request,
    place_id: int,
    item_id: int,
    user: AdminDep,
    db: SessionDep
):
    menu_repo = MenuRepository(db)
    item = menu_repo.get_by_id(item_id)
    if not item or item.restaurant_id != place_id:
        flash(request, "Menu item not found", "danger")
        return RedirectResponse(url=f"/admin/places/{place_id}/menu", status_code=status.HTTP_303_SEE_OTHER)
    
    item.is_available = not item.is_available
    db.add(item)
    db.commit()
    
    status_text = "enabled" if item.is_available else "disabled"
    flash(request, f"Menu item '{item.name}' has been {status_text}!", "success")
    return RedirectResponse(url=f"/admin/places/{place_id}/menu", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.get("/reviews", response_class=HTMLResponse, name="admin_reviews")
async def admin_reviews_list(request: Request, user: AdminDep, db: SessionDep):
    reviews = db.exec(
        select(Review, Restaurant.name.label("restaurant_name"), User.username)
        .join(Restaurant, Review.restaurant_id == Restaurant.id)
        .join(User, Review.user_id == User.id)
        .order_by(Review.created_at.desc())
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/reviews.html",
        context={
            "user": user,
            "reviews": reviews
        }
    )

@admin_router.post("/reviews/{review_id}/delete")
async def admin_review_delete(
    request: Request,
    review_id: int,
    user: AdminDep,
    db: SessionDep
):
    review = db.get(Review, review_id)
    if not review:
        flash(request, "Review not found", "danger")
    else:
        db.delete(review)
        db.commit()
        flash(request, "Review deleted successfully!", "success")
    
    return RedirectResponse(url=request.url_for("admin_reviews"), status_code=status.HTTP_303_SEE_OTHER)