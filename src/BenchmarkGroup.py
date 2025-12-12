from src.Benchmark import Benchmark

class BenchmarkGroup:
    def __init__(self, name: str):
        self.name = name
        self.benchmarks = []

    def addBenchmark(self, benchmark : Benchmark):
        self.benchmarks.append(benchmark)