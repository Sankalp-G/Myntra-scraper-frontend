#url shortener apis 

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as sl
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import altair as alt
import os
from dotenv import load_dotenv

load_dotenv()

hostname = os.getenv('DB_HOST')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)

cur = connection.cursor(cursor_factory=RealDictCursor)

cur.execute("select DISTINCT sub_category sub_category from products")
sub_categories = cur.fetchall()
def get_sub_cat(row):
    return row["sub_category"]
sub_categories = list(map(get_sub_cat, sub_categories))
sub_categories.sort()

x=np.linspace(0,10,100)
bar_x=np.array([1,2,3,4,5])

sl.title("Sub Category Breakdown")
select=sl.selectbox(" Select a type of category", options=sub_categories)

column_config = {
    "name": "Product Name",
    "brand": "Brand",
    "best_price": "Best Price",
    "mrp": "MRP",
    "coupon_code": "Coupon Code",
    "url": sl.column_config.LinkColumn("URL"),
    "rating": "Rating",
    "rating_count": "Rating Count",
    "discount_percentage": "Discount Percentage"
}

sl.markdown("---")
sl.markdown("## Product vs Best Price")

@sl.cache_data
def visualize_top_products_horizontal(sub_category):
    # Construct SQL query
    sql = f"SELECT DISTINCT * FROM products WHERE sub_category = '{sub_category}' AND scrape_id = 11  ORDER BY best_price ASC LIMIT 10"
    # Read data from database into DataFrame
    table = pd.read_sql_query(sql, connection)

    chart = alt.Chart(table).mark_bar().encode(
        x=alt.X("best_price:Q", title="Best Price", sort=None),
        y=alt.Y("name:N", title="Product Name", sort=None),
        color="name:N",
        tooltip=["name", "best_price"],
    ).properties(
        title=f'Top 10 Products in {sub_category} Subcategory'
    ).interactive()

    sl.altair_chart(chart, use_container_width=True)

    with sl.expander("View Table"):
         sl.dataframe(table, column_config=column_config, hide_index=True)


# Example usage
visualize_top_products_horizontal(select)

sl.markdown("---")
sl.markdown("## Top 10 Products")

@sl.cache_data
def visualize_top_products_bar_of_pie(sub_category):
    # Construct SQL query
    sql = f"SELECT DISTINCT name, brand, best_price, mrp, coupon_code, concat('https://myntra.com/', href) as url, rating, rating_count FROM products WHERE sub_category = '{sub_category}' ORDER BY best_price DESC LIMIT 10"
    
    # Read data from database into DataFrame
    table = pd.read_sql_query(sql, connection)
    
    chart = alt.Chart(table).mark_arc().encode(
        theta="best_price:Q",
        color="name:N",
        tooltip=["name", "best_price"]
    ).properties(
        title=f'Top 10 Products in {sub_category} Subcategory'
    ).interactive()

    sl.altair_chart(chart, use_container_width=True)
    with sl.expander("View Table"):
         sl.dataframe(table, column_config=column_config, hide_index=True)

# Example usage
visualize_top_products_bar_of_pie(select)

sl.markdown("---")
sl.markdown("## Product vs Rating")
plt.style.use('_mpl-gallery')

@sl.cache_data
def plot_top_product_ratings(sub_category):
    # Construct SQL query
    sql = f"SELECT DISTINCT name, brand, best_price, mrp, coupon_code, concat('https://myntra.com/', href) as url, rating, rating_count FROM products WHERE sub_category = '{sub_category}' ORDER BY rating DESC LIMIT 10"
    
    # Read data from database into DataFrame
    table = pd.read_sql_query(sql, connection)

    sl.bar_chart(table, x='name', y='rating', color='name', use_container_width=True, height=500)

    with sl.expander("View Table"):
         sl.dataframe(table, column_config=column_config, hide_index=True)

# Example usage
plot_top_product_ratings(select)

sl.markdown("---")
sl.markdown("## Discount vs Product")

@sl.cache_data
def plot_top_product_discounts(sub_category):
    # Construct SQL query
    sql = f"SELECT DISTINCT name, brand, best_price, mrp, discounted_price, coupon_code, concat('https://myntra.com/', href) as url, rating, rating_count FROM products WHERE sub_category = '{sub_category}' ORDER BY discounted_price DESC LIMIT 10"
    
    # Read data from database into DataFrame
    table = pd.read_sql_query(sql, connection)

    sl.bar_chart(table, x='name', y='discounted_price', color='name', use_container_width=True, height=500)

    with sl.expander("View Table"):
         sl.dataframe(table, column_config=column_config, hide_index=True)

# Example usage
plot_top_product_discounts(select)

sl.markdown("---")
sl.markdown("## Rating: ")

@sl.cache_data
def compare_top_10_items_errorbar(sub_category):
    # Construct SQL query
    sql = f"SELECT DISTINCT name, brand, best_price, mrp, coupon_code, concat('https://myntra.com/', href) as url, rating, rating_count FROM products WHERE sub_category = '{sub_category}' ORDER BY rating DESC LIMIT 10"
    
    # Read data from database into DataFrame
    table = pd.read_sql_query(sql, connection)

    sl.bar_chart(table, x='rating', y='name', color='name', use_container_width=True, height=500)

    with sl.expander("View Table"):
         sl.dataframe(table, column_config=column_config, hide_index=True)

# Example usage
compare_top_10_items_errorbar(select)

sl.markdown("---")
sl.markdown("## Product vs Discount Percentage")

@sl.cache_data
def plot_top_subcategory_discounts(sub_category):
    # Construct SQL query
    sql = f"SELECT DISTINCT name, brand, best_price, mrp, discount_percentage, coupon_code, concat('https://myntra.com/', href) as url, rating, rating_count FROM products WHERE sub_category = '{sub_category}' ORDER BY discount_percentage DESC LIMIT 10"
    
    # Read data from database into DataFrame
    table = pd.read_sql_query(sql, connection)

    sl.bar_chart(table, x='discount_percentage', y='name', color='name', use_container_width=True, height=500)

    with sl.expander("View Table"):
         sl.dataframe(table, column_config=column_config, hide_index=True)

# Example usage
plot_top_subcategory_discounts(select)
