class Column:
    def __init__(self, name: str, unit: str = ""):
        self.name = name
        self.values = []
        self.unit = unit

    def addValue(self, value: float):
        self.values.append(value)

class BenchmarkResult:
    def __init__(self, name: str):
        self.name = name
        self.columns = {}

    def addColumnValue(self, col_name: str, value: float, unit: str = ""):
        if not self.columns.__contains__(col_name):
            self.columns[col_name] = Column(col_name, unit)

        self.columns[col_name].addValue(value)