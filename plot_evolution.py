import sys
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV files
try:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    Y1 = pd.read_csv(file1)
    Y2 = pd.read_csv(file2)
except IndexError:
    print("Please provide two CSV file paths as command line arguments.")
    sys.exit(1)
except FileNotFoundError:
    print("One or both CSV files not found.")
    sys.exit(1)

# Create figure and axis objects
fig, ax1 = plt.subplots()

# Plot the first dataset
color = 'tab:blue'
ax1.set_xlabel('Generation')
ax1.set_ylabel('Best score', color=color)
ax1.plot(Y1, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(bottom=0)
# Create a second y-axis
ax2 = ax1.twinx()

# Plot the second dataset
color = 'tab:red'
ax2.set_ylabel('Mutation rate', color=color)
ax2.plot(Y2, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(bottom=0)

# Show plot
plt.show()
