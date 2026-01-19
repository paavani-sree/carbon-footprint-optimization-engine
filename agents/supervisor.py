from agents.supplier_agent import evaluate_supplier
from agents.logistics_agent import optimize_logistics
from agents.compliance_agent import compliance_check
from agents.decision_agent import decision_engine

def run_cfoe(supplier, distance_km):
    supplier_status = evaluate_supplier(supplier)

    best_mode, emissions_map = optimize_logistics(distance_km)
    emissions = emissions_map[best_mode]

    compliant = compliance_check(emissions)

    decision = decision_engine(
        supplier_status,
        emissions,
        compliant,
        best_mode
    )

    return {
        "supplier": supplier["name"],
        "supplier_status": supplier_status,
        "transport_mode": best_mode,
        "carbon_emissions": emissions,
        "compliance": compliant,
        "decision": decision
    }
