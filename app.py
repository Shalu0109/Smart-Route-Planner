import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# Page Configuration

st.set_page_config(
    page_title="NexRoute AI – Smart Route Planner",
    layout="wide"
)

st.title(" NexRoute AI – Smart Route Planner")
st.markdown(
    "An intelligent routing system optimizing **cost**, **delivery time**, and **environmental impact**"
)


# Load Data

@st.cache_data
def load_data():
    routes = pd.read_csv("routes_distance.csv")
    fleet = pd.read_csv("vehicle_fleet.csv")
    costs = pd.read_csv("cost_breakdown.csv")
    orders = pd.read_csv("orders.csv")
    return routes, fleet, costs, orders

routes, fleet, costs, orders = load_data()


# Data Preparation

df = routes.merge(costs, on="order_id", how="left") \
           .merge(orders, on="order_id", how="left")

df.fillna(0, inplace=True)


# Sidebar Controls

st.sidebar.header("Route Preferences")

priority = st.sidebar.selectbox(
    "Delivery Priority",
    ["Express", "Standard", "Economy"]
)

time_weight = st.sidebar.slider("Time Priority", 0.0, 1.0, 0.4)
cost_weight = st.sidebar.slider("Cost Priority", 0.0, 1.0, 0.35)
carbon_weight = st.sidebar.slider("Sustainability Priority", 0.0, 1.0, 0.25)

# Normalize weights
total_weight = time_weight + cost_weight + carbon_weight
time_weight /= total_weight
cost_weight /= total_weight
carbon_weight /= total_weight


# Scoring Logic

df["time_score"] = df["distance_km"] + df["traffic_delay"] + df["weather_impact"]

df["cost_score"] = (
    df["fuel_cost"] +
    df["toll_charges"] +
    df["maintenance_cost"]
)

df["carbon_score"] = df["distance_km"] * df["co2_emissions_per_km"]

df["final_route_score"] = (
    time_weight * df["time_score"] +
    cost_weight * df["cost_score"] +
    carbon_weight * df["carbon_score"]
)


# KPI Section

st.subheader(" Route Optimization Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Routes Evaluated", len(df))
col2.metric("Avg Route Cost", f"₹{round(df['cost_score'].mean(), 2)}")
col3.metric("Avg CO₂ per Route", f"{round(df['carbon_score'].mean(), 2)} kg")


# Best Route Recommendation

st.subheader(" Optimal Route Recommendation")

best_route = df.loc[df["final_route_score"].idxmin()]

st.success(
    f"Recommended Route for Order {best_route['order_id']} "
    f"({priority} Delivery)"
)

st.write("**Why this route?**")
st.write(
    f"- Lowest combined score balancing time, cost, and emissions\n"
    f"- Distance: {best_route['distance_km']} km\n"
    f"- Estimated Cost: ₹{round(best_route['cost_score'], 2)}\n"
    f"- CO₂ Emissions: {round(best_route['carbon_score'], 2)} kg"
)


# Visual Comparisons

st.subheader(" Route Comparison Analysis")

bar_chart = px.bar(
    df.sort_values("final_route_score").head(10),
    x="order_id",
    y="final_route_score",
    title="Top 10 Optimal Routes (Lower is Better)"
)

st.plotly_chart(bar_chart, use_container_width=True)

scatter_chart = px.scatter(
    df,
    x="cost_score",
    y="time_score",
    size="carbon_score",
    color="final_route_score",
    title="Cost vs Time vs Carbon Trade-off"
)

st.plotly_chart(scatter_chart, use_container_width=True)


# Download Section

st.subheader("Export Results")

st.download_button(
    label="Download Route Scores",
    data=df.to_csv(index=False),
    file_name="smart_route_scores.csv",
    mime="text/csv"
)

st.info("NexRoute AI successfully generated optimal routing insights.")
