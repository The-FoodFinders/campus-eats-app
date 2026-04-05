from app.database import create_db_and_tables
from sqlmodel import Session, select
from app.database import engine
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.user import User
from app.utilities.security import encrypt_password


def seed():
    create_db_and_tables()
    with Session(engine) as db:
        existing = db.exec(select(Restaurant)).first()
        if existing:
            print("Already seeded!")
            return

        places = [
            Restaurant(name="Main Cafeteria", location="Student Activity Centre, UWI", description="Central cafeteria serving local Trinidadian dishes daily.", latitude=10.6425, longitude=-61.3990),
            Restaurant(name="Engineering Canteen", location="Faculty of Engineering, UWI", description="Quick bites and hearty meals. Famous for breakfast doubles.", latitude=10.6430, longitude=-61.4005),
            Restaurant(name="Med Sci Canteen", location="Faculty of Medical Sciences, UWI", description="Fresh salads, sandwiches and smoothies.", latitude=10.6415, longitude=-61.3975),
            Restaurant(name="Piazza Food Court", location="The Piazza, UWI", description="Outdoor food court with multiple vendors.", latitude=10.6422, longitude=-61.3985),
            Restaurant(name="Agri Canteen", location="Faculty of Food & Agriculture, UWI", description="Fresh local food at great prices.", latitude=10.6408, longitude=-61.3960),
        ]

        for place in places:
            db.add(place)
        db.commit()

        for place in places:
            db.refresh(place)

        items = [
            MenuItem(name="Pelau", price=45.0, description="Rice with pigeon peas and chicken", is_available=True, restaurant_id=places[0].id),
            MenuItem(name="Macaroni Pie", price=30.0, description="Baked macaroni with cheese", is_available=True, restaurant_id=places[0].id),
            MenuItem(name="Roti & Curry", price=40.0, description="Dhalpuri roti with curry", is_available=True, restaurant_id=places[0].id),
            MenuItem(name="Fresh Lime Juice", price=12.0, description="Freshly squeezed lime juice", is_available=True, restaurant_id=places[0].id),
            MenuItem(name="Doubles", price=8.0, description="Two bara with curried channa", is_available=True, restaurant_id=places[1].id),
            MenuItem(name="Bake & Shark", price=35.0, description="Fried bake with shark fillet", is_available=True, restaurant_id=places[1].id),
            MenuItem(name="Chicken Sandwich", price=28.0, description="Grilled chicken on hops bread", is_available=True, restaurant_id=places[1].id),
            MenuItem(name="Greek Salad", price=35.0, description="Fresh greens, olives, feta and tomato", is_available=True, restaurant_id=places[2].id),
            MenuItem(name="Fruit Smoothie", price=20.0, description="Blended seasonal fruits", is_available=True, restaurant_id=places[2].id),
            MenuItem(name="Jerk Chicken Platter", price=55.0, description="Smoky jerk chicken with rice", is_available=True, restaurant_id=places[3].id),
            MenuItem(name="Corn Soup", price=25.0, description="Thick Trini corn soup", is_available=True, restaurant_id=places[3].id),
            MenuItem(name="Provision & Saltfish", price=45.0, description="Local ground provisions with saltfish", is_available=True, restaurant_id=places[4].id),
            MenuItem(name="Coconut Water", price=20.0, description="Fresh young coconut", is_available=True, restaurant_id=places[4].id),
        ]

        for item in items:
            db.add(item)
        db.commit()

        existing_bob = db.exec(select(User).where(User.username == "bob")).first()
        if not existing_bob:
            bob = User(
                username="bob",
                email="bob@sta.uwi.edu",
                password=encrypt_password("bobpass"),
                role="regular_user"
            )
            db.add(bob)
            db.commit()

        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed()
