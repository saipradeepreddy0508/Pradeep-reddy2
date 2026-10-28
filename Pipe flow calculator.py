# Pradeep-reddy2
import streamlit as st
import math

# Constant
G = 9.81  # Acceleration due to gravity (m/s^2)

# Calculation Functions
def calculate_reynolds_number(density, velocity, diameter, viscosity):
    """Calculates Reynolds Number (Re)"""
    return (density * velocity * diameter) / viscosity

def calculate_friction_factor(reynolds, roughness, diameter):
    """Calculates Darcy Friction Factor (f)"""
    if reynolds <= 2000:
        return 64.0 / reynolds
    else:
        # Turbulent flow (Swamee-Jain equation)
        relative_roughness = roughness / diameter
        term = (relative_roughness / 3.7) + (5.74 / (reynolds ** 0.9))
        return 0.25 / (math.log10(term) ** 2)

def calculate_head_loss(f, length, diameter, velocity):
    """Calculates Head Loss (hf) in meters"""
    return f * (length / diameter) * ((velocity ** 2) / (2 * G))

def calculate_pressure_drop(head_loss, density):
    """Calculates Pressure Drop (delta_p) in Pascals"""
    return density * G * head_loss

# App UI Configuration
st.set_page_config(page_title="Pipe Flow Calculator", page_icon="🚰", layout="centered")

st.title("🚰 Pipe Flow Calculator")
st.write("Perform hydraulic calculations for fluid flow in pipes.")

# Navigation Options
option = st.sidebar.radio(
    "Select Calculation Type:",
    (
        "1. Reynolds Number",
        "2. Darcy Friction Factor",
        "3. Head Loss",
        "4. Pressure Drop"
    )
)

st.markdown("---")

# 1. Reynolds Number
if option == "1. Reynolds Number":
    st.header("Calculate Reynolds Number (Re)")
    
    col1, col2 = st.columns(2)
    with col1:
        rho = st.number_input("Fluid Density (kg/m³)", value=1000.0, format="%.2f")
        v = st.number_input("Fluid Velocity (m/s)", value=2.0, format="%.2f")
    with col2:
        d = st.number_input("Pipe Inner Diameter (m)", value=0.05, format="%.4f")
        mu = st.number_input("Dynamic Viscosity (Pa·s)", value=0.001002, format="%.6f")

    if st.button("Calculate Re", type="primary"):
        if mu > 0 and d > 0:
            re = calculate_reynolds_number(rho, v, d, mu)
            st.metric(label="Reynolds Number (Re)", value=f"{re:,.2f}")

            if re < 2000:
                st.info("**Flow Regime:** Laminar")
            elif re <= 4000:
                st.warning("**Flow Regime:** Transitional")
            else:
                st.success("**Flow Regime:** Turbulent")
        else:
            st.error("Viscosity and Diameter must be greater than zero.")

# 2. Darcy Friction Factor
elif option == "2. Darcy Friction Factor":
    st.header("Calculate Darcy Friction Factor (f)")
    
    re = st.number_input("Reynolds Number (Re)", value=50000.0, format="%.2f")
    d = st.number_input("Pipe Inner Diameter (m)", value=0.05, format="%.4f")
    epsilon = st.number_input(
        "Pipe Roughness (m) [e.g., 0.000045 for commercial steel]", 
        value=0.000045, 
        format="%.6f"
    )

    if st.button("Calculate Friction Factor", type="primary"):
        if re > 0 and d > 0:
            f = calculate_friction_factor(re, epsilon, d)
            st.metric(label="Darcy Friction Factor (f)", value=f"{f:.5f}")
            if re <= 2000:
                st.caption("Calculated using the laminar equation: f = 64 / Re")
            else:
                st.caption("Calculated using the Swamee-Jain equation for turbulent flow.")
        else:
            st.error("Reynolds number and Diameter must be greater than zero.")

# 3. Head Loss
elif option == "3. Head Loss":
    st.header("Calculate Head Loss (h_f)")
    
    col1, col2 = st.columns(2)
    with col1:
        f = st.number_input("Darcy Friction Factor (f)", value=0.02, format="%.5f")
        L = st.number_input("Pipe Length (m)", value=100.0, format="%.2f")
    with col2:
        d = st.number_input("Pipe Inner Diameter (m)", value=0.05, format="%.4f")
        v = st.number_input("Fluid Velocity (m/s)", value=2.0, format="%.2f")

    if st.button("Calculate Head Loss", type="primary"):
        if d > 0:
            hf = calculate_head_loss(f, L, d, v)
            st.metric(label="Head Loss (h_f)", value=f"{hf:.4f} m")
        else:
            st.error("Pipe diameter must be greater than zero.")

# 4. Pressure Drop
elif option == "4. Pressure Drop":
    st.header("Calculate Pressure Drop (ΔP)")
    
    col1, col2 = st.columns(2)
    with col1:
        hf = st.number_input("Head Loss (m)", value=8.1549, format="%.4f")
    with col2:
        rho = st.number_input("Fluid Density (kg/m³)", value=1000.0, format="%.2f")

    if st.button("Calculate Pressure Drop", type="primary"):
        dp = calculate_pressure_drop(hf, rho)
        st.metric(label="Pressure Drop (ΔP)", value=f"{dp:,.2f} Pa")
        st.caption(f"Equivalent to **{dp/1000:.3f} kPa** or **{dp/100000:.4f} bar**")
