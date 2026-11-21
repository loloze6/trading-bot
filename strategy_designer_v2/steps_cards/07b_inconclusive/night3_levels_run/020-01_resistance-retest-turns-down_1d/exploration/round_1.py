import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            raw = df.get("debug_info.components.resistance.last_history_value", pd.Series(np.nan, index=df.index)).values
            fc = df["forecast"].values
            r30 = pd.Series(c).pct_change(30).values
            ma90 = pd.Series(c).rolling(90, min_periods=30).mean().values
            for i in range(0, n, 5):
                d = {"coin": coin, "win": w, "year": ts.iloc[i].year, "fc": fc[i], "raw": raw[i],
                     "r30": r30[i], "abovema": (c[i] > ma90[i]) if not np.isnan(ma90[i]) else np.nan}
                for h in H:
                    d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    # drift per coin per horizon from non-overlapping grids of h
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
    for h in H:
        g[f"u{h}"] = g[f"f{h}"] - g["coin"].map(lambda x: drift[(x, h)])
    act = g[g["fc"] < 0].copy()
    act["fbin"] = pd.cut(act["fc"], [-20.01, -15, -10, -5, -1, -0.0001])

    def summ(df, by):
        out = df.groupby(by).agg(n=("u5", "count"), u1=("u1", "mean"), u5=("u5", "mean"),
                                 u10=("u10", "mean"), u20=("u20", "mean"))
        t = df.groupby(by)["u5"].apply(lambda s: s.mean() / (s.std() / np.sqrt(s.count())) if s.count() > 2 else np.nan)
        out["t5"] = t
        return out

    res = {}
    res["by_fbin"] = summ(act, "fbin")
    res["by_coin"] = summ(act, "coin")
    res["by_year"] = summ(act, "year")
    act["trend"] = act["abovema"].map({True: "above_ma90", False: "below_ma90"})
    res["by_trend"] = summ(act, "trend")
    act["r30b"] = pd.qcut(act["r30"], 4, labels=["q1_low", "q2", "q3", "q4_high"])
    res["by_r30"] = summ(act, "r30b")
    # all grid bars, forecast zero vs active
    g["state"] = np.where(g["fc"] < 0, "active", np.where(g["fc"] == 0, "zero", "other"))
    res["active_vs_zero"] = summ(g, "state")
    # slopes per horizon
    sl = {}
    for h in H:
        s = act.dropna(subset=[f"u{h}", "fc"])
        lr = stats.linregress(s["fc"], s[f"u{h}"])
        sl[f"h{h}"] = pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(s)})
    res["slope_by_h"] = pd.DataFrame(sl).T
    # raw component quantiles across all grid bars with raw
    gr = g.dropna(subset=["raw"]).copy()
    gr["rawq"] = pd.qcut(gr["raw"].rank(method="first"), 5, labels=["q1", "q2", "q3", "q4", "q5"])
    res["by_raw_quintile"] = summ(gr, "rawq")
    return res
