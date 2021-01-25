from cornelia.imports import *
from cornelia.visualization import *
from cornelia.extraction import *
from cornelia.helpers import *
from cornelia.analysis import *


def match_cols(df1, df2, omit):           
    cols = list(df2.columns)
    cols += omit
    
    df1_out = df1[cols].copy()
    
    cols_removed = [c for c in df1.columns if c not in cols]
    
    if cols_removed:
        print(f"Columns removed: {', '.join()}")
    else:
        print("No columns removed.")
    
    print_df(df1_out, 5)
              
    return df1_out


def shuffle_rows(dfs, verbose=True):
    out_dfs = []
    for i, df in enumerate(dfs):
        out_df = df.copy()
        out_df = out_df.sample(frac=1)
        if verbose:
            print(f"{out_df.shape[0]} rows shuffled in df No.{i + 1}.")
    return dfs


def drop_cols(dfs, cols, verbose=True):
    out_dfs = []
    for df in dfs:
        out_df = df.copy()
        for col in cols:
            out_df = out_df.drop(col, axis=1)
        out_dfs.append(out_df)
    if verbose:
        print("Done.")
        
    return out_dfs


def fill_NAs(dfs, omit, num_method=None, cat_method=None, was_missing=True, verbose=True):
    # fyi: values for numerical column na filling are determined from the first df.
    num_methods = {"median": (lambda x: x.median()),
                   "mean": (lambda x: x.mean())}
    cat_methods = {"mode": (lambda x: x.value_counts().sort_values(ascending=False).index[0])}
    
    out_dfs = [df.copy() for df in dfs]
    
    for col in dfs[0].columns:
        if col in omit:
            continue
        for df in out_dfs:
            if was_missing:
                df[f"{col}=>was_missing"] = df[col].isnull()
                
            if df[col].dtype == "object":
                if cat_method:
                    cat_val = cat_methods[cat_method](out_dfs[0][col])
                else:
                    cat_val = "missing"
                df[col] = df[col].fillna(cat_val)
            else:
                if num_method:
                    num_val = num_methods[num_method](out_dfs[0][col])
                else:
                    num_val = 0
                df[col] = df[col].fillna(num_val)
                
    if verbose:
        print("Done.")
            
    return out_dfs

         
def drop_NAs(dfs, labels, axis, verbose=True):
    shape_before = {k: f"{v.shape[0]}*{v.shape[1]}" for k, v in zip(labels, dfs)}
    dfs_out = [df.copy() for df in dfs]
    for i, df in enumerate(dfs_out):
        dfs_out[i] = df.dropna(axis=axis)
    shape_after = {k: f"{v.shape[0]}*{v.shape[1]}" for k, v in zip(labels, dfs_out)}
    
    if verbose:
        print("Before:")
        pretty_print_dict(shape_before)
        print("After:")
        pretty_print_dict(shape_after)    
    
    return dfs_out
              
def category_encode(dfs, verbose=True):
    dfs_out = [df.copy() for df in dfs]
    mapping = {}
    for col in dfs_out[0].columns:
        if dfs_out[0][col].dtype == "object":
            mapping[col] = {}
            n = 1
            for val in set(dfs_out[0][col].to_list()):
                mapping[col][val] = n
                for df in dfs_out:
                    df[col] = df[col].apply(lambda x: n if x == val else x)
                n += 1    
    if verbose:
        pretty_print_dict(mapping)
    
    return dfs_out, mapping


def one_hot_encode(dfs, card_thresh, verbose=True):
    dfs_out = [df.copy() for df in dfs]
        
    for col in dfs_out[0].columns:
        if dfs_out[0][col].dtype == "object":
            if len(set(dfs_out[0][col])) <= card_thresh:
                for val in list(set(dfs_out[0][col])):
                    for df in dfs_out:
                        df[f"{col}=>{val}_OHE"] = (df[col] == val)
    
    dfs_out = [df[[col for col in df.columns if df[col].dtype != "object"]] for df in dfs_out]
    
    if verbose:
        print("Done.")
    
    return dfs_out


def split_df(df, target, train_n=None, train_p=None, verbose=True):
    in_df = shuffle_rows(dfs=[df], verbose=verbose)[0]
    
    if train_n:
        train = in_df.iloc[:train_n]
        valid = in_df.iloc[train_n:]
    elif train_p:
        train = in_df[:int(in_df.shape[0] * train_p)]
        valid = in_df[int(in_df.shape[0] * train_p):]
    
    train_y = train[target]
    train_X = train.drop(target, axis=1)
    valid_y = valid[target]
    valid_X = valid.drop(target, axis=1)
    
    if verbose:
        print("Shapes of the outputs:", train_X.shape, train_y.shape, valid_X.shape, valid_y.shape)
    
    return train_X, train_y, valid_X, valid_y
