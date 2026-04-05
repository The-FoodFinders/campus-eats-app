import typer
import csv
from tabulate import tabulate
from sqlmodel import select
from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.utilities.security import encrypt_password
from app.repositories.user import UserRepository
from app.schemas.user import AdminCreate, RegularUserCreate

app = typer.Typer()

@app.command()
def initialize():
    with get_cli_session() as db:
        drop_all() 
        create_db_and_tables()  
        
        
        admin_password = encrypt_password("bobpass")
        bob = User(
            username='bob', 
            email='bob@email.com',
            password=admin_password,
            role='admin'
        )
        
        #she's a registered user
        alice_password = encrypt_password("alicepass")
        alice = User(
            username='alice',
            email='alice@email.com',
            password=alice_password,
            role='regular_user'
        )

        db.add_all([bob, alice])
        db.commit()

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
        
        print("Database Initialized !!")

@app.command()
def list_users():
    #for debugging
    with get_cli_session() as db:
        repo = UserRepository(db)
        users = repo.get_all_users()
        if not users:
            print("No users found.")
            return
        
        table_data = [[user.id, user.username, user.role, user.email] for user in users]
        print(tabulate(table_data, headers=["ID", "Username", "Role", "Email"], tablefmt="grid"))

if __name__ == "__main__":
    app()