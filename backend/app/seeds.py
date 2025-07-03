import asyncio
from datetime import datetime, timedelta

from faker import Faker
from sqlmodel import Session

from app.core.security import get_password_hash
from app.db.session import engine
from app.models.models import User, Category, Product, Review, Order, OrderItem


fake = Faker()


def create_users(session):
    print("Creating users...")
    # Admin user
    admin = User(
        email="admin@techstore.com",
        username="admin",
        full_name="Admin User",
        is_active=True,
        is_admin=True,
        hashed_password=get_password_hash("admin123")
    )
    session.add(admin)
    
    # Regular users
    for _ in range(5):
        name = fake.name()
        username = fake.user_name()
        email = fake.email()
        
        user = User(
            email=email,
            username=username,
            full_name=name,
            is_active=True,
            is_admin=False,
            hashed_password=get_password_hash("password123")
        )
        session.add(user)
    
    session.commit()
    return session.query(User).all()


def create_categories(session):
    print("Creating categories...")
    categories = [
        Category(name="Smartphones", description="Mobile phones and accessories"),
        Category(name="Laptops", description="Notebooks, laptops and accessories"),
        Category(name="Tablets", description="Tablets and e-readers"),
        Category(name="Audio", description="Headphones, speakers and audio equipment"),
        Category(name="Wearables", description="Smartwatches and fitness trackers"),
        Category(name="Components", description="PC components and hardware"),
        Category(name="Gaming", description="Gaming consoles and accessories"),
    ]
    
    for category in categories:
        session.add(category)
    
    session.commit()
    return session.query(Category).all()


def create_products(session, users, categories):
    print("Creating products...")
    products = []
    
    # Sample product data for each category
    products_data = {
        "Smartphones": [
            {"name": "iPhone 15 Pro", "price": 999.99, "is_used": False},
            {"name": "Samsung Galaxy S23", "price": 899.99, "is_used": False},
            {"name": "Google Pixel 8", "price": 799.99, "is_used": False},
            {"name": "Xiaomi 14", "price": 599.99, "is_used": False},
            {"name": "iPhone 14", "price": 699.99, "is_used": True},
        ],
        "Laptops": [
            {"name": "MacBook Pro M3", "price": 1499.99, "is_used": False},
            {"name": "Dell XPS 13", "price": 1299.99, "is_used": False},
            {"name": "Lenovo ThinkPad X1", "price": 1199.99, "is_used": False},
            {"name": "HP Spectre x360", "price": 1099.99, "is_used": False},
            {"name": "Asus ROG Zephyrus", "price": 1799.99, "is_used": True},
        ],
        "Tablets": [
            {"name": "iPad Pro 12.9", "price": 999.99, "is_used": False},
            {"name": "Samsung Galaxy Tab S9", "price": 899.99, "is_used": False},
            {"name": "Microsoft Surface Pro", "price": 999.99, "is_used": False},
            {"name": "Amazon Fire HD 10", "price": 149.99, "is_used": True},
        ],
        "Audio": [
            {"name": "Sony WH-1000XM5", "price": 349.99, "is_used": False},
            {"name": "Apple AirPods Pro", "price": 249.99, "is_used": False},
            {"name": "Bose QuietComfort Ultra", "price": 329.99, "is_used": False},
            {"name": "JBL Flip 6", "price": 129.99, "is_used": True},
        ],
        "Wearables": [
            {"name": "Apple Watch Series 9", "price": 399.99, "is_used": False},
            {"name": "Samsung Galaxy Watch 6", "price": 299.99, "is_used": False},
            {"name": "Fitbit Sense 2", "price": 249.99, "is_used": False},
            {"name": "Garmin Forerunner 955", "price": 499.99, "is_used": True},
        ],
        "Components": [
            {"name": "NVIDIA RTX 4080", "price": 999.99, "is_used": False},
            {"name": "AMD Ryzen 9 7950X", "price": 599.99, "is_used": False},
            {"name": "Samsung 990 PRO SSD 2TB", "price": 249.99, "is_used": False},
            {"name": "G.Skill Trident Z5 RAM 32GB", "price": 199.99, "is_used": True},
        ],
        "Gaming": [
            {"name": "PlayStation 5", "price": 499.99, "is_used": False},
            {"name": "Xbox Series X", "price": 499.99, "is_used": False},
            {"name": "Nintendo Switch OLED", "price": 349.99, "is_used": False},
            {"name": "Steam Deck", "price": 399.99, "is_used": True},
        ],
    }
    
    for category in categories:
        category_products = products_data.get(category.name, [])
        for product_data in category_products:
            seller = fake.random_element(users)
            
            product = Product(
                name=product_data["name"],
                description=fake.paragraph(nb_sentences=3),
                price=product_data["price"],
                stock=fake.random_int(min=1, max=100),
                is_used=product_data["is_used"],
                is_active=True,
                image_url=None,  # Would need actual images in a real app
                created_at=fake.date_time_between(start_date="-1y", end_date="now"),
                seller_id=seller.id,
                category_id=category.id
            )
            
            session.add(product)
            products.append(product)
    
    session.commit()
    return products


def create_reviews(session, users, products):
    print("Creating reviews...")
    reviews = []
    
    for product in products:
        # Generate 0-5 reviews per product
        for _ in range(fake.random_int(min=0, max=5)):
            # Skip the seller - can't review their own product
            eligible_users = [user for user in users if user.id != product.seller_id]
            if not eligible_users:
                continue
            
            reviewer = fake.random_element(eligible_users)
            
            review = Review(
                rating=fake.random_int(min=1, max=5),
                comment=fake.paragraph(nb_sentences=2) if fake.boolean(chance_of_getting_true=70) else None,
                created_at=fake.date_time_between(start_date="-6m", end_date="now"),
                user_id=reviewer.id,
                product_id=product.id
            )
            
            session.add(review)
            reviews.append(review)
    
    session.commit()
    return reviews


def create_orders(session, users, products):
    print("Creating orders...")
    orders = []
    
    for user in users:
        # Generate 0-3 orders per user
        for _ in range(fake.random_int(min=0, max=3)):
            # Select 1-5 random products for this order
            order_products = fake.random_elements(
                elements=products,
                length=fake.random_int(min=1, max=5),
                unique=True
            )
            
            total_amount = 0
            
            order = Order(
                total_amount=0,  # Will be calculated based on items
                status=fake.random_element(["pending", "paid", "shipped", "delivered"]),
                created_at=fake.date_time_between(start_date="-1y", end_date="now"),
                user_id=user.id
            )
            
            session.add(order)
            session.flush()  # To get the order ID
            
            # Add order items
            for product in order_products:
                quantity = fake.random_int(min=1, max=3)
                price = product.price
                total_amount += price * quantity
                
                order_item = OrderItem(
                    quantity=quantity,
                    price=price,
                    order_id=order.id,
                    product_id=product.id
                )
                
                session.add(order_item)
            
            order.total_amount = total_amount
            orders.append(order)
    
    session.commit()
    return orders


def main():
    with Session(engine) as session:
        users = create_users(session)
        categories = create_categories(session)
        products = create_products(session, users, categories)
        reviews = create_reviews(session, users, products)
        orders = create_orders(session, users, products)
        
        print(f"Created {len(users)} users")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(products)} products")
        print(f"Created {len(reviews)} reviews")
        print(f"Created {len(orders)} orders")
        
        print("\nSeeding completed successfully!")
        print("\nYou can login with the following admin credentials:")
        print("Email: admin@techstore.com")
        print("Password: admin123")


if __name__ == "__main__":
    main()
