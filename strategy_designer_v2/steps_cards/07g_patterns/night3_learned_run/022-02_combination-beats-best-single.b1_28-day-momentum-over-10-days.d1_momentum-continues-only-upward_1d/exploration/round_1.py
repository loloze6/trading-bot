import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 10
    rows = []
    usual = {}
    for coin, wins in data["bars"].items():
        g10 = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            raw = b.get("debug_info.components.mom28.last_history_value")
            r28c = c / c.shift(28) - 1
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "r28": r28c,
                "r1": r,
                "r5": c / c.shift(5) - 1,
                "r90": c / c.shift(90) - 1,
                "vol20": r.rolling(20).std(),
                "near60": c / c.rolling(60).max() - 1,
                "range1": (b["high"] - b["low"]) / c,
                "volu": np.log(b["volume"].replace(0, np.nan) / b["volume"].rolling(20).mean()),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1,
            })
            f["volchg"] = f["vol20"] / r.rolling(60).std()
            grid = f.iloc[::H]
            grid = grid[grid["fwd"].notna()]
            rows.append(grid)
            g10.append(grid["fwd"])
        g10 = pd.concat(g10)
        usual[coin] = (g10.mean(), g10.std())
    d = pd.concat(rows, ignore_index=True)
    d["drift"] = d["coin"].map(lambda k: usual[k][0])
    d["sd"] = d["coin"].map(lambda k: usual[k][1])
    d["ex"] = d["fwd"] - d["drift"]
    d["st"] = d["ex"] / d["sd"]
    out = {}
    feats = ["r28", "r1", "r5", "r90", "vol20", "near60", "range1", "volu", "volchg"]
    summ = []
    for ft in feats:
        x = d[[ft, "st", "coin"]].dropna().copy()
        x["z"] = x.groupby("coin")[ft].transform(lambda s: (s - s.mean()) / s.std())
        x["q"] = x.groupby("coin")[ft].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        sl = stats.linregress(x["z"], x["st"])
        qm = x.groupby("q")["st"].mean()
        summ.append({"feat": ft, "n": len(x), "slope": sl.slope, "t": sl.slope / sl.stderr,
                     **{f"q{int(k)+1}": v for k, v in qm.items()}})
    out["feature_strength_by_quintile"] = pd.DataFrame(summ).round(4)
    # falls side only (forecast 0 region)
    sub = d[d["r28"] < 0].dropna(subset=["r28", "st"]).copy()
    sub["z"] = sub.groupby("coin")["r28"].transform(lambda s: (s - s.mean()) / s.std())
    sl = stats.linregress(sub["z"], sub["st"])
    out["fall_side_slope"] = pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr,
                                       "mean_st": sub["st"].mean(), "t_mean": stats.ttest_1samp(sub["st"], 0).statistic})
    # rise side split by vol level
    rs = d[(d["r28"] > 0)].dropna(subset=["vol20", "st"]).copy()
    rs["vq"] = rs.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["rise_side_by_vol_tercile"] = rs.groupby("vq")["st"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))]).round(4)
    out["by_weekday_st"] = d.groupby("wd")["st"].agg(["count", "mean"]).round(4)
    out["by_coin_r28_t"] = d.dropna(subset=["r28"]).groupby("coin").apply(
        lambda x: pd.Series({"n": len(x), "t": stats.linregress(x["r28"], x["st"]).rvalue * np.sqrt((len(x) - 2) / (1 - stats.linregress(x["r28"], x["st"]).rvalue ** 2))})).round(3)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd, ignore_index=True)
    out["book_vs_coin_daily"] = pd.Series({"book_mean": dd["book_return"].mean(), "coin_mean": dd["coin_return"].mean(),
                                          "corr": dd[["book_return", "coin_return"]].corr().iloc[0, 1]})
    return out
