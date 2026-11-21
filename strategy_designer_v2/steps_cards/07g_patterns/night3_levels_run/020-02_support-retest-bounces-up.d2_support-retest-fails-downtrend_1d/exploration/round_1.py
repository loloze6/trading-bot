import pandas as pd, numpy as np
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

def explore(data):
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            fwd = c.shift(-H) / c - 1
            f1 = c.shift(-1) / c - 1
            lr = np.log(c).diff()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": fwd,
                "r1": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": lr.rolling(20).std(),
                "dlow30": c / c.rolling(30).min() - 1,
                "dhigh30": c / c.rolling(30).max() - 1,
                "brk20": c / c.shift(1).rolling(20).min() - 1,   # negative = close below prior 20d low
                "brkh20": c / c.shift(1).rolling(20).max() - 1,  # positive = close above prior 20d high
                "rng": (b["high"] - b["low"]) / c,
                "volz": b["volume"] / b["volume"].rolling(20).mean(),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            d["pos"] = np.arange(len(d))
            g = d[(d["pos"] % H == 0)].copy()
            grid.append(g)
            dd = pd.DataFrame({"coin": coin, "f1": f1, "wd": d["wd"], "r1": d["r1"],
                               "absr1z": (d["r1"].abs() / d["vol20"]), "r1s": np.sign(d["r1"])})
            daily.append(dd)
        g = pd.concat(grid)
        m = g["fwd"].mean(); s = g["fwd"].std()
        g["exc"] = g["fwd"] - m
        g["str"] = g["exc"] / s
        rows.append(g)
    G = pd.concat(rows).dropna(subset=["fwd"])
    D = pd.concat(daily).dropna(subset=["f1"])
    out = {}
    def by_q(col, q=5):
        x = G.dropna(subset=[col]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda v: pd.qcut(v.rank(method="first"), q, labels=False))
        r = x.groupby("q").agg(n=("exc", "size"), mean_exc=("exc", "mean"), strength=("str", "mean"),
                               lo=(col, "min"), hi=(col, "max"))
        r["t"] = x.groupby("q")["exc"].apply(_t)
        sp = x.groupby("coin").apply(lambda z: stats.spearmanr(z[col], z["exc"])[0])
        r.loc["spearman_by_coin_mean", "mean_exc"] = sp.mean()
        r.loc["spearman_pos_coins", "mean_exc"] = (sp > 0).sum()
        return r
    for col in ["r5", "r20", "vol20", "dlow30", "dhigh30", "brk20", "brkh20", "rng", "volz"]:
        out["q_" + col] = by_q(col)
    a = G[G["fc"] < 0]
    out["active_vs_not"] = pd.DataFrame({
        "n": [len(a), (G["fc"] == 0).sum()],
        "mean_exc": [a["exc"].mean(), G.loc[G["fc"] == 0, "exc"].mean()],
        "t": [_t(a["exc"]), _t(G.loc[G["fc"] == 0, "exc"])]}, index=["active", "flat"])
    out["active_by_coin"] = a.groupby("coin")["exc"].agg(["size", "mean"])
    wd = D.groupby("wd")["f1"].agg(["size", "mean"])
    wd["t"] = D.groupby("wd")["f1"].apply(lambda v: _t(v - D["f1"].mean()))
    out["weekday_next1d"] = wd
    D["big"] = pd.qcut(D["absr1z"].rank(method="first"), 5, labels=False)
    D["sf1"] = D["f1"] * D["r1s"]
    bm = D.groupby("big")["sf1"].agg(["size", "mean"]); bm["t"] = D.groupby("big")["sf1"].apply(_t)
    out["next1d_signed_by_move_size"] = bm
    return out
