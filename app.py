import os
import numpy as np
import pandas as pd
import streamlit as st

def generate_drilling_data(file_prefix="test_data"):
    """
    Generate synthetic drilling data and return it as a DataFrame.
    
    Parameters:
        file_prefix (str): Prefix for the output file names.
        
    Returns:
        pd.DataFrame: Generated drilling data.
    """
    # Define depth range
    depths = np.arange(500, 1005, 5)
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
        rop[i] = np.clip(rop[i-1] + np.random.uniform(-0.5, 0.5), 2, 20)
        rpm[i] = np.clip(rpm[i-1] + np.random.uniform(-5, 5), 60, 120)
        fr[i] = np.clip(fr[i-1] + np.random.uniform(-10, 10), 200, 400)
        wob[i] = np.clip(wob[i-1] + np.random.uniform(-1, 1), 5, 20)
    
    # Create data
    data = {
        "Depth (m)": depths, 
        "ROP (m/h)": rop, 
        "RPM": rpm, 
        "Flow Rate (L/min)": fr, 
        "Weight on Bit (tons)": wob
    }
    df = pd.DataFrame(data)
    return df

# Streamlit App
st.title("Drilling Data Generator")
st.write("""
This app generates synthetic drilling data with random but gradual changes.
You can download the data as a CSV file.
""")

# Generate Data Button
if st.button("Generate Drilling Data"):
    st.write("Generating data...")
    data = generate_drilling_data()
    st.write("Data preview:")
    st.dataframe(data.head())
    
    # Convert data to CSV for download
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="drilling_data.csv",
        mime="text/csv",
    )
