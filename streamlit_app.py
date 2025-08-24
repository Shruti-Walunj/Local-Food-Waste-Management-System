
import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("food_wastage_management.db")

# SQL Queries

queries = {
    "Providers & Receivers Per City": """
SELECT p.City, 
       COUNT(DISTINCT p.Provider_ID) AS total_providers,
       COUNT(DISTINCT r.Receiver_ID) AS total_receivers
FROM providers p
LEFT JOIN receivers r ON p.City = r.City
GROUP BY p.City
""",

    "Top Provider Type By Listings": """
SELECT Provider_Type, COUNT(*) AS total_items
FROM food_listings
GROUP BY Provider_Type
ORDER BY total_items DESC
LIMIT 5
""",

    "Top Receivers By Claims": """
SELECT r.Name, COUNT(c.Claim_ID) AS total_claims
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Name
ORDER BY total_claims DESC
LIMIT 5
""",

    "Total Quantity Of Food Available": """
SELECT SUM(Quantity) AS total_quantity
FROM food_listings
""",

    "City With Most Food Listings": """
SELECT Location, COUNT(*) AS total_listings
FROM food_listings
GROUP BY Location
ORDER BY total_listings DESC
LIMIT 5
""",

    "Most Common Food Types": """
SELECT Food_Type, COUNT(*) AS count_type
FROM food_listings
GROUP BY Food_Type
ORDER BY count_type DESC
LIMIT 5
""",

    "Claims Per Food Item": """
SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims
FROM food_listings f
JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Food_Name
ORDER BY total_claims DESC
LIMIT 5
""",

    "Provider With Most Successful Claims": """
SELECT p.Name, COUNT(c.Claim_ID) AS successful_claims
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
JOIN claims c ON f.Food_ID = c.Food_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY successful_claims DESC
LIMIT 5
""",

    "Claims Percentage By Status": """
SELECT Status,
       ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims)), 2) AS percentage
FROM claims
GROUP BY Status
""",

    "Average Quantity Claimed Per Receiver": """
SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS avg_quantity_claimed
FROM receivers r
JOIN claims c ON r.Receiver_ID = c.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Name
LIMIT 5
""",

    "Most Claimed Meal Type": """
SELECT Meal_Type, COUNT(*) AS total_claims
FROM food_listings f
JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY Meal_Type
ORDER BY total_claims DESC
LIMIT 5
""",

    "Total Quantity Donated By Each Provider": """
SELECT p.Name, SUM(f.Quantity) AS total_quantity_donated
FROM providers p
JOIN food_listings f ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY total_quantity_donated DESC
LIMIT 5
""",

    "Top Cities By Total Claims": """
SELECT f.Location, COUNT(c.Claim_ID) AS total_claims
FROM food_listings f
JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Location
ORDER BY total_claims DESC
LIMIT 5
""",

    "Listings Per Provider Type Per City": """
SELECT Location, Provider_Type, COUNT(*) AS total_listings
FROM food_listings
GROUP BY Location, Provider_Type
ORDER BY total_listings DESC
LIMIT 10
"""
}

# Streamlit UI
st.set_page_config(page_title="Food Wastage SQL Insights", layout="wide")
st.title("🍽️ Local Food Wastage Management Sytem")

# Sidebar for query selection
query_choice = st.sidebar.selectbox("📌 Choose a query:", list(queries.keys()))

# Run query
df = pd.read_sql_query(queries[query_choice], conn)

# Show results
st.subheader(f"📊 Results: {query_choice}")
st.dataframe(df, use_container_width=True)

# Download option
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download as CSV", csv, f"{query_choice.replace(' ', '_')}.csv", "text/csv")
