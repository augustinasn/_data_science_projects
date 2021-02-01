from cornelia.imports import *

def pretty_print_iterable(d, tabs=0):
    try:
        for k, v in d.items():
            print(tabs * "\t", k)
            if type(v) is dict:
                pretty_print_dict(v, tabs + 1)
            elif type(v) in [list, set, tuple]:
                for i in v:
                    print((tabs + 1) * "\t", i)
            else:
                print((tabs + 1) * "\t", v)
    except Exception as e:
        try:
            for i in d:
                print(tabs * "\t", i)
        except Exception as e:
            print(e)

pretty_print_dict = pretty_print_iterable

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

def plot_distributions(df, target, n_bins):    
    cols = [col for col in df.columns if (("was_missing" not in col) and ("=>" not in col) and (col != target))]    

    fig, axes = plt.subplots(len(cols), 1, figsize=(15, len(cols) * 7))
    fig.subplots_adjust(wspace=0.1,
                        hspace=0.5)
    
    for col, ax in zip(cols, axes):
        out_df = df[[col, target]].copy().dropna(axis=0).sort_values(by=[col])
        
        if df[col].dtype == "object" or df[col].nunique() <= 15:
            x = out_df[col].unique()
            y = out_df[[col, target]].groupby(col).sum()[target]
            style = "o-r"
            
        else:
            out_df[f"{col}_bin"] = pd.qcut(out_df[col],
                                           q=n_bins,
                                           duplicates="drop")
            x = out_df[f"{col}_bin"].astype(str).unique()
            y = out_df[[f"{col}_bin", target]].groupby(f"{col}_bin").sum()[target].to_list()
            style = ".-b"
        
        ax.plot(x, y, style)
    
        for xy in zip(x, y):                                       
            ax.annotate(xy[0],
                        xy=xy,
                        textcoords="data")

        ax.xaxis.set_major_formatter(plt.NullFormatter())
        ax.set_title(f"{col}", fontdict={"fontsize":12,
                                         "fontweight": "medium"})
