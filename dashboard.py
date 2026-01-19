# import streamlit as st
# import json
# import pandas as pd
# from agents.supervisor import run_cfoe

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="Carbon Footprint Optimization Engine",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- TITLE ----------------
# st.title("🌱 Carbon Footprint Optimization Engine")
# st.subheader("AI-driven Sustainable Procurement")

# st.markdown(
#     """
#     This system uses a **multi-agent AI architecture** to analyze supplier sustainability,
#     optimize logistics, ensure compliance, and recommend low-carbon procurement strategies.
#     """
# )

# # ---------------- LOAD SUPPLIERS ----------------
# with open("data/suppliers.json") as f:
#     suppliers = json.load(f)

# supplier_names = [s["name"] for s in suppliers]

# # ---------------- SIDEBAR INPUTS ----------------
# st.sidebar.header("🧾 Procurement Inputs")

# selected_supplier_name = st.sidebar.selectbox(
#     "Select Supplier",
#     supplier_names
# )

# distance_km = st.sidebar.slider(
#     "Transportation Distance (km)",
#     min_value=50,
#     max_value=2000,
#     step=50,
#     value=500
# )

# run_button = st.sidebar.button("🚀 Run Optimization")

# # Get selected supplier object
# selected_supplier = next(
#     s for s in suppliers if s["name"] == selected_supplier_name
# )

# # ---------------- MAIN LOGIC ----------------
# if run_button:
#     result = run_cfoe(selected_supplier, distance_km)

#     st.success("Optimization Completed Successfully ✅")

#     # -------- RESULTS SECTION --------
#     st.markdown("## 📊 Optimization Results")

#     col1, col2, col3 = st.columns(3)

#     col1.metric("Supplier", result["supplier"])
#     col2.metric("Transport Mode", result["transport_mode"])
#     col3.metric("Carbon Emissions (kg CO₂)", result["carbon_emissions"])

#     # -------- COMPLIANCE STATUS --------
#     st.markdown("### ✅ Compliance Status")
#     if result["compliance"]:
#         st.success("Procurement is within allowed carbon limits")
#     else:
#         st.error("Procurement exceeds allowed carbon limits")

#     # -------- AI DECISION --------
#     st.markdown("### 🧠 AI Decision & Recommendation")
#     st.info(result["decision"])

#     # ---------------- GRAPHS ----------------
#     st.markdown("## 📈 Visual Analytics")

#     # -------- GRAPH 1: Emissions by Transport Mode --------
#     st.markdown("### 🚚 Emissions by Transport Mode")

#     emission_data = {
#         "Truck": distance_km * 0.21,
#         "Ship": distance_km * 0.03,
#         "Air": distance_km * 0.85
#     }

#     df_emissions = pd.DataFrame(
#         emission_data.items(),
#         columns=["Transport Mode", "Emissions (kg CO₂)"]
#     ).set_index("Transport Mode")

#     st.bar_chart(df_emissions)

#     # -------- GRAPH 2: Supplier Sustainability Comparison --------
#     st.markdown("### 🏭 Supplier Sustainability Scores")

#     supplier_df = pd.DataFrame(suppliers).set_index("name")
#     st.bar_chart(supplier_df["sustainability_score"])

#     # -------- INSIGHT BOX --------
#     st.markdown("### 💡 Key Insight")
#     st.write(
#         f"For a distance of **{distance_km} km**, the system selected "
#         f"**{result['transport_mode']}** as the lowest-carbon option, "
#         f"resulting in **{result['carbon_emissions']} kg CO₂** emissions."
#     )

# else:
#     st.info("👈 Use the sidebar to select inputs and run the optimization.")
import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime
from agents.supervisor import run_cfoe

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Carbon Footprint Optimization Engine",
    layout="wide"
)

st.title("🌱 Carbon Footprint Optimization Engine")
st.caption("AI-driven Sustainable Procurement • Multi-Agent System")

# ---------------- LOAD / SAVE SUPPLIERS ----------------
SUPPLIER_FILE = "data/suppliers.json"

