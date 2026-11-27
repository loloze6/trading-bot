def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "day"])
    B["val"] = (1 + B["book_return"]).cumprod()
    B["peak"] = B["val"].cummax()
    B["dd"] = B["val"] / B["peak"] - 1
    out["deepest_fall"] = float(B["dd"].min())
    out["dd_by_window"] = B.groupby("wn").agg(mean=("book_return", "mean"), sum=("book_return", "sum"), mindd=("dd", "min"), n=("book_return", "size"))
    # locate deepest fall
    i_tr = B["dd"].idxmin()
    sub = B.loc[:i_tr]
    i_pk = sub["val"].idxmax()
    out["fall_span"] = f"peak w{B.loc[i_pk,'wn']} -> trough w{B.loc[i_tr,'wn']}, days {B.index.get_loc(i_tr)-B.index.get_loc(i_pk)}"
    # bar-level cases
    cr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["r0"] = b["close"] / b["close"].shift(1) - 1
            lr = np.log(b["close"]).diff()
            b["s"] = lr.rolling(30).std()
            b["width"] = (b["high"] - b["low"]) / b["close"] / b["s"]
            b["pos"] = (b["close"] - b["low"]) / (b["high"] - b["low"])
            b["r5"] = b["close"] / b["close"].shift(5) - 1
            b["r60"] = b["close"] / b["close"].shift(60) - 1
            b["a"] = b["postRebalance_current_allocation"]
            b["gain"] = b["a"] * b["nxt"]
            b["coin"] = c; b["wn"] = int(w[1:])
            cr.append(b)
    X = pd.concat(cr)
    drift = X.groupby("coin")["nxt"].mean()
    X["ex"] = X["nxt"] - X["coin"].map(drift)
    A = X[(X["a"].abs() > 1e-9) & X["nxt"].notna()].copy()
    A["side"] = np.sign(A["a"])
    A["direx"] = A["side"] * A["ex"]
    A["dirnxt"] = A["side"] * A["nxt"]
    def summ(g):
        return pd.Series({"n": len(g), "dirnxt_mean": g["dirnxt"].mean(), "t": g["dirnxt"].mean() / (g["dirnxt"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan, "gain_sum": g["gain"].sum(), "abs_a": g["a"].abs().mean()})
    out["by_side"] = A.groupby("side").apply(summ)
    A["fq"] = pd.qcut(A["forecast"].abs(), 3, labels=["lo", "mid", "hi"])
    out["by_side_fq"] = A.groupby(["side", "fq"]).apply(summ)
    A["wq"] = pd.qcut(A["width"], 3, labels=["narrow", "mid", "wide"])
    out["by_side_width"] = A.groupby(["side", "wq"]).apply(summ)
    A["r0s"] = np.where(A["r0"] > 0, "dayup", "daydown")
    out["by_side_r0"] = A.groupby(["side", "r0s"]).apply(summ)
    A["t60"] = np.where(A["r60"] > 0, "60up", "60down")
    out["by_side_r60"] = A.groupby(["side", "t60"]).apply(summ)
    A["r5s"] = pd.qcut(A["r5"], 3, labels=["r5lo", "r5mid", "r5hi"])
    out["by_side_r5"] = A.groupby(["side", "r5s"]).apply(summ)
    out["by_window"] = A.groupby("wn").apply(summ)
    out["by_coin"] = A.groupby("coin").apply(summ)
    # holding length: consecutive bars in position
    out["share_bars_pos"] = float((X["a"].abs() > 1e-9).mean())
    out["mean_abs_alloc_in_pos"] = float(A["a"].abs().mean())
    return out
