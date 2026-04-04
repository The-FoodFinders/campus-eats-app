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

        restaurant1 = Restaurant(
            name="Lindas",
            description="Affordable student meals",
            location="UWI St. Augustine",
            latitude=10.638671,
            longitude=-61.398127
        )

        restaurant2 = Restaurant(
            name="KFC",
            description="Affordable student meals",
            location="UWI St. Augustine",
            latitude=10.639109,
            longitude=-61.398151
        )

        restaurant3 = Restaurant(
            name="Rituals",
            description="Affordable student meals",
            location="UWI St. Augustine",
            latitude=10.638868,
            longitude=-61.398615
        )
        
        db.add_all([
            restaurant1,
            restaurant2,
            restaurant3
        ])

        db.commit()

        menu_items = [
            MenuItem(
                name="Chicken Sandwich",
                price=25.0,
                description="Grilled chicken with lettuce and sauce",
                restaurant_id=restaurant2.id
            ),
            MenuItem(
                name="Beef Patty",
                price=15.0,
                description="Juicy beef patty",
                restaurant_id=restaurant1.id
            ),
            MenuItem(
                name="Coffee",
                price=38.0,
                description="Classic Trinidad street food",
                restaurant_id=restaurant3.id
            ),
        ]

        db.add_all(menu_items)
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