import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; H = 5
    rows = []
    for coin, wins in bars.items():
        allg = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({"coin": coin, "win": w, "ts": ts, "yr": ts.dt.year,
                "fc": b["forecast"].astype(float),
                "raw": b["debug_info.components.support_cluster.last_history_value"].astype(float),
                "pos20": (c - b["low"].rolling(20).min()) / (b["high"].rolling(20).max() - b["low"].rolling(20).min()),
                "ret20": c / c.shift(20) - 1,
                "wd": ts.dt.weekday, "fwd5": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1})
            f["grid5"] = (np.arange(len(f)) % H == 0)
            allg.append(f)
        df = pd.concat(allg, ignore_index=True)
        df["ex5"] = df.fwd5 - df[df.grid5].fwd5.mean()
        df["ex1"] = df.fwd1 - df.fwd1.mean()
        df["fcq"] = np.nan
        nz = df.fc < 0
        df.loc[nz, "fcq"] = pd.qcut(df.loc[nz, "fc"].rank(method="first"), 5, labels=False)
        df["p20q"] = pd.qcut(df.pos20.rank(method="first"), 5, labels=False)
        rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.grid5 & D.ex5.notna()]
    out = {}
    # strongest-short fifth vs rest: per coin, per year, and date-clustered
    top = G[G.fcq == 0]
    out["top_short_fifth_by_coin"] = top.groupby("coin").ex5.agg(["mean", "count"]).round(4)
    out["top_short_fifth_by_year"] = top.groupby("yr").ex5.agg(["mean", "count"]).round(4)
    dm = top.groupby("ts").ex5.mean()
    out["top_short_fifth_date_clustered"] = pd.Series({"mean": dm.mean(), "n_dates": len(dm),
        "t": dm.mean() / (dm.std() / np.sqrt(len(dm)))}).round(4)
    # raw count: within non-zero, convexity by raw value fifth
    nzG = G[G.fc < 0].dropna(subset=["raw"]).copy()
    nzG["rq"] = nzG.groupby("coin").raw.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["raw_fifth_ex5"] = nzG.groupby("rq").agg(raw_mean=("raw", "mean"), ex5=("ex5", "mean"), n=("ex5", "count")).round(4)
    # pos20 date-clustered and by coin
    g = G.dropna(subset=["pos20"])
    pc = g.groupby("coin").apply(lambda x: pd.Series({"corr": x[["pos20", "ex5"]].corr().iloc[0, 1],
        "top_minus_bottom": x[x.p20q == 4].ex5.mean() - x[x.p20q == 0].ex5.mean()})).round(4)
    out["pos20_by_coin"] = pc
    spread = g[g.p20q == 4].groupby("ts").ex5.mean().sub(g[g.p20q == 0].groupby("ts").ex5.mean()).dropna()
    hi = g[g.p20q >= 3].groupby("ts").ex5.mean(); lo = g[g.p20q <= 1].groupby("ts").ex5.mean()
    out["pos20_date_clustered"] = pd.Series({"hi_mean": hi.mean(), "lo_mean": lo.mean(),
        "welch_t": stats.ttest_ind(hi, lo, equal_var=False).statistic, "n_hi": len(hi), "n_lo": len(lo)}).round(4)
    out["pos20_by_year_hi_minus_lo"] = g.groupby("yr").apply(lambda x: x[x.p20q >= 3].ex5.mean() - x[x.p20q <= 1].ex5.mean()).round(4)
    # weekday date-clustered and per coin
    d1 = D.dropna(subset=["ex1"])
    wdd = d1.groupby(["ts", "wd"]).ex1.mean().reset_index()
    w = wdd.groupby("wd").ex1.agg(["mean", "count", "std"]); w["t"] = w["mean"] / (w["std"] / np.sqrt(w["count"]))
    out["weekday_date_clustered"] = w.round(5)
    out["weekday_by_coin_mean_bps"] = (d1.groupby(["coin", "wd"]).ex1.mean().unstack() * 1e4).round(1)
    out["fri_minus_wed_by_year_bps"] = (d1.groupby("yr").apply(lambda x: x[x.wd == 4].ex1.mean() - x[x.wd == 2].ex1.mean()) * 1e4).round(1)
    return out
