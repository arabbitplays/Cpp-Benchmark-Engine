from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt

from src.BenchmarkAnalyzer import getAnalytics
from src.Benchmark import Benchmark
from src.BenchmarkRun import BenchmarkRun

def createPlotLibrary(benchmarks, output_dir):
    out_dir_path = Path(output_dir)

    for bm_name, benchmark in benchmarks.items():
        bm_dir_path = out_dir_path / bm_name
        bm_dir_path.mkdir(parents=True, exist_ok=True)
        run = next(iter(benchmark.runs.values()))
        col_names = run.getColumnNames()

        for col_name in col_names:
            plot = plotColumnForBenchmark(benchmark, col_name)
            plot.savefig(str(bm_dir_path) + "/" + bm_name + "-" + col_name + ".png")
            plot.close()


def plotColumnForRun(run: BenchmarkRun, col_name: str):
    data = run.columns[col_name].values
    median, mad = getAnalytics(data)
    return plot1(data, median, mad)

def plotColumnForBenchmark(benchmark: Benchmark, col_name: str):
    unit = ""
    labels = []
    datas = []

    for label, run in benchmark.runs.items():
        labels.append(run.input_size)
        data = run.columns[col_name].values
        unit = run.columns[col_name].unit
        datas.append(data)

    return plot2(datas, labels, unit, benchmark.name + " - " + col_name)

def plot1(data, median, mad):

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
    return plt


def plot2(datas, labels=None, unit:str = "", title:str = ""):
    fig, ax = plt.subplots(figsize=(6, 4))
    bp = ax.boxplot(datas, labels=labels, patch_artist=True)

    ax.set_title(title)
    ax.set_ylabel(unit)

    plt.tight_layout()
    return plt