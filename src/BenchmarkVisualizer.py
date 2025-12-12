from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt

from src.BenchmarkAnalyzer import getAnalytics
from src.Benchmark import Benchmark
from src.BenchmarkGroup import BenchmarkGroup
from src.BenchmarkRun import BenchmarkRun

def create_plot_library(benchmarks, output_dir):
    out_dir_path = Path(output_dir)

    done_bm_count = 0
    for bm_name, benchmark in benchmarks.items():
        bm_dir_path = out_dir_path / bm_name
        bm_dir_path.mkdir(parents=True, exist_ok=True)
        run = next(iter(benchmark.runs.values()))
        col_names = run.getColumnNames()

        for col_name in col_names:
            plot = plot_column_for_benchmark(benchmark, col_name)
            plot.savefig(str(bm_dir_path) + "/" + bm_name + "-" + col_name + ".png", dpi=300)
            plot.close()

        done_bm_count += 1
        print("[" + str(done_bm_count) + "/" + str(len(benchmarks)) + "] Generated " + str(len(col_names)) + " plots for benchmark " + bm_name)


def plot_column_for_run(run: BenchmarkRun, col_name: str):
    data = run.columns[col_name].values
    median, mad = getAnalytics(data)
    return plot1(data, median, mad)

def plot_column_for_benchmark(benchmark: Benchmark, col_name: str):
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


# ----------------------- Groups ------------------------------------------

def plot_benchmark_group(group : BenchmarkGroup, output_dir):
    run = next(iter(group.benchmarks[0].runs.values()))
    col_names = run.getColumnNames()

    out_dir_path = Path(output_dir)
    group_dir_path = out_dir_path / group.name
    group_dir_path.mkdir(parents=True, exist_ok=True)

    for col_name in col_names:
        plot = plot_column_for_benchmark_group(group, col_name)
        plot.savefig(str(group_dir_path) + "/" + group.name + "-" + col_name + ".png", dpi=300)
        plot.close()

def plot_column_for_benchmark_group(group: BenchmarkGroup, col_name: str):
    unit = ""
    labels = []
    layers = []
    datas = []

    # get labels of the bars
    for label, run in group.benchmarks[0].runs.items():
        labels.append(run.input_size)
        unit = run.columns[col_name].unit
    for i in range(0, len(labels)):
        datas.append([])

    for benchmark in group.benchmarks:
        label_idx = 0
        for label, run in benchmark.runs.items():
            data = run.columns[col_name].values
            median, mad = getAnalytics(data)
            datas[label_idx].append(median)
            label_idx += 1
        layers.append(benchmark.name)

    return group_bar_plot(datas, labels, layers, unit, group.name + " - " + col_name)

def group_bar_plot(data, labels, layers, unit:str = "", title:str = ""):
    n_bars = len(labels)
    n_layers = len(data[0])

    cmap = plt.get_cmap("tab10")  # you can use "tab20", "viridis", etc.
    colors = [cmap(i / n_layers) for i in range(n_layers)]

    for bar_idx in range(n_bars):
        # Get values and layer indices for this bar
        values = [(data[bar_idx][i], i) for i in range(n_layers)]
        # Sort by value descending (largest at bottom)
        values.sort(reverse=True, key=lambda x: x[0])

        bottom = 0
        for val, layer_idx in values:
            plt.bar(bar_idx, val, color=colors[layer_idx])

    plt.xticks(range(n_bars), labels)
    plt.ylabel(unit)
    plt.title(title)

    # Add a legend manually to preserve color-to-layer mapping
    for i in range(n_layers):
        plt.bar(0, 0, color=colors[i], label=layers[i])  # invisible bars for legend
    plt.legend()
    plt.legend()
    return plt