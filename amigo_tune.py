import streamlit as st
import pandas as pd

def calculate_amigo_pi(K, tau, theta):
    """Calculate Kc and tau_I for a PI controller using AMIGO tuning rules."""
    Kc = (0.15 / K) + ((0.35 - (theta * tau) / ((theta + tau) ** 2)) * (tau / (K * theta)))
    tau_I = 0.35 * theta + (13 * theta * tau**2) / (tau**2 + 12 * theta * tau + 7 * theta**2)
    return Kc, tau_I

def calculate_amigo_pid(K, tau, theta):
    """Calculate Kc, tau_I, and tau_D for a PID controller using AMIGO tuning rules."""
    Kc = (1 / K) * (0.2 + 0.45 * (tau / theta))
    tau_I = (0.40 * theta + 0.8 * tau) / (theta + 0.1 * tau)
    tau_D = 0.50 * tau / (0.30 + tau)
    return Kc, tau_I, tau_D

def main():
    st.title("Online Calculator for Determination of AMIGO Controller Settings based on FOPTD model")

    # Input panel on the left
    with st.sidebar:
        st.header("Input Parameters")
        K = st.number_input("Process Gain (K):", min_value=0.0, value=1.0)
        tau = st.number_input("Time Constant (τ):", min_value=0.0, value=1.0)
        theta = st.number_input("Time Delay (θ):", min_value=0.0, value=0.1, format="%.3f")

        controller_type = st.selectbox("Controller Type:", ["PI", "PID"], index=0)

    # Perform calculation based on controller type
    if controller_type == "PI":
        Kc, tau_I = calculate_amigo_pi(K, tau, theta)
        tau_D = None  # Not applicable for PI controller
    elif controller_type == "PID":
        Kc, tau_I, tau_D = calculate_amigo_pid(K, tau, theta)

    # Prepare results in a table
    data = {
        "Parameter": ["Controller Type", "Controller Gain (Kc)", "Integral Time (τ_I)", "Derivative Time (τ_D)"],
        "Value": [
            controller_type,
            f"{Kc:.4f}",
            f"{tau_I:.4f}",
            f"{tau_D:.4f}" if tau_D is not None else "Not applicable",
        ],
    }
    df = pd.DataFrame(data)

    # Display results
    st.header("Calculated Parameters")
    st.table(df)

if __name__ == "__main__":
    main()
