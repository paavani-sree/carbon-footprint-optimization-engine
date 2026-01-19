def transport_emissions(distance_km, mode):
    emission_factors = {
        "truck": 0.21,
        "ship": 0.03,
        "air": 0.85
    }
    return distance_km * emission_factors.get(mode, 0.2)


def production_emissions(units, factor):
    return units * factor
