import subprocess
import os
import re
from pathlib import Path

from src.Benchmark import Benchmark
from src.BenchmarkRun import BenchmarkRun


def list_files(directory: str) -> list[str]:
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


class BenchmarkEngine:
    HEADER_PATTERN = re.compile(
        r'-{5,}\n'  # line of dashes before
        r'Benchmark.+?\n'  # header line starting with "Benchmark"
        r'-{5,}',  # line of dashes after
        re.DOTALL
    )

    def __init__(self, binary_path: str, output_dir: str = "benchmark_outputs"):
        self.binary_path = Path(binary_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmarks(self, runs: int = 5):
        if not self.binary_path.exists():
            raise FileNotFoundError(f"Binary not found: {self.binary_path}")

        for i in range(1, runs + 1):
            output_file = self.output_dir / f"run_{i}.txt"
            print(f"[Run {i}/{runs}] Executing {self.binary_path} -> {output_file}")

            with open(output_file, "w") as out:
                result = subprocess.run(
                    [str(self.binary_path)],
                    stdout=out,
                    stderr=subprocess.STDOUT,
                    text=True
                )

            if result.returncode != 0:
                print(f"⚠️  Run {i} failed with exit code {result.returncode}")
            else:
                print(f"✅  Run {i} completed successfully.")

        print("\nAll benchmark runs completed.")
        print(f"Results saved in: {self.output_dir.resolve()}")

    def splitUserCounter(self, user_counter: str):
        name, value_unit = user_counter.split('=', 1)

        # Match numeric part at start, unit after
        match = re.match(r'([0-9.]+)([a-zA-Z/]+)?', value_unit)
        if not match:
            raise ValueError(f"Could not parse value/unit from: {value_unit}")

        value = match.group(1)
        unit = match.group(2) if match.group(2) else ""

        return name, value, unit

        return re.split(r'\s{2,}', header_line)

    def getFirstBenchmarkLine(self, lines):
        start_index = None
        for i, line in enumerate(lines):
            if re.match(r'-{5,}', line):
                if start_index is None:
                    start_index = i
                else:
                    start_index = i + 1
                    break

        if start_index is None or start_index >= len(lines):
            return -1
        return start_index

    def parse_output_files(self):
        result_file_names = list_files(self.output_dir)
        benchmarks = {}

        for file_name in result_file_names:
            result_path = self.output_dir / file_name
            if not result_path.exists():
                raise FileNotFoundError(f"No such result file: {result_path}")

            text = result_path.read_text()
            lines = text.splitlines()
            start_index = self.getFirstBenchmarkLine(lines)

            token_pattern = re.compile(r"\d+(?:\.\d+)?\sns|[^\s]+")

            for line in lines[start_index:]:
                if not line.strip() or line.startswith("Run on"):
                    continue

                parts = token_pattern.findall(line.strip())
                run_name = parts[0]
                if '/' in run_name:
                    bm_name, input_size = run_name.split('/', 1)
                else:
                    bm_name = run_name
                    input_size = -1

                if not benchmarks.__contains__(bm_name):
                    benchmarks[bm_name] = Benchmark(bm_name)
                benchmark = benchmarks[bm_name]

                run = benchmark.getRun(input_size)

                run.addColumnValue("Time", parts[1].replace("ns", "").strip(), "ns")
                run.addColumnValue("CPU", parts[2].replace("ns", "").strip(), "ns")
                run.addColumnValue("Iterations", parts[3])

                for user_counter in parts[4:]:
                    name, value, unit = self.splitUserCounter(user_counter)
                    run.addColumnValue(name, value, unit)
        return benchmarks
