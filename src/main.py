from BenchmarkEngine import BenchmarkEngine
from src.BenchmarkVisualizer import plotColumnForRun, plotColumnForBenchmark, createPlotLibrary

if __name__ == "__main__":
    binary_file = "/home/oschdi/Projects/cpp-lab/delfin/exercise1/basics/build/release/system_benchmarks"
    raw_data_dir = "benchmark_outputs"
    plot_dir = "plot_outputs"
    engine = BenchmarkEngine(binary_file, raw_data_dir)
    #engine.run_benchmarks(10)
    result = engine.parse_output_files()

    createPlotLibrary(result, plot_dir)

