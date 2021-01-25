from cornelia.imports import *
from cornelia.visualization import *
from cornelia.preprocessing import *
from cornelia.extraction import *
from cornelia.helpers import *


def feature_importance(m, df, print_rows=10, to_keep_threshold=0):
    fi = pd.DataFrame({"feature_name": df.columns,
                       "importance": m.feature_importances_}).sort_values("importance",
                                                                          ascending=False).reset_index(drop=True)
    print_df(fi, print_rows)
    
    to_drop = fi[fi["importance"] < to_keep_threshold]["feature_name"].to_list()
    to_keep = [c for c in df.columns if c not in to_drop]
    
    return to_drop, to_keep

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
             "Precision (What proportion of positive identifications was actually correct?)",
             "Recall (What proportion of actual positives was identified correctly?)",
             "F1",
             "ROC AUC"]

    out_df = pd.DataFrame(columns=["Train", "Valid"], index=index)
    
    for X, y, label in zip([X_train, X_valid], [y_train, y_valid], ["Train", "Valid"]):
        preds = m.predict(X)
        preds_proba = m.predict_proba(X)        
        jacquard_score = sum(preds == y) / len(preds)
        true_positives = sum([ True for i, j in zip(preds, y) if (i == 1 and j == 1) ]) / sum(preds)
        true_negatives = sum([ True for i, j in zip(preds, y) if (i == 0 and j == 0) ]) / (len(preds) - sum(preds))
        false_positives = sum([ True for i, j in zip(preds, y) if (i == 1 and j == 0) ]) / sum(preds)
        false_negatives = sum([ True for i, j in zip(preds, y) if (i == 0 and j == 1) ]) / (len(preds) - sum(preds))
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2 * (precision * recall) / (precision + recall)
        roc_auc = roc_auc_score(y, m.predict_proba(X)[:, 1])


        scores = [jacquard_score, precision,
                  recall, f1, roc_auc]

        for i, score in zip(index, scores):
            out_df.loc[i, label] = score

    print_df(out_df, -1)
    
    return index, scores


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

        
# Example configs for pipeline:
#
# config_1 = {"sample": [0.2, 0.5],
#             "nas": {"mode": "fill",
#                     "params": {"num_method": ["median", "mean", "mode"],
#                                "cat_method": ["mode", None],
#                                "was_missing": [True, False]}},
#             "drop_cols": [["a", "b", "c"],
#                           ["a", "b"]],
#             "categoricals": {"mode": "category_encode"},
#             "split": [0.5, 0.7, 0.9],
#             "prediction": {"model": "rf",
#                            "params": {"n_estimators": [50, 75, 100, 150],
#                                       "max_samples": [50_000, 100_000, 250_000],
#                                       "max_features": [0.7, 0.8, 0.9],
#                                       "min_samples_leaf": [1, 3, 5]}}}

# config_2 = {"sample": [0.2, 0.5],
#             "nas": {"mode": "drop",
#                     "params": {"axis": [0, 1]}},
#             "drop_cols": [["a", "b", "c"],
#                           ["a", "b"]],
#             "categoricals": {"mode": "one_hot_encode",
#                              "params": {"card_threshold": [15]}},
#             "split": [0.5, 0.7, 0.9],
#             "prediction": {"model": "rf",
#                            "params": {"n_estimators": [50, 75, 100, 150],
#                                       "max_samples": [50_000, 100_000, 250_000],
#                                       "max_features": [0.7, 0.8, 0.9],
#                                       "min_samples_leaf": [1, 3, 5]}
#                            }
#             }


