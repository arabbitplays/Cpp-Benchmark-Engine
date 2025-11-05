from BenchmarkEngine import BenchmarkEngine
from src.BenchmarkVisualizer import plotColumnForRun, plotColumnForBenchmark

if __name__ == "__main__":
    engine = BenchmarkEngine("/home/oschdi/Projects/cpp-lab/delfin/exercise1/basics/build/release/system_benchmarks")
    #engine.run_benchmarks(10)
    result = engine.parse_output_files()

    plotColumnForBenchmark(result["read_linear"], "bytes_per_second")
    print(len(result))
