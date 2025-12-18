def normalize_weights(time_w, cost_w, carbon_w):
    total = time_w + cost_w + carbon_w
    return time_w/total, cost_w/total, carbon_w/total
