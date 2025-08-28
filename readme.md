This is my first CRUD with Python using FastAPI, SQLAlchemy and Pydantic.

The project is oriented to a shopping business, such as a Butchery, Fish Market or Fruit Market, where the prices are set per kilo.

- Product
    - Price (The price is oriented to be per kilogram)
    - Description
      
- Order Item
    - Price
    - Weight

- Order
    - Date
    - Total

- Client
    - Name
    - Direction
    - Email
    - Phone Number
 
In this case, the client doesn't have any method of authentication. That's because the goal of this project is to integrate with a Telegram or WhatsApp bot, so the client can order from there.
