from tools.carbon_tools import transport_emissions

def optimize_logistics(distance_km):
    modes = ["truck", "ship", "air"]
    emissions = {}

    for mode in modes:
        emissions[mode] = transport_emissions(distance_km, mode)

    best_mode = min(emissions, key=emissions.get)
    return best_mode, emissions
