import numpy as np
import pandas as pd
import streamlit as st
import os

def generate_drilling_data(start_depth, end_depth, step, max_step_rop, max_step_rpm, max_step_fr, max_step_wob):
    """
    Generate synthetic drilling data and return it as a DataFrame.
    
    Parameters:
        start_depth (int): Starting depth in meters.
        end_depth (int): Ending depth in meters.
        step (int): Step size in meters.
        max_step_rop (float): Maximum step size for ROP changes.
        max_step_rpm (float): Maximum step size for RPM changes.
        max_step_fr (float): Maximum step size for Flow Rate changes.
        max_step_wob (float): Maximum step size for Weight on Bit changes.
    
    Returns:
        pd.DataFrame: Generated drilling data.
    """
    depths = np.arange(start_depth, end_depth + step, step)
    num_points = len(depths)
    
    # Initialize parameters with random starting values
    rop = np.zeros(num_points)
    rpm = np.zeros(num_points)
    fr = np.zeros(num_points)
    wob = np.zeros(num_points)
    
    rop[0] = np.random.uniform(2, 20)
    rpm[0] = np.random.uniform(60, 120)
    fr[0] = np.random.uniform(200, 400)
    wob[0] = np.random.uniform(5, 20)
    
    # Generate gradual changes
    for i in range(1, num_points):
        rop[i] = np.clip(rop[i-1] + np.random.uniform(-max_step_rop, max_step_rop), 2, 20)
        rpm[i] = np.clip(rpm[i-1] + np.random.uniform(-max_step_rpm, max_step_rpm), 60, 120)
        fr[i] = np.clip(fr[i-1] + np.random.uniform(-max_step_fr, max_step_fr), 200, 400)
        wob[i] = np.clip(wob[i-1] + np.random.uniform(-max_step_wob, max_step_wob), 5, 20)
    
    data = {
        "Depth (m)": depths, 
        "ROP (m/h)": rop, 
        "RPM": rpm, 
        "Flow Rate (L/min)": fr, 
        "Weight on Bit (tons)": wob
    }
    return pd.DataFrame(data)

# Streamlit App
st.title("Enhanced Drilling Data Generator")
st.write("""
This app generates synthetic drilling data with customizable parameters.
Adjust the settings below to control how the data is generated.
""")

# Sidebar for configuration
st.sidebar.header("Configuration")

# Input fields for parameters
start_depth = st.sidebar.number_input("Start Depth (m)", min_value=0, max_value=10000, value=500, step=10)
end_depth = st.sidebar.number_input("End Depth (m)", min_value=start_depth, max_value=10000, value=1000, step=10)
step = st.sidebar.number_input("Step Size (m)", min_value=1, max_value=100, value=5, step=1)
max_step_rop = st.sidebar.slider("Max Step for ROP", 0.1, 5.0, 0.5)
max_step_rpm = st.sidebar.slider("Max Step for RPM", 1, 20, 5)
max_step_fr = st.sidebar.slider("Max Step for Flow Rate", 1, 50, 10)
max_step_wob = st.sidebar.slider("Max Step for Weight on Bit", 0.1, 5.0, 1.0)

# File name input
file_prefix = st.sidebar.text_input("File Prefix", value="test_data")

# Generate Data Button
if st.button("Generate Drilling Data"):
    st.write("Generating data...")
    data = generate_drilling_data(
        start_depth, end_depth, step, 
        max_step_rop, max_step_rpm, max_step_fr, max_step_wob
    )
    st.write("Data preview:")
    st.dataframe(data.head())
    
    # Convert data to CSV for download
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{file_prefix}.csv",
        mime="text/csv",
    )
