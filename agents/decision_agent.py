from llm import call_llm

def decision_engine(supplier_status, emissions, compliant, transport_mode):
    prompt = f"""
You are a Procurement Decision Agent.

Supplier status: {supplier_status}
Transport mode: {transport_mode}
Carbon emissions: {emissions} kg CO2
Compliance status: {compliant}

Decide whether to:
- Approve procurement
- Suggest an alternative with justification
"""
    return call_llm(prompt)
