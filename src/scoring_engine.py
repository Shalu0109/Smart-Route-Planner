def calculate_scores(df, time_w, cost_w, carbon_w):
    df["time_score"] = (
        df["distance_km"] +
        df["traffic_delay"] +
        df["weather_impact"]
    )

    df["cost_score"] = (
        df["fuel_cost"] +
        df["toll_charges"] +
        df["maintenance_cost"]
    )

    df["carbon_score"] = (
        df["distance_km"] *
        df["co2_emissions_per_km"]
    )

    total = time_w + cost_w + carbon_w
    time_w, cost_w, carbon_w = time_w/total, cost_w/total, carbon_w/total

    df["final_score"] = (
        time_w * df["time_score"] +
        cost_w * df["cost_score"] +
        carbon_w * df["carbon_score"]
    )

    return df
