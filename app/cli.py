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
            Restaurant(name="Dee & Vees", location="School of Education Compound", description="Authentic Creole food vendor serving hearty local Trinidadian meals.", latitude=10.64664, longitude=-61.40291, category="School of Education", phone="Unknown"),
            Restaurant(name="La Bloom Café", location="Centre for Language and Learning", description="Coffee, drinks and a variety of food items. A great spot to recharge between classes.", latitude=10.64259, longitude=-61.39870, category="Language & Learning", phone="Unknown"),
            Restaurant(name="Vending Machine (Drinks)", location="Student Activity Centre (SAC) Ground Floor", description="Assorted drinks of all varieties. Quick pick me ups between classes.", latitude=10.63937, longitude=-61.39763, category="Vending", phone="Unknown"),
            Restaurant(name="Just Juiced", location="Student Activity Centre (SAC) Ground Floor", description="Fresh squeezed juices and natural beverages made from local fruits.", latitude=10.63947, longitude=-61.39771, category="SAC", phone="Unknown"),
            Restaurant(name="Oriental Cuisine", location="Student Activity Centre (SAC) Ground Floor", description="Chinese food served fresh daily. Popular for fried rice, chow mein and more.", latitude=10.63970, longitude=-61.39785, category="SAC", phone="Unknown"),
            Restaurant(name="Panks Sweet Sauce Doubles", location="Student Activity Centre (SAC) Ground Floor", description="Classic Trini doubles and street food. A campus favourite for breakfast and lunch.", latitude=10.63931, longitude=-61.39800, category="SAC", phone="Unknown"),
            Restaurant(name="Juman's Roti Shop", location="Student Activity Centre (SAC) 2nd Floor", description="Authentic Trini roti — dhalpuri and paratha with a variety of curries.", latitude=10.63967, longitude=-61.39767, category="SAC", phone="+1868-645-5104"),
            Restaurant(name="Veg Out", location="Close to Student Activity Centre (SAC)", description="Pies, pastries and drinks. Great vegetarian-friendly options on campus.", latitude=10.63919, longitude=-61.39786, category="SAC", phone="+1868-769-4424"),
            Restaurant(name="Campus Mini Mart", location="Student Activities Centre", description="Campus convenience store stocking snacks, drinks and everyday essentials.", latitude=10.63926, longitude=-61.39784, category="SAC", phone="Unknown"),
            Restaurant(name="Bago Thingz", location="SAL Hall", description="Desserts and sweet treats near the dormitories.", latitude=10.64997, longitude=-61.39553, category="Halls of Residence", phone="Unknown"),
            Restaurant(name="Pita Pit", location="JFK Quadrangle", description="Wraps, paninis and pita pockets with fresh fillings. A healthy and tasty choice.", latitude=10.63893, longitude=-61.39870, category="JFK", phone="+1868-285-7482"),
            Restaurant(name="Rituals Coffee House", location="JFK Quadrangle", description="Premium coffee, teas, cold drinks and food items. The campus coffee hotspot.", latitude=10.63888, longitude=-61.39869, category="JFK", phone="+1868-225-5125"),
            Restaurant(name="Linda's Bakery", location="JFK Quadrangle", description="Freshly baked pastries, salads, breads and natural juices. A campus institution.", latitude=10.63865, longitude=-61.39858, category="JFK", phone="+1868-280-2350"),
            Restaurant(name="The Gourmet Pot", location="Dudley Huggins Building", description="Contemporary cuisine with diverse menu options. Elevated campus dining.", latitude=10.64507, longitude=-61.40038, category="Dudley Huggins", phone="+1868-610-9768"),
            Restaurant(name="KFC", location="JFK Food Court", description="Fries, chicken and combos from the globally loved brand.", latitude=10.63910, longitude=-61.39821, category="JFK Food Court", phone="+1868-225-4532"),
            Restaurant(name="Subway", location="JFK Food Court", description="Sub sandwiches made to order with fresh bread, proteins and toppings.", latitude=10.63916, longitude=-61.39832, category="JFK Food Court", phone="+1868-226-7874"),
            Restaurant(name="Benny's BBQ & Burgers", location="Car Park next to Staff Social Club", description="Burgers and BBQ done right. Smoky flavours with generous portions.", latitude=10.64588, longitude=-61.40231, category="Staff Social Club Area", phone="+1868-704-0400"),
            Restaurant(name="Boba and Brew Café", location="Republic Bank Plaza – UWI", description="Pastries, smoothies and ice cream. A trendy café spot on campus.", latitude=10.64567, longitude=-61.40109, category="Republic Bank Plaza", phone="+1868-615-8222"),
            Restaurant(name="Al Mohammed on the Link Up", location="Teaching and Learning Centre", description="Burgers and sandwiches served near the Teaching and Learning Centre.", latitude=10.64153, longitude=-61.39671, category="Teaching & Learning Centre", phone="Unknown"),
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
            MenuItem(name="Pelau", price=40.0, description="Rice cooked with pigeon peas, chicken and coconut milk", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Stewed Chicken & Rice", price=45.0, description="Slow-stewed chicken with white rice", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Macaroni Pie", price=30.0, description="Baked macaroni with seasoned minced beef and cheese", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Callaloo & Crab", price=60.0, description="Dasheen bush cooked with blue crab, served with provisions", is_available=True, restaurant_id=pid("Dee & Vees")),
            MenuItem(name="Sorrel Drink", price=12.0, description="Refreshing chilled sorrel beverage", is_available=True, restaurant_id=pid("Dee & Vees")),
            # La Bloom Café
            MenuItem(name="Cappuccino", price=25.0, description="Espresso with steamed milk foam", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Iced Latte", price=28.0, description="Chilled espresso with milk over ice", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Chicken Sandwich", price=40.0, description="Grilled chicken on toasted bread with fresh lettuce and tomato", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Cheese Croissant", price=20.0, description="Buttery croissant filled with melted cheddar cheese", is_available=True, restaurant_id=pid("La Bloom Café")),
            MenuItem(name="Fresh Orange Juice", price=18.0, description="Freshly squeezed orange juice", is_available=True, restaurant_id=pid("La Bloom Café")),
            #Vending Machine (Drinks)            
            MenuItem(name="Coca-Cola", price=10.0, description="Sweet, fizzy, caramel-flavoured soda", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Sprite", price=10.0, description="Light, citrusy soda with no caffeine", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Fanta", price=10.0, description="Sweet and fruity", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Mountain Dew", price=12.0, description="High-energy citrus soda with caffeine", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Bottled Water", price=5.0, description="Plain, still water", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Juice", price=8.0, description="Sweet fruit juice in small bottles or boxes", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Redbull", price=20.0, description="High caffeine drinks designed to boost energy. Slightly bitter with a sweet aftertaste.", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Gatorade", price=18.0, description="Electrolyte drinks for hydration. Light, slightly salty-sweet taste.", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Iced Coffee", price=20.0, description="Cold, sweetened coffee drink. Creamy and caffeinated.", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Iced Tea", price=18.0, description="Light tea flavour with fruit sweetness", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Protein Drinks", price=25.0, description="Thick, milk-based drinks with added protein", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            MenuItem(name="Kombucha", price=30.0, description="Slightly fizzy fermented tea", is_available=True, restaurant_id=pid("Vending Machine (Drinks)")),
            #Campus Campus Mini Mart
            MenuItem(name="Pringles (Original)", price=25.0, description="Classic original flavour Pringles potato crisps", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Cheetos", price=18.0, description="Crunchy cheesy corn puffs", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Crix Crackers", price=10.0, description="Iconic Trinidadian cream crackers", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Shirley Biscuits", price=8.0, description="Classic sweet Trinidadian biscuits", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Chips Ahoy", price=18.0, description="Classic chocolate chip cookies in a snack pack", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Solo (Soft Drink)", price=12.0, description="Chilled Solo soft drink in assorted Trinidadian flavours — orange, grape or cream soda", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Coconut Water (can)", price=15.0, description="Natural coconut water in a can — refreshing and hydrating", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Milo (can)", price=18.0, description="Chilled canned Milo chocolate milk drink", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Fresh Start Juice", price=10.0, description="Assorted fruit juices in various flavours", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            MenuItem(name="Bottled Water", price=8.0, description="Chilled 500ml bottled water — refreshing and essential for campus life", is_available=True, restaurant_id=pid("Campus Mini Mart")),
            # Just Juiced
            MenuItem(name="Lime Juice", price=12.0, description="Freshly squeezed lime juice, sweetened to taste", is_available=True, restaurant_id=pid("Just Juiced")),
            MenuItem(name="Passion Fruit Juice", price=15.0, description="Fresh passion fruit blended with water and sugar", is_available=True, restaurant_id=pid("Just Juiced")),
            MenuItem(name="Watermelon Juice", price=14.0, description="Cold blended watermelon juice", is_available=True, restaurant_id=pid("Just Juiced")),
            MenuItem(name="Mango Juice", price=15.0, description="Thick blended mango juice from local mangoes", is_available=True, restaurant_id=pid("Just Juiced")),
            MenuItem(name="Mixed Fruit Punch", price=16.0, description="Blend of seasonal tropical fruits", is_available=True, restaurant_id=pid("Just Juiced")),
            # Oriental Cuisine
            MenuItem(name="Fried Rice", price=40.0, description="Classic Chinese-style fried rice with egg and vegetables", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Chow Mein", price=45.0, description="Stir-fried noodles with mixed vegetables and soy sauce", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Sweet & Sour Chicken", price=55.0, description="Crispy chicken tossed in tangy sweet and sour sauce", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Wonton Soup", price=30.0, description="Light broth with pork dumplings and scallions", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            MenuItem(name="Spring Rolls (2 pcs)", price=20.0, description="Crispy vegetable spring rolls with dipping sauce", is_available=True, restaurant_id=pid("Oriental Cuisine")),
            # Panks Sweet Sauce Doubles
            MenuItem(name="Doubles", price=8.0, description="Two bara with curried channa — the classic Trini breakfast", is_available=True, restaurant_id=pid("Panks Sweet Sauce Doubles")),
            MenuItem(name="Aloo Pie", price=10.0, description="Fried dough filled with curried potato and seasoning", is_available=True, restaurant_id=pid("Panks Sweet Sauce Doubles")),
            MenuItem(name="Pholourie", price=10.0, description="Fried split peas fritters served with tamarind sauce", is_available=True, restaurant_id=pid("Panks Sweet Sauce Doubles")),
            # Juman's Roti Shop
            MenuItem(name="Dhalpuri with Chicken Curry", price=45.0, description="Layered dhalpuri roti filled with chicken curry", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Dhalpuri with Goat Curry", price=50.0, description="Dhalpuri roti with slow-cooked curried goat", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Paratha with Aloo", price=35.0, description="Flaky paratha roti with curried potato", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Bus-Up-Shot with Shrimp", price=55.0, description="Torn paratha roti with curried shrimp filling", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            MenuItem(name="Mango Chow", price=15.0, description="Green mango with pepper, garlic and chadon beni", is_available=True, restaurant_id=pid("Juman's Roti Shop")),
            # Veg Out
            MenuItem(name="Spinach Pie", price=15.0, description="Pastry filled with seasoned spinach", is_available=True, restaurant_id=pid("Veg Out")),
            MenuItem(name="Vegetable Patty", price=14.0, description="Golden patty filled with mixed vegetables", is_available=True, restaurant_id=pid("Veg Out")),
            MenuItem(name="Apple Juice", price=12.0, description="Chilled apple juice", is_available=True, restaurant_id=pid("Veg Out")),
            MenuItem(name="Cheese Straw", price=8.0, description="Crunchy baked cheese straws", is_available=True, restaurant_id=pid("Veg Out")),
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
            # Linda's Bakery
            MenuItem(name="White Bread Loaf", price=18.0, description="Soft, everyday sandwich bread.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Whole Wheat Bread", price=20.0, description="Denser bread made with whole grains. More filling and has a nutty, slightly earthy flavour", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Hops Bread", price=18.0, description="Small, round buns. Soft inside with a slightly crispy crust.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Sausage Rolls", price=12.0, description="Savory pastry filled with seasoned meat. Soft inside with a crispy golden crust outside.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Currant Rolls", price=12.0, description="Sweet bread-like pastry with dried currants. Slightly sweet and soft.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Meat Pies", price=16.0, description="Pastry filled with seasoned meat and gravy. Hearty and flavorful, usually slightly spicy depending on filling.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Cheese Pies", price=15.0, description="Vegetarian option with cheese baked inside flaky pastry.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Cake Slices", price=18.0, description="Soft sponge cake served in slices. Black cake is rich and fruity, chocolate is sweet and moist.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Cupcakes", price=10.0, description="Mini cakes topped with icing. Soft sponge base with sweet frosting on top — often chocolate or vanilla.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            MenuItem(name="Coffee/Tea", price=12.0, description="Hot beverages — usually simple, black or with milk and sugar added.", is_available=True, restaurant_id=pid("Linda's Bakery")),
            # The Gourmet Pot
            MenuItem(name="Grilled Salmon", price=85.0, description="Pan-seared salmon fillet with herb butter and seasonal vegetables", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Pasta Primavera", price=60.0, description="Fettuccine with sautéed seasonal vegetables in garlic olive oil", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Beef Burger", price=65.0, description="Hand-pressed beef patty with gourmet toppings on a brioche bun", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Caesar Salad", price=40.0, description="Romaine lettuce, croutons, parmesan and Caesar dressing", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            MenuItem(name="Sparkling Water", price=15.0, description="Chilled sparkling water", is_available=True, restaurant_id=pid("The Gourmet Pot")),
            # KFC
            MenuItem(name="2-Piece Meal", price=39.95, description="Two pieces of Original Recipe chicken with fries and a drink", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Zinger Burger Meal", price=39.95, description="Spicy Zinger chicken burger with fries and a drink", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Popcorn Chicken", price=27.0, description="Bite-sized crispy chicken pieces", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Coleslaw", price=12.0, description="KFC signature creamy coleslaw", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Soft Drink (Medium)", price=18.0, description="Pepsi, 7-Up or Mirinda — medium size", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Krunch Twist", price=29.95, description="Crispy KFC chicken fillet twisted in a soft tortilla wrap with fresh lettuce and creamy mayo", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Krunch Twist Combo", price=39.95, description="Krunch Twist wrap paired with a side of fries and a medium drink for the full meal experience", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Mac & Cheese", price=12.0, description="Creamy KFC macaroni and cheese in a regular portion", is_available=True, restaurant_id=pid("KFC")),
            MenuItem(name="Mash & Gravy", price=12.0, description="Smooth mashed potatoes topped with rich KFC gravy", is_available=True, restaurant_id=pid("KFC")),
            # Subway
            MenuItem(name="Italian BMT (6-inch)", price=36.0, description="Pepperoni, salami and ham on Italian bread with your choice of toppings", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Chicken Teriyaki (Footlong)", price=59.0, description="Teriyaki chicken strip sub on honey oat bread", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Veggie Delite (6-inch)", price=27.0, description="Fresh garden vegetables on your choice of bread", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Cookies (3 pack)", price=15.0, description="Freshly baked Subway cookies — chocolate chip or macadamia nut", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Philly Cheese Steak (6-inch)", price=45.0, description="Steak, green peppers, onions, double American cheese and mayo on toasted bread", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Philly Cheese Steak (Footlong)", price=75.0, description="Steak, green peppers, onions, double American cheese and mayo on toasted footlong bread", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Meatball Marinara (6-inch)", price=44.0, description="Hearty meatballs smothered in rich marinara sauce on freshly baked bread, topped with your choice of veggies and cheese", is_available=True, restaurant_id=pid("Subway")),
            MenuItem(name="Meatball Marinara (Footlong)", price=69.0, description="Hearty meatballs smothered in rich marinara sauce on freshly baked footlong bread, topped with your choice of veggies and cheese", is_available=True, restaurant_id=pid("Subway")),
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
        ]

        for item in items:
            db.add(item)
        db.commit()
        
        print("Database Initialized!")

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