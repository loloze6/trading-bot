import pandas as pd, numpy as np
from scipy import stats

def summ_s(x):
    x = pd.Series(x).dropna(); n = len(x)
    if n < 3:
        return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "share_pos": np.nan})
    return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)), "share_pos": (x > 0).mean()})

def explore(data):
    bars = data["bars"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(cl)
            r1 = np.full(n, np.nan); r1[1:] = cl[1:]/cl[:-1]-1
            vol = pd.Series(r1).rolling(30, min_periods=15).std().values
            for h in (1, 2, 3):
                for i in range(0, n, h):
                    if i >= 1 and i + h < n:
                        rows.append(dict(coin=c, win=w, h=h, fwd=cl[i+h]/cl[i]-1, r1=r1[i], vol=vol[i],
                                         year=ts.iloc[i].year, wd=ts.iloc[i].dayofweek))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    df["z"] = df["r1"] / df["vol"]
    d1 = df[df.h == 1].dropna(subset=["z"]).copy()
    d1["exs"] = d1["ex"] / d1["vol"]
    d1["zq"] = d1.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["h1_by_zdecile"] = d1.groupby("zq").apply(lambda g: pd.concat([summ_s(g["ex"]), pd.Series({"z": g["z"].mean()})]))
    def slope(g):
        g = g.dropna(subset=["z", "exs"])
        if len(g) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(g)})
        s = stats.linregress(g["z"], g["exs"])
        return pd.Series({"slope": s.slope, "t": s.slope/s.stderr, "n": len(g)})
    out["h1_slope_by_coin"] = d1.groupby("coin").apply(slope)
    out["h1_slope_by_year"] = d1.groupby("year").apply(slope)
    d1["weekend_target"] = d1["wd"].isin([4, 5])
    out["h1_slope_by_targetday_fri_sat"] = d1.groupby("weekend_target").apply(slope)
    d1["neg"] = d1["z"] < 0
    out["h1_slope_down_vs_up_days"] = d1.groupby("neg").apply(slope)
    for h in (2, 3):
        e = df[df.h == h].dropna(subset=["z"]).copy()
        e["exs"] = e["ex"] / (e["vol"] * np.sqrt(h))
        e["zq"] = e.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"h{h}_by_zquintile"] = e.groupby("zq")["ex"].apply(summ_s).unstack()
        out[f"h{h}_slope_all"] = slope(e).to_frame().T
    out["h1_slope_all"] = slope(d1).to_frame().T
    return out
