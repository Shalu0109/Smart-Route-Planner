import pandas as pd

def load_data():
    routes = pd.read_csv("data/routes_distance.csv")
    orders = pd.read_csv("data/orders.csv")
    costs = pd.read_csv("data/cost_breakdown.csv")

    routes.fillna(0, inplace=True)
    orders.fillna(0, inplace=True)
    costs.fillna(0, inplace=True)

    return routes, orders, costs
