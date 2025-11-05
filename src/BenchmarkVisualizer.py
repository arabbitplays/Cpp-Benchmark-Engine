from statistics import median

import matplotlib.pyplot as plt

from src.BenchmarkAnalyzer import getAnalytics
from src.Benchmark import Benchmark
from src.BenchmarkRun import BenchmarkRun


def plotColumnForRun(run: BenchmarkRun, col_name: str):
    data = run.columns[col_name].values
    median, mad = getAnalytics(data)
    plot1(median, mad)

def plotColumnForBenchmark(benchmark: Benchmark, col_name: str):
    medians = []
    mads = []
    labels = []

    for label, run in benchmark.runs.items():
        labels.append(label)
        data = run.columns[col_name].values
        median, mad = getAnalytics(data)
        medians.append(median)
        mads.append(mad)

    plot2(medians, mads, labels)

def plot1(median, mad):

    # Plot data points
    plt.figure(figsize=(8, 4))
    plt.scatter(range(len(data)), data, color='steelblue', label='Data Points')

    # Add median line
    plt.axhline(median, color='red', linestyle='--', linewidth=2, label=f'Median = {median:.2f}')

    # Add MAD range (median ± MAD)
    plt.axhline(median + mad, color='orange', linestyle=':', label=f'Median + MAD = {median + mad:.2f}')
    plt.axhline(median - mad, color='orange', linestyle=':', label=f'Median - MAD = {median - mad:.2f}')

    plt.ylim(median - 2 * mad, median + 2 * mad)  # <-- restrict y-axis

    # Labels and legend
    plt.title("Median and Median Absolute Deviation (MAD)")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot2(medians, mads, labels=None, width=0.6):
    n = len(medians)
    x = range(n)

    plt.figure(figsize=(1.5 * n, 4))

    for i, (median_val, mad_val) in enumerate(zip(medians, mads)):
        # Draw the "box" for MAD
        plt.bar(i, 2 * mad_val, bottom=median_val - mad_val,
                width=width, color='orange', alpha=0.3, edgecolor='black')
        # Draw median line
        plt.plot([i - width / 2, i + width / 2],
                 [median_val, median_val],
                 color='red', linestyle='--', linewidth=2)

    # Labels
    plt.xticks(x, labels if labels else [f"Item {i + 1}" for i in x])
    plt.ylabel("Value")
    plt.title("Median ± MAD Box Plots")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()