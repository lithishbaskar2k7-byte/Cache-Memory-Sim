class SimulationHistory:

    def __init__(self):
        self.records = []

    def add(self, result):
        self.records.append(result)

    def clear(self):
        self.records.clear()

    def get_records(self):
        return self.records