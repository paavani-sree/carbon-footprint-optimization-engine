def evaluate_supplier(supplier):
    if supplier["sustainability_score"] >= 75:
        return "compliant"
    return "non-compliant"
