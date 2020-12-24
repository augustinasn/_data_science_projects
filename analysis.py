from cornelia.imports import *
from cornelia.visualization import print_df

def feature_importance(m, df, print_rows=10, to_keep_threshold=0):
    fi = pd.DataFrame({"feature_name": df.columns,
                       "importance": m.feature_importances_}).sort_values("importance",
                                                                          ascending=False).reset_index(drop=True)
    print_df(fi, print_rows)
    
    return fi[fi["importance"] < to_keep_threshold]["feature_name"].to_list()

def rmse(x, y):
    return math.sqrt(((x - y)**2).mean())

def score_regr(m, X_train, y_train, X_valid, y_valid):
    res = [rmse(m.predict(X_train), y_train), 
           rmse(m.predict(X_valid), y_valid), 
           m.score(X_train, y_train),         
           m.score(X_valid, y_valid)]         
    
    if hasattr(m, "oob_score_"):
        res.append(m.oob_score_)
        
    print(res)
    
def score_class(m, X_train, y_train, X_valid, y_valid):
    index = ["Jacquard Score (%)",
             "True Positives (% of all positives)",
             "True Negatives (% of all negatives)",
             "False Positives (% of all positives)",
             "False Negatives (% of all negatives)",
             "Precision (What proportion of positive identifications was actually correct?)",
             "Recall (What proportion of actual positives was identified correctly?)"]

    out_df = pd.DataFrame(columns=["Train", "Valid"], index=index)
    
    for X, y, label in zip([X_train, X_valid], [y_train, y_valid], ["Train", "Valid"]):
        preds = m.predict(X)

        jacquard_score = sum(preds == y) / len(preds)
        true_positives = sum([ True for i, j in zip(preds, y) if (i == 1 and j == 1) ]) / sum(preds)
        true_negatives = sum([ True for i, j in zip(preds, y) if (i == 0 and j == 0) ]) / (len(preds) - sum(preds))
        false_positives = sum([ True for i, j in zip(preds, y) if (i == 1 and j == 0) ]) / sum(preds)
        false_negatives = sum([ True for i, j in zip(preds, y) if (i == 0 and j == 1) ]) / (len(preds) - sum(preds))
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)

        scores = [jacquard_score, true_positives, true_negatives, false_positives, false_negatives, precision, recall]

        for i, score in zip(index, scores):
            out_df.loc[i, label] = score

    print_df(out_df, -1)


def score_with_cols_dropped(m, cols, X_train, X_valid, y_train, y_valid):
    for f in cols:
        X_train_interim, X_valid_interim = drop_cols(dfs=[X_train, X_valid],
                                                     cols=[f])
        m.fit(train_X_interim, train_y)
        print(f"Score when \"{f}\" is dropped:")
        score_class(m, X_train_interim, y_train, X_valid_interim, y_valid)


def confidence(model, df, n_bins):
    preds = []
    for tree in model.estimators_:
        preds.append(np.argmax(tree.predict_proba(df), axis=1))
    preds = np.stack(preds, axis=1)
    out_df = df.copy()
    out_df["preds_avg"] = np.mean(preds, axis=1)
    out_df["preds_std"] = np.std(preds, axis=1)
    
    # Create bins:
    for col in df.columns:
        if df[col].dtype != "object":
            out_df[f"{col}_bin"] = pd.qcut(out_df[col],
                                           q=n_bins,
                                           duplicates="drop")
    for col in df.columns:
        if df[col].nunique() < 15:
            groupby = out_df[[col, "preds_avg", "preds_std"]].groupby(col).mean() 
        else:
            groupby = out_df[[f"{col}_bin", "preds_avg", "preds_std"]].groupby(f"{col}_bin").mean() 

        if groupby.shape[0] != 0:  
            print_df(groupby, -1)

def similiar_features(df):
    corr = np.round(scipy.stats.spearmanr(df).correlation, 4)
    corr_condensed = hc.distance.squareform(1 - corr)
    
    z = hc.linkage(corr_condensed,
                   method="average")
    fig = plt.figure(figsize=(16, 10))

    dendrogram = hc.dendrogram(z,
                               labels=df.columns,
                               orientation="left",
                               leaf_font_size=16)
    plt.show()




def pdps(model, data, target, omit, clusters):
    
    def plot_pdp(model,
                 data,
                 model_features,
                 feature,
                 clusters=None):
    
        p = pdp.pdp_isolate(model=model,
                            dataset=data,
                            model_features=model_features,
                            feature=feature)
        
        return pdp.pdp_plot(p,
                            feature,
                            plot_lines=True,
                            cluster=bool(clusters),
                            n_cluster_centers=clusters)

    model_features = [col for col in data.columns if col != target]
    plot_features = [col for col in model_features if col not in omit]
    
    for feature in plot_features:
        plot_pdp(model=model,
                 data=data,
                 model_features=model_features,
                 feature=feature,
                 clusters=clusters)



    