def load_suppliers():
    with open(SUPPLIER_FILE) as f:
        return json.load(f)

def save_suppliers(data):
    with open(SUPPLIER_FILE, "w") as f:
        json.dump(data, f, indent=4)

suppliers = load_suppliers()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Controls")

mode = st.sidebar.radio(
    "Choose Mode",
    ["Single Supplier Optimization", "Compare Suppliers", "Add New Supplier"]
)

distance_km = st.sidebar.slider(
    "Transportation Distance (km)",
    50, 3000, 500, step=50
)

# ======================================================
# 1️⃣ SINGLE SUPPLIER OPTIMIZATION
# ======================================================
if mode == "Single Supplier Optimization":
    supplier_name = st.sidebar.selectbox(
        "Select Supplier",
        [s["name"] for s in suppliers]
    )

    supplier = next(s for s in suppliers if s["name"] == supplier_name)

    if st.sidebar.button("🚀 Run Optimization"):
        result = run_cfoe(supplier, distance_km)

        st.subheader("📊 Optimization Result")

        c1, c2, c3 = st.columns(3)
        c1.metric("Supplier", result["supplier"])
        c2.metric("Transport Mode", result["transport_mode"])
        c3.metric("CO₂ Emissions (kg)", result["carbon_emissions"])

        st.success("✅ Compliance Passed" if result["compliance"] else "❌ Compliance Failed")
        st.info(result["decision"])

        # -------- Emissions Chart --------
        st.subheader("📈 Emissions by Transport Mode")
        df_emissions = pd.DataFrame({
            "Truck": [distance_km * 0.21],
            "Ship": [distance_km * 0.03],
            "Air": [distance_km * 0.85]
        }).T
        df_emissions.columns = ["Emissions (kg CO₂)"]
        st.bar_chart(df_emissions)

        # -------- Future Prediction --------
        st.subheader("🔮 Future Emissions Prediction (Next 5 Years)")
        years = np.arange(1, 6)
        future_emissions = [result["carbon_emissions"] * (1.05 ** y) for y in years]

        forecast_df = pd.DataFrame({
            "Year": [datetime.now().year + y for y in years],
            "Predicted Emissions": future_emissions
        }).set_index("Year")

        st.line_chart(forecast_df)

        # -------- CSV Download --------
        st.subheader("⬇ Download Report")
        report_df = pd.DataFrame([result])
        st.download_button(
            "Download CSV",
            report_df.to_csv(index=False),
            "carbon_report.csv",
            "text/csv"
        )

# ======================================================
# 2️⃣ COMPARE SUPPLIERS SIDE-BY-SIDE
# ======================================================
elif mode == "Compare Suppliers":
    s1, s2 = st.sidebar.multiselect(
        "Select Two Suppliers",
        [s["name"] for s in suppliers],
        max_selections=2
    )

    if len([s1, s2]) == 2 and st.sidebar.button("⚖ Compare"):
        sup1 = next(s for s in suppliers if s["name"] == s1)
        sup2 = next(s for s in suppliers if s["name"] == s2)

        r1 = run_cfoe(sup1, distance_km)
        r2 = run_cfoe(sup2, distance_km)

        df_compare = pd.DataFrame([r1, r2]).set_index("supplier")
        st.subheader("📊 Supplier Comparison")
        st.dataframe(df_compare)

        st.bar_chart(df_compare["carbon_emissions"])

# ======================================================
# 3️⃣ ADD SUPPLIER FROM UI
# ======================================================
elif mode == "Add New Supplier":
    st.subheader("➕ Add Supplier")

    name = st.text_input("Supplier Name")
    sustainability = st.slider("Sustainability Score", 0, 100, 70)
    base_emission = st.number_input("Base Emission Factor", 0.0, 5.0, 1.0)

    if st.button("Save Supplier"):
        suppliers.append({
            "name": name,
            "sustainability_score": sustainability,
            "base_emission": base_emission
        })
        save_suppliers(suppliers)
        st.success("Supplier Added Successfully 🎉")
