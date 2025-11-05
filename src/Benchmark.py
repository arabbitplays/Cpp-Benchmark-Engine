from src.BenchmarkRun import BenchmarkRun

class Benchmark:
    def __init__(self, name: str):
        self.name = name
        self.runs = {}

    def getRun(self, input_size: int):
        if not self.runs.__contains__(input_size):
            self.runs[input_size] = BenchmarkRun(self.name, input_size)
        return self.runs[input_size]