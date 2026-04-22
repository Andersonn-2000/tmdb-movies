import pandas as pd
from pathlib import Path

class CSVExporter:
    def __init__(self, filename: Path | str):
        self.filename = Path(filename)
        self.header = False
    
    def save(self, data) -> None:

        if not data:
            return
        
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(data=data)
        df.to_csv(
            self.filename,
            mode='a',
            header= not self.header,
            index=False,
            encoding="utf-8")
        
        self.header = True