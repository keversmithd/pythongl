import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data_analysis/data/SNasiagosn.csv')

# Display the first few rows of the data

columns = ['ra', 'lii', 'bii']  # List of column names

# Generate histograms for each column
for i, column in enumerate(columns):
    plt.figure()  # Create a new figure for each column
    data[column].hist(bins=50, figsize=(20,15))
    plt.savefig(f'data_analysis/images/{column}_{i}.png')  # Save the figure with a unique name





