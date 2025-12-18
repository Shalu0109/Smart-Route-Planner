from src.scoring_engine import calculate_scores

def get_optimal_route(routes, orders, costs, time_w, cost_w, carbon_w):
    df = routes.merge(costs, on="order_id") \
               .merge(orders, on="order_id")

    df = calculate_scores(df, time_w, cost_w, carbon_w)

    best_route = df.loc[df["final_score"].idxmin()]

    return df, best_route
