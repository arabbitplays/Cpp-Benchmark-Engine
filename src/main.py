from BenchmarkEngine import BenchmarkEngine
from src.BenchmarkVisualizer import plot_column_for_run, plot_column_for_benchmark, create_plot_library, plot_benchmark_group

if __name__ == "__main__":
    name = "hyperthreading"
    # = "system"
    binary_file = "/home/oschdi/Projects/delfin/exercise3/basics/build/src/parallel_system_benchmarks"
    raw_data_dir = name + "_bm_out"
    plot_dir = name + "_plot_out"
    engine = BenchmarkEngine(binary_file, raw_data_dir)
    #engine.run_benchmarks(5)
    result = engine.parse_output_files()

    create_plot_library(result, plot_dir)

    #contended_group = engine.create_group(result, "*_contended-4194304")
    #uncontended_group = engine.create_group(result, "*_uncontended-4194304")
    #alloc_group = engine.create_group(result, "*read_linear-268435456")
    #linear_group = engine.create_group(result, "read_linear-*")
    #random_group = engine.create_group(result, "read_random-*")

    #plot_benchmark_group(contended_group, plot_dir)
    #plot_benchmark_group(uncontended_group, plot_dir)
    #plot_benchmark_group(alloc_group, plot_dir)
    #plot_benchmark_group(linear_group, plot_dir)
    #plot_benchmark_group(random_group, plot_dir)