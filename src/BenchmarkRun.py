class Column:
    def __init__(self, name: str, unit: str = ""):
        self.name = name
        self.values = []
        self.unit = unit

    def addValue(self, value: float):
        self.values.append(value)

class BenchmarkRun:
    def __init__(self, name: str, input_size: int):
        self.name = name
        self.input_size = input_size;
        self.columns = {}

    def normalizeUnit(self, unit: str):
        if unit == "ns" or unit == "":
            return unit, 1

        unit_multipliers = {
            "Ki/s": 1 / (1024 ** 2),
            "Mi/s": 1 / 1024,
            "Gi/s": 1,
            "Ti/s": 1024,
        }

        if unit in unit_multipliers:
            return "Gi/s", unit_multipliers[unit]

        unit_multipliers = {
            "K/s": 1 / (1000 ** 2),
            "M/s": 1 / 1000,
            "G/s": 1,
            "T/s": 1000,
        }

        if unit in unit_multipliers:
            return "G/s", unit_multipliers[unit]

        unit_multipliers = {
            "Ki": 1 / (1024 ** 2),
            "Mi": 1 / 1024,
            "Gi": 1,
            "Ti": 1024,
        }

        if unit in unit_multipliers:
            return "Gi", unit_multipliers[unit]

        raise ValueError(f"Unknown unit: {unit}")

    def addColumnValue(self, col_name: str, value: float, unit: str = ""):
        norm_unit, unit_norm_factor = self.normalizeUnit(unit)
        if not self.columns.__contains__(col_name):
            self.columns[col_name] = Column(col_name, norm_unit)

        self.columns[col_name].addValue(value * unit_norm_factor)

    def getColumnNames(self):
        return self.columns.keys()