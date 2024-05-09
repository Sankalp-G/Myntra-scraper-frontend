import streamlit as st
import requests

st.markdown('<h1><span style="color: #33D4FF;">🌐Scrap</span><span style="color: #3965FC;">Nexus</span></h1>', unsafe_allow_html=True)
subheader_color = "#ADD8E6"
st.markdown(f'<h2 style="color: {subheader_color};">Graph your way to clarity</h2>', unsafe_allow_html=True)


#https://lottiefiles.com/animations/rocket-in-space-transparent-background-T0pLH42g8D?from=search
st.markdown("---")
description = """
Our project is a web scraper designed specifically for Myntra products. With the aim of providing insightful analytics, we meticulously extract data on various product attributes, such as ratings, prices, and reviews, from Myntra's extensive product catalog. Leveraging cutting-edge web scraping techniques, our scraper gathers real-time information on product performance, user feedback, and market trends.

Once the data is collected, our platform transforms it into actionable insights through dynamic visualizations. Users can explore a range of graph types. These intuitive graphs offer a comprehensive view of product popularity, customer satisfaction, and potential areas for improvement.

Whether it's monitoring the performance of a specific product, identifying emerging trends in a particular category, or understanding customer sentiment, our web scraper and visualization tool empower businesses and individuals alike to make data-driven decisions with confidence.
"""

# Display the description using markdown with a smaller font size
st.markdown(description, unsafe_allow_html=True)
st.markdown("To visit [Myntra](https://www.myntra.com)")
st.markdown("---")
st.caption("Contact Us: +91 12345 67890")
