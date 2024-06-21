import pandas as pd
import numpy as np
from faker import Faker
import sys


def generate_data(num_orders=1000, num_products=256):
    fake = Faker()

    # Defining the range of dates for the orders
    start_date = pd.to_datetime('2021-01-01')
    end_date = pd.to_datetime('2023-01-01')

    # Generating a list of unique products
    unique_products = []
    for _ in range(num_products):
        product_name = fake.word().capitalize() + ' ' + fake.word().capitalize()
        product_id = np.random.randint(1000, 2000)  # Product IDs between 1000 and 1999
        product_price = round(np.random.uniform(10, 500), 2)  # Prices between $10 and $500
        unique_products.append((product_id, product_name, product_price))

    # Creating random data for each column based on the schema
    order_ids = range(1, num_orders + 1)
    customer_ids = np.random.randint(1, 300, num_orders)  # Assuming 300 unique customers
    order_dates = pd.to_datetime(np.random.choice(pd.date_range(start_date, end_date), num_orders))
    quantities = np.random.randint(1, 10, num_orders)  # Quantity between 1 and 9

    # Selecting a random product for each order by index
    indices = np.random.randint(0, num_products, num_orders)
    product_ids = [unique_products[i][0] for i in indices]
    product_names = [unique_products[i][1] for i in indices]
    product_prices = [unique_products[i][2] for i in indices]

    # Creating DataFrame
    orders = pd.DataFrame({
        'order_id': order_ids,
        'customer_id': customer_ids,
        'order_date': order_dates,
        'product_id': product_ids,
        'product_name': product_names,
        'product_price': product_prices,
        'quantity': quantities
    })

    # Saving the DataFrame to a CSV file
    orders.to_csv('data/orders.csv', index=False)
    print("Generated 'data/orders.csv' with {} entries.".format(num_orders))


if __name__ == '__main__':
    num_orders = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    generate_data(num_orders=num_orders, num_products=256)
