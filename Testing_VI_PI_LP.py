import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Solver import solution
from Constants import Constants, generate_unique_coordinates
from utils import *
import itertools
import ComputeExpectedStageCosts
import ComputeTransitionProbabilities

# Define the parameter ranges
M_values = range(3, 9)
N_values = range(3, 9)
N_DRONES_values = range(2, 6)

# Initialize lists to store results
results = []

# Iterate over all parameter combinations
for M in M_values:
    for N in N_values:
        for N_DRONES in N_DRONES_values:
            print(f"Testing M={M}, N={N}, Drones={N_DRONES}")
            # Update Constants
            Constants.M = M
            Constants.N = N
            Constants.N_DRONES = N_DRONES
            Constants.START_POS, Constants.GOAL_POS, Constants.DRONE_POS = generate_unique_coordinates(N_DRONES + 2, M, N)
            Constants.STATE_SPACE = np.array(list(itertools.product(np.arange(N), np.arange(M), np.arange(N), np.arange(M))), dtype=int)[:, [3, 2, 1, 0]]
            Constants.K = len(Constants.STATE_SPACE)
            Constants.CURRENT_PROB = np.random.uniform(0, 0.1, (M, N))
            Constants.FLOW_FIELD = np.random.choice([-2, -1, 0, 1, 2], size=(M, N, 2))

            # Generate random P and Q matrices for testing
            P = ComputeTransitionProbabilities.compute_transition_probabilities(Constants)
            Q = ComputeExpectedStageCosts.compute_expected_stage_cost(Constants)

            # Test Value Iteration
            start_time = time.time()
            solution(P, Q, Constants, method="value_iteration")
            vi_time = time.time() - start_time

            # Test Policy Iteration
            start_time = time.time()
            solution(P, Q, Constants, method="policy_iteration")
            pi_time = time.time() - start_time

            # Test Linear Programming
            start_time = time.time()
            solution(P, Q, Constants, method="linear_programing")
            lp_time = time.time() - start_time

            # Determine the best algorithm for the current setting
            best_time = min(vi_time, pi_time, lp_time)
            if best_time == vi_time:
                best_algorithm = "Value Iteration"
            elif best_time == pi_time:
                best_algorithm = "Policy Iteration"
            else:
                best_algorithm = "Linear Programming"

            # Store the results
            results.append({
                "M": M,
                "N": N,
                "N_DRONES": N_DRONES,
                "Value Iteration Time": vi_time,
                "Policy Iteration Time": pi_time,
                "Linear Programming Time": lp_time,
                "Best Algorithm": best_algorithm
            })

# Convert results to a DataFrame
df_results = pd.DataFrame(results)

# Check if DataFrame is created correctly
print("DataFrame created successfully:")
print(df_results.head())

# Save DataFrame to CSV
csv_file_path = "solver_performance_results.csv"
df_results.to_csv(csv_file_path, index=False)

# Confirm that the CSV file is saved
print(f"Results saved to {csv_file_path}")

# Plot the performance with respect to parameters
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# Plot performance with respect to M
df_results.groupby("M").mean(numeric_only=True)[["Value Iteration Time", "Policy Iteration Time", "Linear Programming Time"]].plot(ax=axes[0])
axes[0].set_title("Performance with respect to M")
axes[0].set_xlabel("M")
axes[0].set_ylabel("Time (s)")

# Plot performance with respect to N
df_results.groupby("N").mean(numeric_only=True)[["Value Iteration Time", "Policy Iteration Time", "Linear Programming Time"]].plot(ax=axes[1])
axes[1].set_title("Performance with respect to N")
axes[1].set_xlabel("N")
axes[1].set_ylabel("Time (s)")

# Plot performance with respect to N_DRONES
df_results.groupby("N_DRONES").mean(numeric_only=True)[["Value Iteration Time", "Policy Iteration Time", "Linear Programming Time"]].plot(ax=axes[2])
axes[2].set_title("Performance with respect to N_DRONES")
axes[2].set_xlabel("N_DRONES")
axes[2].set_ylabel("Time (s)")

plt.tight_layout()
plt.show()

# Print summary table
print("Summary of best algorithms for each setting:")
print(df_results)