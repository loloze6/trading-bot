import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["forecast"].astype(float),
                "r1": r1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "r60": c / c.shift(60) - 1,
                "vol20": r1.rolling(20).std(),
                "vol60": r1.rolling(60).std(),
                "rngrel": rng / rng.rolling(20).mean(),
                "body": (c - o).abs() / (hi - lo).replace(0, np.nan),
                "clv": ((c - lo) - (hi - c)) / (hi - lo).replace(0, np.nan),
                "dow": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "pos": np.arange(len(b)),
            })
            df["s20"] = df["r20"] / (df["vol20"] * np.sqrt(20))
            df["volratio"] = df["vol20"] / df["vol60"]
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    out = {}
    feats = ["s20", "r5", "r20", "r60", "r1", "vol20", "volratio", "rngrel", "body", "clv", "fc"]
    res = []
    for f in feats:
        d = G[[f, "ex"]].dropna()
        sl = stats.linregress(d[f], d["ex"])
        res.append([f, len(d), sl.slope, sl.slope / sl.stderr, d[f].corr(d["ex"], method="spearman")])
    out["grid_slopes_ex10"] = pd.DataFrame(res, columns=["feat", "n", "slope", "t", "spearman"])
    def qtab(f, q=5):
        d = G[[f, "ex", "fwd"]].dropna().copy()
        d["q"] = pd.qcut(d[f], q, labels=False, duplicates="drop")
        t = d.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), mean_fwd=("fwd", "mean"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")
    for f in ["s20", "r60", "vol20", "volratio", "r5"]:
        out["q_" + f] = qtab(f)
    # brief: wide-flat day after a run, graded by rngrel, run-signed forward
    d = G.dropna(subset=["r5", "rngrel", "body"]).copy()
    d["runsign"] = np.sign(d["r5"])
    d["ex_run"] = d["ex"] * d["runsign"]
    d["flat"] = d["body"] < 0.3
    d["wide"] = pd.qcut(d["rngrel"], 3, labels=["narrow", "mid", "wide"])
    t = d.groupby(["flat", "wide"]).agg(n=("ex_run", "size"), m=("ex_run", "mean"), sd=("ex_run", "std"))
    t["t"] = t["m"] / (t["sd"] / np.sqrt(t["n"]))
    out["brief_runsigned_ex"] = t.drop(columns="sd")
    # year
    t = G.groupby("year").agg(n=("ex", "size"), fwd=("fwd", "mean"))
    out["year_fwd"] = t
    # weekday daily returns
    D = A.dropna(subset=["fwd1"])
    t = D.groupby("dow")["fwd1"].agg(["size", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["size"]))
    out["dow_next_day"] = t.drop(columns="std")
    # next-day after large daily moves scaled by vol
    D = D.dropna(subset=["r1", "vol20"]).copy()
    D["z"] = D["r1"] / D["vol20"].shift(0)
    D["zq"] = pd.qcut(D["z"], 7, labels=False)
    t = D.groupby("zq").agg(n=("fwd1", "size"), z=("z", "mean"), m=("fwd1", "mean"), sd=("fwd1", "std"))
    t["t"] = t["m"] / (t["sd"] / np.sqrt(t["n"]))
    out["next_day_by_zmove"] = t.drop(columns="sd")
    # book: daily returns, position, coin
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            br.append(x)
    B = pd.concat(br).dropna()
    out["book_by_coin"] = B.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), sd=("book_return", "std"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t_ in wins.items():
            if len(t_): x = t_.copy(); x["coin"] = coin; tr.append(x)
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["dur_d"], 4, duplicates="drop")
    out["trades_by_duration"] = T.groupby("dq", observed=True)["net_profit_loss_percent"].agg(["size", "mean", "median"])
    T["eq"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("eq", observed=True)["net_profit_loss_percent"].agg(["size", "mean", "median"])
    return out
