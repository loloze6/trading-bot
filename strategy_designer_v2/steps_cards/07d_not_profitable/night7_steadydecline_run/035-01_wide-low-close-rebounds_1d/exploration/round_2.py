def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.copy().reset_index(drop=True)
            b["w"] = w; b["coin"] = c
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["ret2"] = b["close"].shift(-2) / b["close"] - 1
            dr = b["close"].pct_change()
            b["vol30"] = dr.rolling(30).std()
            b["vol90"] = dr.rolling(90, min_periods=60).std()
            b["r60"] = b["close"] / b["close"].shift(60) - 1
            b["raw"] = b["debug_info.components.wide_low_close.last_history_value"]
            b["pp"] = b["debug_info.components.wide_low_close.post_pipeline_value"]
            b["alloc"] = b["postRebalance_current_allocation"]
            # past-only 80th percentile of raw (rolling 120 bars, excluding current)
            b["q80"] = b["raw"].shift(1).rolling(120, min_periods=40).quantile(0.8)
            b["q60"] = b["raw"].shift(1).rolling(120, min_periods=40).quantile(0.6)
            b["toppast"] = b["raw"] > b["q80"]
            b["pos"] = 0
            b["bi"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["drift"] = B.groupby("coin")["ret1"].transform("mean")
    B["ex"] = B["ret1"] - B["drift"]
    B["gain"] = B["alloc"] * B["ret1"]
    B["agit"] = B["vol30"] > B["vol90"]
    cost = 0.0019 / 2
    def book(mask_col, scale="alloc"):
        res = []
        for (c, w), b in B.groupby(["coin", "w"]):
            m = b[mask_col].fillna(False).astype(bool)
            if scale == "alloc":
                pos = np.where(m, b["alloc"], 0.0)
            elif scale == "pp":
                pos = np.where(m, (b["pp"].fillna(0) / 10.0) * (0.382 / np.sqrt(365)) / b["vol30"].fillna(1), 0.0)
                pos = np.clip(pos, 0, 2)
            pos = pd.Series(pos, index=b.index).fillna(0)
            turn = (pos - pos.shift(1).fillna(0)).abs()
            r = pos * b["ret1"].fillna(0) - turn * cost
            res.append(pd.DataFrame({"w": w, "bi": b["bi"], "r": r, "in": pos > 0}))
        R = pd.concat(res)
        d = R.groupby(["w", "bi"])["r"].mean().reset_index()
        d["wn"] = d["w"].str[1:].astype(int)
        d = d.sort_values(["wn", "bi"])
        v = (1 + d["r"]).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(d)) - 1
        lo = min(d[d["wn"] != k]["r"].mean() / d[d["wn"] != k]["r"].std() * np.sqrt(365) for k in d["wn"].unique())
        return {"sharpe": d["r"].mean() / d["r"].std() * np.sqrt(365), "yearly": yr, "maxdd": dd,
                "calmar": yr / -dd, "share_in": R["in"].mean(), "mean_on_in": d["r"].mean() / R["in"].mean(), "loo_min_sharpe": lo}
    B["all"] = True
    B["top_agit"] = B["toppast"] & B["agit"]
    B["top_notrising"] = B["toppast"] & (B["r60"] < 0.1)
    res = {}
    for k in ["all", "toppast", "top_agit", "top_notrising"]:
        res[k] = book(k)
    res["toppast_ppsize"] = book("toppast", "pp")
    out["books"] = pd.DataFrame(res).T
    # signal in past-only top vs not; by agitation, cond alone
    g = B.dropna(subset=["ret1", "q80"]).groupby(["agit", "toppast"])
    out["agit_x_toppast"] = pd.DataFrame({"n": g.size(), "ex%": g["ex"].mean() * 100,
        "t": g["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s)))),
        "ret2%": g["ret2"].mean() * 100})
    # within top: graded? raw tertiles inside toppast
    T = B[B["toppast"]].dropna(subset=["ret1"]).copy()
    T["exc"] = T["raw"] / T["q80"]
    T["g"] = pd.qcut(T["exc"], 3, labels=False)
    g = T.groupby("g")
    out["inside_top_graded"] = pd.DataFrame({"n": g.size(), "ex%": g["ex"].mean() * 100,
        "t": g["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))})
    # where does the recorded book lose: gain on top vs non-top bars by agitation
    g = B.dropna(subset=["ret1"]).groupby(["toppast"])
    out["gain_split_recorded"] = pd.DataFrame({"n": g.size(), "sum_gain": g["gain"].sum(), "mean_alloc": g["alloc"].mean()})
    return out