class Pipeline:
    def __init__(self, config, train_df, test_df, target, backup=False):
        self.config = config
        self.raw_train_df = train_df
        self.raw_test_df = test_df
        self.target = target
        self.backup = backup
        self.param_sets = list()
        self.labels = list()
        self.validate_input()
        self.last_input = list()
        self.last_m = None 
        
        
    def validate_input(self):
        self.params = [self.config["sample"],
                       self.config["nas"]["mode"],
                       self.config["nas"]["params"].get("num_method", "median"),
                       self.config["nas"]["params"].get("cat_method", "mode"),
                       self.config["nas"]["params"].get("was_missing", True),
                       self.config["nas"]["params"].get("axis", 0),
                       self.config.get("drop_cols", None),
                       self.config["categoricals"]["mode"],
                       self.config["categoricals"].get("params", dict()).get("card_thresh", 15),
                       self.config["split"],
                       self.config["prediction"]["model"],
                       self.config["prediction"]["params"].get("n_estimators", 20),
                       self.config["prediction"]["params"].get("max_samples", None),
                       self.config["prediction"]["params"].get("max_features", 'auto'),
                       self.config["prediction"]["params"].get("min_samples_leaf", 1)]
        
        self.labels = ["sample", "nas_mode", "nas_fill_num_method", "nas_fill_cat_method",
                       "nas_fill_was_missing", "nas_drop_axis", "drop_cols", "categoricals_mode",
                       "categoricals_one_hot_encode_card_thresh", "split",
                       "prediction_model", "prediction_rf_n_estimators", "prediction_rf_max_samples",
                       "prediction_rf_max_features", "prediction_rf_min_samples_leaf"]
        
        self.params = [[i] if not isinstance(i, list) else i for i in self.params]
        self.param_sets = list(itertools.product(*self.params))
                
    def feature_importance(self, to_keep_threshold):
        train_X, train_y, valid_X, valid_y = self.last_input
        
        fi_cols_to_drop = feature_importance(m=self.last_m,
                                             df=train_X,
                                             print_rows=15,
                                             to_keep_threshold=to_keep_threshold)
        return fi_cols_to_drop
    
    def colinear_features(self):
        train_X, train_y, valid_X, valid_y = self.last_input
        similiar_features(train_X)

    
    def scores(self, last_n=-1, sort_by=False):
        try:
            archive = pd.read_csv("./tmp/.scores",
                              sep=";")
            
            if sort:
                archive = archive.sort_values(by=sort_by)
                
            if last_n == -1:
                print_df(archive, last_n)
            else:
                print_df(archive.tail(last_n), -1)
        except:
            print("There's no score file.")
        
    def clear_score(self):
        try:
            os.remove("./tmp/.scores")
        except:
            pass
        
    def run(self):
        for i, ps in enumerate(self.param_sets):
            print(f"\nSub-iteration {i + 1}/{len(self.param_sets)}:")
            
            # Sample data:
            print("\t - Sample:")
            print(f"\t\t # {int(ps[0] * 100)}% of the training/testing data.")
            train_df = self.raw_train_df.copy().sample(frac=ps[0])
            test_df = self.raw_test_df.copy().sample(frac=ps[0])
                        
            # NANs:
            print("\t - NaNs:")
            if self.config["nas"]["mode"] == "fill":
                print("\t\t # mode: fill;")
                print(f"\t\t # num_method: {ps[2]};")
                print(f"\t\t # cat_method: {ps[3]};")
                print(f"\t\t # was_missing: {ps[4]};")
                
                train_df, test_df = fill_NAs(dfs=[train_df, test_df],
                                             omit=[self.target],
                                             num_method=ps[2],
                                             cat_method=ps[3],
                                             was_missing=ps[4],
                                             verbose=False)
            elif self.config["nas"]["mode"] == "drop":
                print("\t\t # mode: drop;")
                print(f"\t\t # axis: {ps[5]};")

                train_df, test_df = drop_NAs(dfs=[train_df, test_df],
                                                  labels=["train_df", "test_df"],
                                                  axis=ps[5],
                                                  verbose=False)
            # Categorical features:
            print("\t - Categoricals:")
            if self.config["categoricals"]["mode"] == "category_encode":
                print("\t\t # mode: categorical_encoding;")
                [train_df, test_df], _ = category_encode(dfs=[train_df, test_df],
                                                         verbose=False)
            elif self.config["categoricals"]["mode"] == "one_hot_encode":
                print("\t\t # mode: one_hot_encode;")
                print(f"\t\t # cardinality threshold: {ps[8]};")
                train_df, test_df = one_hot_encode(dfs=[train_df, test_df],
                                                        card_thresh=ps[8],
                                                        verbose=False)
            # Drop columns:
            if ps[6]:
                print("\t - Drop columns:")
                for c in ps[6]:
                    print(f"\t\t # {c};")
                train_df, test_df = drop_cols(dfs=[train_df, test_df],
                                                   cols=ps[6],
                                                   verbose=False)
            # Split data:
            print("\t - Train/validation split:")
            print(f"\t\t # {round(ps[9] * 100, 0)}/{round((1 - ps[9]) * 100, 0)}")
            train_X, train_y, valid_X, valid_y = split_df(df=train_df,
                                                          target=self.target,
                                                          train_p=ps[9],
                                                          verbose=False)
            # Train model:
            print("\t - Prediction:")
            if self.config["prediction"]["model"] == "rf":
                print(f"\t\t # model - RandomForest;")
                print(f"\t\t # n_estimators - {ps[11]};")
                print(f"\t\t # max_samples - {ps[12]};")
                print(f"\t\t # max_features - {ps[13]};")
                print(f"\t\t # min_samples_leaf - {ps[14]};")

                m = RandomForestClassifier(n_estimators=ps[11],
                                           max_samples=ps[12],
                                           max_features=ps[13],
                                           min_samples_leaf=ps[14],
                                           n_jobs=-1)
                m.fit(train_X, train_y)

            # Backup model:
            if self.backup:
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
                pickle_obj(m, f"model_{timestamp}")
            
            # Score model:
            print("\t - Score:")
            score_labels, scores = score_class(m, train_X, train_y, valid_X, valid_y)
            
            # Archive the result:
            fp = "./tmp/.scores"
            if not os.path.isfile(fp):
                with open("./tmp/.scores", "w+") as fh:
                    fh.write(";".join(self.labels + score_labels) + os.linesep)
                    
            with open(fp, "a") as fh:
                fh.write(";".join([str(i) if not isinstance(i, list) else ",".join([str(j) for j in i]) for i in ps] + [str(s) for s in scores]) + os.linesep)
                
            self.last_input = [train_X, valid_X, valid_X, valid_y]
            self.last_m = m
