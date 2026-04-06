from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies import AdminDep, SessionDep
from app.repositories.restaurant import RestaurantRepository
from app.repositories.menu import MenuRepository
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.utilities.flash import flash
from . import router, templates

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
        context={"user": user}
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
    flash(request, f"✅ {name} added successfully!", "success")
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
        context={"place": place, "user": user}
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
    flash(request, f"✅ {name} added to menu!", "success")
    return RedirectResponse(url=f"/admin/places/{place_id}/menu", status_code=status.HTTP_303_SEE_OTHER)