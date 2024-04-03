import sys
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV files
try:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]
    Y1 = pd.read_csv(file1)
    Y2 = pd.read_csv(file2)
    Y3 = pd.read_csv(file3) if len(sys.argv) > 3 else None
except IndexError:
    print("Please provide at least two CSV file paths as command line arguments.")
    sys.exit(1)
except FileNotFoundError:
    print("CSV files not found.")
    sys.exit(1)

# Create figure and axis objects
fig, ax1 = plt.subplots()

# Plot the first dataset
color = 'tab:red'
ax1.set_xlabel('Generation')
ax1.set_ylabel('Scores', color=color)
ax1.plot(Y1, color=color, label='Best score')
ax1.plot(Y2, color='tab:orange', label='Average score')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(bottom=0)

# Create a second y-axis if mutation rate data is provided
if Y3 is not None:
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Mutation rate', color=color)
    ax2.plot(Y3, color=color, label='Mutation rate')
    ax2.tick_params(axis='y', labelcolor=color)

    # Get handles and labels for the plots to use in the legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right')
else:
    ax1.legend(loc='upper right')

# Show plot
plt.show()
