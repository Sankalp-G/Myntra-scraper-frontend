import psycopg2
from psycopg2.extras import RealDictCursor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

cur.execute("select distinct sub_category from products")
sub_categories = cur.fetchall()

plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")

def get_sub_cat(row):
    return row["sub_category"]

sub_categories = list(map(get_sub_cat, sub_categories))
import streamlit as st

st.title("Home Page")
st.markdown("We're dedicated to providing you with powerful insights into product pricing and trends. Our home page features major graphs that offer valuable perspectives on the market landscape: ")
st.markdown("---")

@st.cache_data
def median_price():
    st.markdown("## Median Price per Sub Category")
    sql=f"SELECT distinct name, mrp, sub_category FROM products"
    table = pd.read_sql_query(sql, connection)
    median = table.groupby("sub_category")["mrp"].median()

    st.bar_chart(median)

median_price()

st.markdown("---")

st.markdown("## Product Median price per Sub Category")

@st.cache_data
def bubble_chart():
    class BubbleChart:
        def __init__(self, area, bubble_spacing=0):
            """
            Setup for bubble collapse.

            Parameters
            ----------
            area : array-like
                Area of the bubbles.
            bubble_spacing : float, default: 0
                Minimal spacing between bubbles after collapsing.

            Notes
            -----
            If "area" is sorted, the results might look weird.
            """
            area = np.asarray(area)
            r = np.sqrt(area / np.pi)

            self.bubble_spacing = bubble_spacing
            self.bubbles = np.ones((len(area), 4))
            self.bubbles[:, 2] = r
            self.bubbles[:, 3] = area
            self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
            self.step_dist = self.maxstep / 2

            # calculate initial grid layout for bubbles
            length = np.ceil(np.sqrt(len(self.bubbles)))
            grid = np.arange(length) * self.maxstep
            gx, gy = np.meshgrid(grid, grid)
            self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
            self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

            self.com = self.center_of_mass()

        def center_of_mass(self):
            return np.average(
                self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
            )

        def center_distance(self, bubble, bubbles):
            return np.hypot(bubble[0] - bubbles[:, 0],
                            bubble[1] - bubbles[:, 1])

        def outline_distance(self, bubble, bubbles):
            center_distance = self.center_distance(bubble, bubbles)
            return center_distance - bubble[2] - \
                bubbles[:, 2] - self.bubble_spacing

        def check_collisions(self, bubble, bubbles):
            distance = self.outline_distance(bubble, bubbles)
            return len(distance[distance < 0])

        def collides_with(self, bubble, bubbles):
            distance = self.outline_distance(bubble, bubbles)
            return np.argmin(distance, keepdims=True)

        def collapse(self, n_iterations=50):
            """
            Move bubbles to the center of mass.

            Parameters
            ----------
            n_iterations : int, default: 50
                Number of moves to perform.
            """
            for _i in range(n_iterations):
                moves = 0
                for i in range(len(self.bubbles)):
                    rest_bub = np.delete(self.bubbles, i, 0)
                    # try to move directly towards the center of mass
                    # direction vector from bubble to the center of mass
                    dir_vec = self.com - self.bubbles[i, :2]

                    # shorten direction vector to have length of 1
                    dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                    # calculate new bubble position
                    new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                    new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                    # check whether new bubble collides with other bubbles
                    if not self.check_collisions(new_bubble, rest_bub):
                        self.bubbles[i, :] = new_bubble
                        self.com = self.center_of_mass()
                        moves += 1
                    else:
                        # try to move around a bubble that you collide with
                        # find colliding bubble
                        for colliding in self.collides_with(new_bubble, rest_bub):
                            # calculate direction vector
                            dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                            dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                            # calculate orthogonal vector
                            orth = np.array([dir_vec[1], -dir_vec[0]])
                            # test which direction to go
                            new_point1 = (self.bubbles[i, :2] + orth *
                                          self.step_dist)
                            new_point2 = (self.bubbles[i, :2] - orth *
                                          self.step_dist)
                            dist1 = self.center_distance(
                                self.com, np.array([new_point1]))
                            dist2 = self.center_distance(
                                self.com, np.array([new_point2]))
                            new_point = new_point1 if dist1 < dist2 else new_point2
                            new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                            if not self.check_collisions(new_bubble, rest_bub):
                                self.bubbles[i, :] = new_bubble
                                self.com = self.center_of_mass()

                if moves / len(self.bubbles) < 0.1:
                    self.step_dist = self.step_dist / 2

        def plot(self, ax, labels, colors):
            """
            Draw the bubble plot.

            Parameters
            ----------
            ax : matplotlib.axes.Axes
            labels : list
                Labels of the bubbles.
            colors : list
                Colors of the bubbles.
            """
            for i in range(len(self.bubbles)):
                circ = plt.Circle(
                    self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
                ax.add_patch(circ)
                ax.text(*self.bubbles[i, :2], labels[i],
                        horizontalalignment='center', verticalalignment='center')

    sql=f"SELECT distinct name, mrp, sub_category FROM products"
    table = pd.read_sql_query(sql, connection)
    median = table.groupby("sub_category")["mrp"].median()

    bubble_chart = BubbleChart(area=median, bubble_spacing=0.1)

    bubble_chart.collapse()

    colors = plt.cm.tab10(np.linspace(0, 1, len(median)))

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"), figsize=(15, 12))

    bubble_chart.plot(
        ax, median.keys(), colors)
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()

    st.write(fig)

bubble_chart()

st.markdown("---")

@st.cache_data
def product_number():
    st.markdown("## Number of Products per Sub Category")
    sql = f"SELECT sub_category, count(name) as count FROM products GROUP BY sub_category"
    table = pd.read_sql_query(sql, connection)
    table = table.set_index("sub_category")
    st.bar_chart(table)

product_number()
st.markdown("---")

@st.cache_data
def median_rating():
    st.markdown("## Median Rating per Sub Category")
    sql=f"SELECT distinct name, rating, sub_category FROM products"
    table = pd.read_sql_query(sql, connection)
    median = table.groupby("sub_category")["rating"].median()

    st.bar_chart(median)
    st.markdown("---")

median_rating()


