from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from sqlmodel import select
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    restaurants = db.exec(select(Restaurant)).all()

    return templates.TemplateResponse(
        request=request, 
        name="app.html",
        context={
            "user": user,
            "restaurants": restaurants
        }
    )

@router.get("/restaurant/{restaurant_id}", response_class=HTMLResponse)
async def restaurant_menu(
    request: Request,
    restaurant_id: int,
    user: AuthDep,
    db: SessionDep
):
    restaurant = db.get(Restaurant, restaurant_id)

    menu_items = db.exec(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="restaurant_menu.html",
        context={
            "user": user,
            "restaurant": restaurant,
            "menu_items": menu_items
        }
    )

@router.get("/map/{restaurant_id}", response_class=HTMLResponse)
async def view_map(
    request: Request,
    restaurant_id: int,
    user: AuthDep,
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