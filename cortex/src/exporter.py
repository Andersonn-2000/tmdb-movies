import os
import pandas as pd
from pathlib import Path

class CSVExporter:
    def __init__(self, filename: Path | str):
        self.filename = filename
    
    def save(self, data) -> None:

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        df = pd.DataFrame(data=data)
        df.to_csv(self.filename, index=False, encoding="utf-8")