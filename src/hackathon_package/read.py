# Built-Ins
from pathlib import Path

# Dependencies
import pandas as pd

# Local Imports


def open_csv(file_path: str | Path):
    df = pd.read_csv(file_path)
    print(df)


if __name__ == "__main__":
    base_fp = Path("C:/D stuff/UMD Geol/Research/For experiments/Experiments/")
    spot_set = Path(base_fp, "FMQ900_GS_slab/GSB1.2_normal_b/t0/Spot/")
    for i in spot_set.iterdir():
        print(i)
    # open_csv()
