import pandas as pd

def read_from_csv(filename):
    df = pd.read_csv(filename)

    return df