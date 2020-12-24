from cornelia.imports import *


def print_df(df, rows):
    if rows == -1:
        display(HTML(df.to_html()))
    else:
        display(HTML(df.reset_index(drop=True).iloc[:rows].to_html()))
    
def print_missing_data(dfs, labels):
    out_series = [(df.isnull().sum() / df.shape[0] * 100) for df in dfs]
    for ser, lab in zip(out_series, labels):
        ser.name = f"Missing values in {lab} (%)"
        
    out_df = pd.concat(out_series, axis=1)
    out_df.index.name = "feature_name"
    
    return out_df

def print_descriptive_stats(dfs, labels):
    dfs_copy = [df.copy() for df in dfs]
    for df, l in zip(dfs_copy, labels):
        df.columns = [f"{c} ({l})" for c in df.columns]
    return pd.concat([df.describe() for df in dfs_copy], axis=1).sort_index(axis=1).T

def print_categories(df):
    for col in df.columns:
        if df[col].dtype == "object":
            print(f"'{col}' has {df[col].nunique()} categories: {set(df[col])}")
            
def plot_data(dfs, labels, bench, n_bins):
    cols = [col for col in dfs[bench].columns if (("was_missing" not in col) and ("=>" not in col))]
    
    fig, axes = plt.subplots(len(cols), len(dfs), figsize=(16, len(cols) * 7))

    fig.subplots_adjust(wspace=0.1,
                        hspace=0.5)
    
    for col, ax_tuple in zip(cols, axes):
        for ax, df, l in zip(ax_tuple, dfs, labels):
            if df[col].dtype == "object":
                x = df[col].value_counts().index.to_list()
                y = df[col].value_counts().to_list()
                
                ax.bar(x=x,
                       height=y,
                       color="red")
                
                ax.tick_params(axis="x",
                               labelrotation=90)
                
            else:
                lbound = float(df[col].min())
                ubound = float(df[col].max())
                step = (ubound - lbound) / (n_bins)

                bins = np.arange(lbound, ubound + step, step)

                ax.hist(x=df[col],
                        bins=bins,
                        color="blue")
                
                ax.set_xticks(bins)

                ax.ticklabel_format(useOffset=False,
                                    style="plain")

                ax.set_xticklabels([f"{round(v, 1):,}" for v in bins], rotation=45)
            
            ax.set_title(f"{l}=>{col}", fontdict={"fontsize":12,
                                                  "fontweight": "medium"})

# def distributions(dfs, labels, n_bins, unique_thresh, target):
#     dfs_copy = [df.copy() for df in dfs]
#     for df, la in zip(dfs_copy, labels):
#         for col in df.columns:
#             if df[col].nunique() < unique_thresh:
#                 df[f"{col}_"] = df[col]
#                 groupby = df[[col, target, f"{col}_"]].groupby([col, target]).count() 
#             else:
#                 df[f"{col}_bins"] = pd.qcut(df[col],
#                                             q=n_bins,
#                                             duplicates="drop")

#                 groupby = df[[f"{col}_bins", col, target]].groupby([f"{col}_bins", target]).count() 

#             if groupby.shape[0] != 0:
#                 print(f"Distribution of \"{col}\" for \"{la}\":")
#                 print_df(groupby, -1)
