import pandas as pd

def createGameObject(csv):
    df = pd.read_csv(csv)
    return df