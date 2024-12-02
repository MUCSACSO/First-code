import os
import pandas as pd
import numpy as np

def generate_drilling_data(directory="data", file_prefix="test_data"):
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
    
    # Save data
    data = {"Depth (m)": depths, "ROP (m/h)": rop, "RPM": rpm, "Flow Rate (L/min)": fr, "Weight on Bit (tons)": wob}
    df = pd.DataFrame(data)
    
    os.makedirs(directory, exist_ok=True)
    file_index = 1
    while os.path.exists(f"{directory}/{file_prefix}_{file_index}.xlsx"):
        file_index += 1
    file_name = f"{directory}/{file_prefix}_{file_index}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"Data exported to {file_name}")

if __name__ == "__main__":
    generate_drilling_data()
