import pandas as pd, numpy as np
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o = b["open"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z": r / sd,
                "rng": (h - l) / c / sd,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "body": (c - o).abs() / (h - l).replace(0, np.nan),
                "run5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "sd": sd,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift1 = D.groupby("coin")["f1"].mean()
    drift3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift1)
    D["x3"] = D["f3"] - D["coin"].map(drift3)
    D3 = D[D.pos % 3 == 0]

    def tab(df, key, col):
        g = df.dropna(subset=[key, col]).groupby(key)[col]
        out = pd.DataFrame({"n": g.size(), "mean%": g.mean() * 100, "t": g.apply(_t)})
        # coins with positive mean
        pc = df.dropna(subset=[key, col]).groupby([key, "coin"])[col].mean().gt(0).groupby(level=0).sum()
        out["coins+"] = pc
        return out.round(3)

    D["zb"] = pd.cut(D["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    D3 = D[D.pos % 3 == 0].copy(); D3["zb"] = pd.cut(D3["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    D["rq"] = pd.qcut(D["rng"], 5, labels=False)
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False)
    D["sdq"] = D.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    D3 = D[D.pos % 3 == 0].copy(); D3["zb"] = pd.cut(D3["z"], [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    D3["rq"] = D.loc[D3.index, "rq"]

    # brief's own setup: run (|run5| large), wide range, flat body
    D["run"] = np.sign(D["run5"]) * (D["run5"].abs() > 1)
    D["xr1"] = D["x1"] * -D["run"]  # move against the run
    wf = D[(D.run != 0)].copy()
    wf["wide"] = np.where(wf["rq"] >= 3, "wide", np.where(wf["rq"] <= 1, "narrow", "mid"))
    wf["flat"] = np.where(wf["body"] < 0.3, "flat", "body")
    brief = wf.dropna(subset=["xr1"]).groupby(["wide", "flat"])["xr1"].agg(["size", "mean", _t])

    # z bucket conditioned on vol level
    zsd = D[D.z <= -1].dropna(subset=["x1"]).groupby("sdq")["x1"].agg(["size", "mean", _t])

    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, win=w))
    B = pd.concat(bk)
    Bd = B.groupby(["win", "day"])["book_return"].mean().dropna()
    q = Bd.quantile([0.02, 0.98])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    T["fq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    tr = T.groupby("fq")["net_profit_loss_percent"].agg(["size", "mean", _t])
    trc = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", _t])

    return {
        "x1 by z bucket": tab(D, "zb", "x1"),
        "x3 by z bucket (grid3)": tab(D3, "zb", "x3"),
        "x1 by range quintile": tab(D, "rq", "x1"),
        "x3 by range quintile (grid3)": tab(D3, "rq", "x3"),
        "x1 by clv quintile": tab(D, "clvq", "x1"),
        "x1 by vol quintile (own coin)": tab(D, "sdq", "x1"),
        "x1 by weekday": tab(D, "wd", "x1"),
        "x1 by year": tab(D, "yr", "x1"),
        "brief: move against run, x1": brief.round(5),
        "x1 after z<=-1 by vol quintile": zsd.round(5),
        "corr z with next x1 by coin": D.groupby("coin").apply(lambda g: g["z"].corr(g["x1"])).round(4),
        "book day ret tails": pd.Series({"q02": q.iloc[0], "q98": q.iloc[1], "n": len(Bd), "mean": Bd.mean(), "t": _t(Bd)}),
        "trades by entry forecast quartile": tr.round(4),
        "trades by coin": trc.round(4),
    }
