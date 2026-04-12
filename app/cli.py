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

user_app = typer.Typer()
restaurant_app = typer.Typer()
menu_app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(restaurant_app, name="restaurant")
app.add_typer(menu_app, name="menu")

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
            Restaurant(name="Dee & Vees", location="School of Education Compound", description="Authentic Creole food vendor serving hearty local Trinidadian meals.", latitude=10.6418, longitude=-61.3963, category="School of Education", phone="Unknown"),
            Restaurant(name="La Bloom Café", location="Centre for Language and Learning", description="Coffee, drinks and a variety of food items. A great spot to recharge between classes.", latitude=10.6427, longitude=-61.3978, category="Language & Learning", phone="Unknown"),
            Restaurant(name="Vending Machine (Ice Cream)", location="Student Activity Centre (SAC) Ground Floor", description="Ice cream and lollies vending machine. Quick sweet treats between classes.", latitude=10.6424, longitude=-61.3990, category="SAC", phone="Unknown"),
            Restaurant(name="Caribbean Natural Juices", location="Student Activity Centre (SAC) Ground Floor", description="Fresh squeezed juices and natural beverages made from local fruits.", latitude=10.6424, longitude=-61.3991, category="SAC", phone="Unknown"),
            Restaurant(name="Celes and Son Home-style Cooking", location="Student Activity Centre (SAC) Ground Floor", description="Creole home-style cooking with hearty local dishes at student-friendly prices.", latitude=10.6423, longitude=-61.3992, category="SAC", phone="+1868-663-6183"),
            Restaurant(name="Maureen's Cuisine", location="Student Activity Centre (SAC) Ground Floor", description="Serving pies, sandwiches and snacks. A popular stop for a quick bite.", latitude=10.6423, longitude=-61.3993, category="SAC", phone="Unknown"),
            Restaurant(name="Oriental Cuisine", location="Student Activity Centre (SAC) Ground Floor", description="Chinese food served fresh daily. Popular for fried rice, chow mein and more.", latitude=10.6422, longitude=-61.3991, category="SAC", phone="Unknown"),
            Restaurant(name="Lee's Doubles", location="Student Activity Centre (SAC) Ground Floor", description="Classic Trini doubles and street food. A campus favourite for breakfast and lunch.", latitude=10.6422, longitude=-61.3990, category="SAC", phone="Unknown"),
            Restaurant(name="Juman's Roti Shop", location="Student Activity Centre (SAC) 2nd Floor", description="Authentic Trini roti — dhalpuri and paratha with a variety of curries.", latitude=10.6424, longitude=-61.3989, category="SAC", phone="+1868-645-5104"),
            Restaurant(name="Veg & More", location="Close to Student Activity Centre (SAC)", description="Pies, pastries and drinks. Great vegetarian-friendly options on campus.", latitude=10.6421, longitude=-61.3988, category="SAC", phone="+1868-769-4424"),
            Restaurant(name="Mini Mart (SAC)", location="Student Activities Centre", description="Campus convenience store stocking snacks, drinks and everyday essentials.", latitude=10.6423, longitude=-61.3987, category="SAC", phone="Unknown"),
            Restaurant(name="Mini Mart (SAL Hall)", location="SAL Hall", description="Convenient store near SAL Hall with snacks, beverages and daily necessities.", latitude=10.6432, longitude=-61.3985, category="Halls of Residence", phone="Unknown"),
            Restaurant(name="Pita Pit", location="JFK Quadrangle", description="Wraps, paninis and pita pockets with fresh fillings. A healthy and tasty choice.", latitude=10.6430, longitude=-61.3999, category="JFK", phone="+1868-285-7482"),
            Restaurant(name="Rituals Coffee House", location="JFK Quadrangle", description="Premium coffee, teas, cold drinks and food items. The campus coffee hotspot.", latitude=10.6431, longitude=-61.4000, category="JFK", phone="+1868-225-5125"),
            Restaurant(name="Linda's", location="JFK Quadrangle", description="Freshly baked pastries, salads, breads and natural juices. A campus institution.", latitude=10.6429, longitude=-61.3998, category="JFK", phone="+1868-280-2350"),
            Restaurant(name="Ave 5055", location="JFK Quadrangle", description="Desserts, sweet treats and indulgent snacks to satisfy your sweet tooth.", latitude=10.6430, longitude=-61.3997, category="JFK", phone="Unknown"),
            Restaurant(name="The Gourmet Pot", location="Dudley Huggins Building", description="Contemporary cuisine with diverse menu options. Elevated campus dining.", latitude=10.6435, longitude=-61.4008, category="Dudley Huggins", phone="+1868-610-9768"),
            Restaurant(name="KFC", location="JFK Food Court", description="Kentucky Fried Chicken — fries, chicken and combos from the globally loved brand.", latitude=10.6428, longitude=-61.4003, category="JFK Food Court", phone="+1868-225-4532"),
            Restaurant(name="Subway", location="JFK Food Court", description="Sub sandwiches made to order with fresh bread, proteins and toppings.", latitude=10.6428, longitude=-61.4004, category="JFK Food Court", phone="+1868-226-7874"),
            Restaurant(name="Benny's BBQ & Burgers", location="Car Park next to Staff Social Club", description="Burgers and BBQ done right. Smoky flavours with generous portions.", latitude=10.6412, longitude=-61.4010, category="Staff Social Club Area", phone="+1868-704-0400"),
            Restaurant(name="Boba and Brew Café", location="Republic Bank Plaza – UWI", description="Pastries, smoothies and ice cream. A trendy café spot on campus.", latitude=10.6440, longitude=-61.3980, category="Republic Bank Plaza", phone="+1868-615-8222"),
            Restaurant(name="Blue Waters Vending", location="Main Campus & School of Education", description="Blue Waters vending machines offering chilled beverages across campus.", latitude=10.6425, longitude=-61.3975, category="Vending", phone="Unknown"),
            Restaurant(name="Al Mohammed on the Link Up", location="Teaching and Learning Centre", description="Burgers and sandwiches served near the Teaching and Learning Centre.", latitude=10.6433, longitude=-61.3995, category="Teaching & Learning Centre", phone="Unknown"),
            Restaurant(name="Snack Machine (Couva)", location="Couva Facilities", description="Snack vending machine at the Couva campus facility.", latitude=10.5890, longitude=-61.4200, category="Couva", phone="Unknown"),
        ]

        for place in places:
            db.add(place)
        db.commit()
        for place in places:
            db.refresh(place)

        def pid(name):
            for p in places:
                if p.name == name:
                    return p.id
            raise ValueError(f"Place not found: {name}")

        items = [
            # Dee & Vees
            MenuItem(name="Pelau", price=50.0, description="Rice cooked with pigeon peas, chicken and coconut milk", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Stewed Chicken & Rice", price=55.0, description="Slow-stewed chicken with white rice and macaroni", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Macaroni Pie", price=30.0, description="Baked macaroni with seasoned minced beef and cheese", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Callaloo & Crab", price=60.0, description="Dasheen bush cooked with blue crab, served with provisions", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Sorrel Drink", price=12.0, description="Refreshing chilled sorrel beverage", is_available=True, restaurant_id=pid("Dee & Vees")),
            # La Bloom Café
            MenuItem(name="Cappuccino", price=25.0, description="Espresso with steamed milk foam", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Iced Latte", price=28.0, description="Chilled espresso with milk over ice", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Chicken Sandwich", price=40.0, description="Grilled chicken on toasted bread with fresh lettuce and tomato", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Cheese Croissant", price=20.0, description="Buttery croissant filled with melted cheddar cheese", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Fresh Orange Juice", price=18.0, description="Freshly squeezed orange juice", is_available=True, restaurant_id=pid("La Bloom Café")),
            # Caribbean Natural Juices
            MenuItem(name="Lime Juice", price=12.0, description="Freshly squeezed lime juice, sweetened to taste", is_available=True, restaurant_id=pid("Caribbean Natural Juices")),
            MenuItem(name="Passion Fruit Juice", price=15.0, description="Fresh passion fruit blended with water and sugar", is_available=True, restaurant_id=pid("Caribbean Natural Juices")),
            MenuItem(name="Watermelon Juice", price=14.0, description="Cold blended watermelon juice", is_available=True, restaurant_id=pid("Caribbean Natural Juices")),
            MenuItem(name="Mango Juice", price=15.0, description="Thick blended mango juice from local mangoes", is_available=True, restaurant_id=pid("Caribbean Natural Juices")),
            MenuItem(name="Mixed Fruit Punch", price=16.0, description="Blend of seasonal tropical fruits", is_available=True, restaurant_id=pid("Caribbean Natural Juices")),
            # Celes and Son
            MenuItem(name="Stewed Beef & Rice", price=55.0, description="Tender stewed beef with white rice and peas", is_available=True, restaurant_id=pid("Celes and Son Home-style Cooking")),
            MenuItem(name="Dhal & Rice", price=40.0, description="Split peas dhal with steamed white rice", is_available=True, restaurant_id=pid("Celes and Son Home-style Cooking")),
            MenuItem(name="Bodi & Potato Curry", price=45.0, description="Long beans and potato cooked in curry sauce", is_available=True, restaurant_id=pid("Celes and Son Home-style Cooking")),
            MenuItem(name="Fried Bake", price=10.0, description="Light fluffy fried bake, served alone or with filling", is_available=True, restaurant_id=pid("Celes and Son Home-style Cooking")),
            MenuItem(name="Lemonade", price=12.0, description="Chilled homemade lemonade", is_available=True, restaurant_id=pid("Celes and Son Home-style Cooking")),
            # Maureen's Cuisine
            MenuItem(name="Cheese Pie", price=15.0, description="Flaky pastry filled with seasoned cheese", is_available=True, restaurant_id=pid("Maureen's Cuisine")),
            MenuItem(name="Chicken Pie", price=18.0, description="Golden pastry with seasoned chicken filling", is_available=True, restaurant_id=pid("Maureen's Cuisine")),
            MenuItem(name="Ham & Cheese Sandwich", price=25.0, description="Soft hops bread with ham, cheese and lettuce", is_available=True, restaurant_id=pid("Maureen's Cuisine")),
            MenuItem(name="Sausage Roll", price=14.0, description="Puff pastry wrapped around spiced pork sausage", is_available=True, restaurant_id=pid("Maureen's Cuisine")),
            MenuItem(name="Juice Box", price=10.0, description="Assorted juice boxes — various flavours", is_available=True, restaurant_id=pid("Maureen's Cuisine")),
            # Oriental Cuisine
            MenuItem(name="Fried Rice", price=40.0, description="Classic Chinese-style fried rice with egg and vegetables", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Chow Mein", price=45.0, description="Stir-fried noodles with mixed vegetables and soy sauce", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Sweet & Sour Chicken", price=55.0, description="Crispy chicken tossed in tangy sweet and sour sauce", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Wonton Soup", price=30.0, description="Light broth with pork dumplings and scallions", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Spring Rolls (2 pcs)", price=20.0, description="Crispy vegetable spring rolls with dipping sauce", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            # Lee's Doubles
            MenuItem(name="Doubles", price=8.0, description="Two bara with curried channa — the classic Trini breakfast", is_available=True, restaurant_id=pid("Lee's Doubles")),
            MenuItem(name="Doubles with Slight", price=8.0, description="Doubles with mild pepper sauce", is_available=True, restaurant_id=pid("Lee's Doubles")),
            MenuItem(name="Doubles with Extra Pepper", price=8.0, description="Doubles loaded with hot pepper sauce for the brave", is_available=True, restaurant_id=pid("Lee's Doubles")),
            MenuItem(name="Aloo Pie", price=10.0, description="Fried dough filled with curried potato and seasoning", is_available=True, restaurant_id=pid("Lee's Doubles")),
            MenuItem(name="Pholourie", price=10.0, description="Fried split peas fritters served with tamarind sauce", is_available=True, restaurant_id=pid("Lee's Doubles")),
            # Juman's Roti Shop
            MenuItem(name="Dhalpuri with Chicken Curry", price=45.0, description="Layered dhalpuri roti filled with chicken curry", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Dhalpuri with Goat Curry", price=50.0, description="Dhalpuri roti with slow-cooked curried goat", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Paratha with Aloo", price=35.0, description="Flaky paratha roti with curried potato", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Bus-Up-Shot with Shrimp", price=55.0, description="Torn paratha roti with curried shrimp filling", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Mango Chow", price=15.0, description="Green mango with pepper, garlic and chadon beni", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            # Veg & More
            MenuItem(name="Spinach Pie", price=15.0, description="Pastry filled with seasoned spinach", is_available=True, restaurant_id=pid("Veg & More")),
            MenuItem(name="Vegetable Patty", price=14.0, description="Golden patty filled with mixed vegetables", is_available=True, restaurant_id=pid("Veg & More")),
            MenuItem(name="Apple Juice", price=12.0, description="Chilled apple juice", is_available=True, restaurant_id=pid("Veg & More")),
            MenuItem(name="Cheese Straw", price=8.0, description="Crunchy baked cheese straws", is_available=True, restaurant_id=pid("Veg & More")),
            # Pita Pit
            MenuItem(name="Chicken Caesar Wrap", price=45.0, description="Grilled chicken with Caesar dressing in a flour tortilla wrap", is_available=True, restaurant_id=pid("Pita Pit")),
            MenuItem(name="Tuna Panini", price=40.0, description="Pressed panini with tuna, lettuce, tomato and mayo", is_available=True, restaurant_id=pid("Pita Pit")),
            MenuItem(name="BBQ Chicken Pita", price=48.0, description="Grilled chicken in pita bread with BBQ sauce and coleslaw", is_available=True, restaurant_id=pid("Pita Pit")),
            MenuItem(name="Veggie Pita", price=35.0, description="Pita loaded with fresh vegetables and hummus", is_available=True, restaurant_id=pid("Pita Pit")),
            MenuItem(name="Bottled Water", price=8.0, description="500ml chilled bottled water", is_available=True, restaurant_id=pid("Pita Pit")),
            # Rituals Coffee House
            MenuItem(name="Espresso", price=20.0, description="Strong single shot of espresso", is_available=True, restaurant_id=pid("Rituals Coffee House")),
            MenuItem(name="Cappuccino", price=28.0, description="Espresso with steamed milk and foam", is_available=True, restaurant_id=pid("Rituals Coffee House")),
            MenuItem(name="Caramel Frappé", price=38.0, description="Blended iced coffee with caramel syrup and whipped cream", is_available=True, restaurant_id=pid("Rituals Coffee House")),
            MenuItem(name="Chocolate Muffin", price=20.0, description="Moist double chocolate chip muffin", is_available=True, restaurant_id=pid("Rituals Coffee House")),
            MenuItem(name="Club Sandwich", price=45.0, description="Triple-decker sandwich with chicken, bacon, egg and lettuce", is_available=True, restaurant_id=pid("Rituals Coffee House")),
            # Linda's
            MenuItem(name="Coconut Bake", price=12.0, description="Traditional coconut-flavoured baked bread roll", is_available=True, restaurant_id=pid("Linda's")),
            MenuItem(name="Fruit Salad", price=20.0, description="Fresh seasonal fruit salad with a squeeze of lime", is_available=True, restaurant_id=pid("Linda's")),
            MenuItem(name="Guava Cheese", price=10.0, description="Sweet guava paste — a traditional Trinidadian treat", is_available=True, restaurant_id=pid("Linda's")),
            MenuItem(name="Tamarind Balls", price=8.0, description="Sweet and tangy tamarind candy balls", is_available=True, restaurant_id=pid("Linda's")),
            MenuItem(name="Fresh Carrot Juice", price=15.0, description="Freshly blended carrot juice", is_available=True, restaurant_id=pid("Linda's")),
            # Ave 5055
            MenuItem(name="Ice Cream Cone", price=15.0, description="Creamy soft-serve ice cream in a cone", is_available=True, restaurant_id=pid("Ave 5055")),
            MenuItem(name="Brownie Slice", price=20.0, description="Rich dark chocolate brownie", is_available=True, restaurant_id=pid("Ave 5055")),
            MenuItem(name="Cheesecake Slice", price=25.0, description="Smooth New York-style cheesecake", is_available=True, restaurant_id=pid("Ave 5055")),
            MenuItem(name="Chocolate Cake Slice", price=22.0, description="Moist layered chocolate cake with ganache icing", is_available=True, restaurant_id=pid("Ave 5055")),
            # The Gourmet Pot
            MenuItem(name="Grilled Salmon", price=85.0, description="Pan-seared salmon fillet with herb butter and seasonal vegetables", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Pasta Primavera", price=60.0, description="Fettuccine with sautéed seasonal vegetables in garlic olive oil", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Beef Burger", price=65.0, description="Hand-pressed beef patty with gourmet toppings on a brioche bun", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Caesar Salad", price=40.0, description="Romaine lettuce, croutons, parmesan and Caesar dressing", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Sparkling Water", price=15.0, description="Chilled sparkling water", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            # KFC
            MenuItem(name="2-Piece Meal", price=75.0, description="Two pieces of Original Recipe chicken with fries and a drink", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Zinger Burger Meal", price=80.0, description="Spicy Zinger chicken burger with fries and a drink", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Popcorn Chicken", price=45.0, description="Bite-sized crispy chicken pieces", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Coleslaw", price=15.0, description="KFC signature creamy coleslaw", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Soft Drink (Medium)", price=18.0, description="Pepsi, 7-Up or Mirinda — medium size", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Krunch Twist", price=29.95, description="Crispy KFC chicken fillet twisted in a soft tortilla wrap with fresh lettuce and creamy mayo", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Krunch Twist Combo", price=39.95, description="Krunch Twist wrap paired with a side of fries and a medium drink for the full meal experience", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Mac & Cheese", price=20.0, description="Creamy KFC macaroni and cheese in a regular portion", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Mash & Gravy", price=18.0, description="Smooth mashed potatoes topped with rich KFC gravy", is_available=True, restaurant_id=pid("KFC")),
            # Subway
            MenuItem(name="Italian BMT (6-inch)", price=55.0, description="Pepperoni, salami and ham on Italian bread with your choice of toppings", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Chicken Teriyaki (Footlong)", price=85.0, description="Teriyaki chicken strip sub on honey oat bread", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Veggie Delite (6-inch)", price=45.0, description="Fresh garden vegetables on your choice of bread", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Cookies (3 pack)", price=20.0, description="Freshly baked Subway cookies — chocolate chip or macadamia nut", is_available=True, restaurant_id=pid("Subway")),
            # Benny's BBQ & Burgers
            MenuItem(name="BBQ Burger", price=60.0, description="Beef patty with smoky BBQ sauce, cheddar and caramelised onions", is_available=True, restaurant_id=pid("Benny's BBQ & Burgers")),
            MenuItem(name="Smoked BBQ Ribs", price=90.0, description="Slow-smoked pork ribs glazed with house BBQ sauce", is_available=True, restaurant_id=pid("Benny's BBQ & Burgers")),
            MenuItem(name="BBQ Chicken Platter", price=70.0, description="Grilled BBQ chicken with coleslaw and fries", is_available=True, restaurant_id=pid("Benny's BBQ & Burgers")),
            MenuItem(name="Loaded Fries", price=35.0, description="Fries topped with cheese sauce, bacon bits and jalapeños", is_available=True, restaurant_id=pid("Benny's BBQ & Burgers")),
            # Boba and Brew Café
            MenuItem(name="Classic Milk Tea Boba", price=35.0, description="Creamy milk tea with tapioca pearls", is_available=True, restaurant_id=pid("Boba and Brew Café")),
            MenuItem(name="Taro Boba", price=38.0, description="Taro milk tea with chewy boba pearls", is_available=True, restaurant_id=pid("Boba and Brew Café")),
            MenuItem(name="Mango Smoothie", price=30.0, description="Thick blended mango smoothie", is_available=True, restaurant_id=pid("Boba and Brew Café")),
            MenuItem(name="Strawberry Ice Cream", price=25.0, description="Two scoops of strawberry ice cream", is_available=True, restaurant_id=pid("Boba and Brew Café")),
            MenuItem(name="Croissant", price=20.0, description="Buttery baked croissant", is_available=True, restaurant_id=pid("Boba and Brew Café")),
            # Al Mohammed on the Link Up
            MenuItem(name="Classic Burger", price=50.0, description="Beef patty with lettuce, tomato, onion and special sauce", is_available=True, restaurant_id=pid("Al Mohammed on the Link Up")),
            MenuItem(name="Chicken Sandwich", price=45.0, description="Crispy fried chicken fillet on a toasted bun", is_available=True, restaurant_id=pid("Al Mohammed on the Link Up")),
            MenuItem(name="Doubles", price=8.0, description="Trini-style doubles with curried channa", is_available=True, restaurant_id=pid("Al Mohammed on the Link Up")),
            MenuItem(name="Soft Drink", price=10.0, description="Chilled canned soft drink", is_available=True, restaurant_id=pid("Al Mohammed on the Link Up")),
        ]

        for item in items:
            db.add(item)
        db.commit()
        
        print("Database Initialized with all 24 UWI campus food vendors!")

@user_app.command("create")
def create_user(username: str, email: str, password: str, role: str = "regular_user"):
    with get_cli_session() as db:
        user = User(username=username, email=email, password=password, role=role)
        db.add(user)
        db.commit()
        typer.echo(f"Created user: {username}")

@user_app.command("list")
def list_users():
    with get_cli_session() as db:
        users = db.exec(select(User)).all()

        table = [[u.id, u.username, u.email, u.role] for u in users]
        typer.echo(tabulate(table, headers=["ID", "Username", "Email", "Role"]))

@user_app.command("delete")
def delete_user(user_id: int, confirm: bool = False):
    if not confirm:
        typer.echo("Add --confirm to delete")
        return

    with get_cli_session() as db:
        user = db.get(User, user_id)

        if not user:
            typer.echo("User not found")
            return

        db.delete(user)
        db.commit()
        typer.echo(f"Deleted user {user_id}")


@restaurant_app.command("list")
def list_restaurants():
    with get_cli_session() as db:
        restaurants = db.exec(select(Restaurant)).all()

        table = [[r.id, r.name, r.location] for r in restaurants]
        typer.echo(tabulate(table, headers=["ID", "Name", "Location"]))

@app.command()
def update_restaurant(restaurant_id: int, name: str = None, location: str = None, description: str = None, phone: str = None):
    with get_cli_session() as db:
        restaurant = db.get(Restaurant, restaurant_id)

        if not restaurant:
            print("Restaurant not found")
            return

        if name:
            restaurant.name = name
        if location:
            restaurant.location = location
        if description:
            restaurant.description = description
        if phone:
            restaurant.phone = phone

        db.add(restaurant)
        db.commit()

        print(f"Restaurant {restaurant_id} updated successfully")

@restaurant_app.command("delete")
def delete_restaurant(restaurant_id: int, confirm: bool = False):
    if not confirm:
        typer.echo("Add --confirm to delete")
        return

    with get_cli_session() as db:
        r = db.get(Restaurant, restaurant_id)

        if not r:
            typer.echo("Restaurant not found")
            return

        db.delete(r)
        db.commit()
        typer.echo(f"Deleted restaurant {restaurant_id}")


@menu_app.command("delete")
def delete_menu_item(item_id: int, confirm: bool = False):
    if not confirm:
        typer.echo("Add --confirm to delete")
        return

    with get_cli_session() as db:
        item = db.get(MenuItem, item_id)

        if not item:
            typer.echo("Item not found")
            return

        db.delete(item)
        db.commit()
        typer.echo(f"Deleted menu item {item_id}")

@menu_app.command("list")
def list_menu():
    with get_cli_session() as db:
        items = db.exec(select(MenuItem)).all()

        table = [[i.id, i.name, i.price, i.restaurant_id] for i in items]
        typer.echo(tabulate(table, headers=["ID", "Name", "Price", "Restaurant"]))

if __name__ == "__main__":
    app()