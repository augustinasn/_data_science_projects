from cornelia.imports import *
from cornelia.visualization import print_df

def read_feather(filename):
    df = pd.read_feather(f"./data/{filename}")
    print_df(df, 5)
    return df

def pickle_obj(obj, name):
    with open(f"./tmp/{name}.pkl", "wb") as fh:
        pickle.dump(obj, fh)
    print(f"Object saved @ ./tmp/{name}.pkl")

def unpickle_obj(name):
    with open(f"./tmp/{name}.pkl", "rb") as fh:
        return pickle.load(fh)
