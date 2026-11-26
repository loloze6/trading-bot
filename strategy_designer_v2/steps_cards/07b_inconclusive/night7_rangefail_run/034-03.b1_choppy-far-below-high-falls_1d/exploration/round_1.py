import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 3, 5, 10, 20]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            ret1 = pd.Series(c).pct_change()
            vol20 = ret1.rolling(20).std().values
            hi20 = pd.Series(c).shift(1).rolling(20).max().values
            raw = (c - hi20) / hi20 / vol20
            r20 = pd.Series(c).pct_change(20).values
            vol60 = ret1.rolling(60).std().values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0, n, 5):
                d = {"coin": coin, "w": w, "i": i, "yr": yr[i],
                     "reg": b["regime"].iloc[i], "fc": b["forecast"].iloc[i],
                     "raw": raw[i], "r20": r20[i], "agit": vol20[i] / vol60[i] if vol60[i] > 0 else np.nan,
                     "day": str(b["timestamp"].iloc[i])[:10]}
                for h in H:
                    d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    # coin drift per horizon over all grid rows (non-overlapping for h=5 only; approx for others)
    for h in H:
        df[f"a{h}"] = df[f"f{h}"] - df.groupby("coin")[f"f{h}"].transform("mean")
    ch = df[df.reg == "unknown"].copy()
    below = ch[ch.raw < 0].copy()
    out = {}
    out["counts"] = pd.Series({"grid": len(df), "choppy": len(ch), "choppy_below": len(below),
                               "choppy_at_high": int((ch.raw >= 0).sum())})
    below["q"] = pd.qcut(below["raw"], 5, labels=["deep1", "q2", "q3", "q4", "shallow5"])
    def tstat(x):
        x = x.dropna(); return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    g = below.groupby("q", observed=True)
    out["by_depth_quintile_adj"] = pd.DataFrame({h: g[f"a{h}"].mean() for h in H}).assign(n=g.size(), raw_mean=g["raw"].mean(), t5=g["a5"].apply(tstat))
    at = ch[ch.raw >= 0]
    out["choppy_at_or_above_high_adj"] = pd.Series({f"a{h}": at[f"a{h}"].mean() for h in H} | {"n": len(at), "t5": tstat(at["a5"])})
    out["all_below_adj"] = pd.Series({f"a{h}": below[f"a{h}"].mean() for h in H} | {f"t{h}": tstat(below[f"a{h}"]) for h in H})
    gc = below.groupby("coin")
    out["by_coin"] = pd.DataFrame({"n": gc.size(), "a5": gc["a5"].mean(), "a10": gc["a10"].mean(),
                                   "corr_raw_a5": gc.apply(lambda x: x["raw"].corr(x["a5"]))})
    gy = below.groupby("yr")
    out["by_year"] = pd.DataFrame({"n": gy.size(), "a5": gy["a5"].mean(), "a10": gy["a10"].mean(),
                                   "corr_raw_a5": gy.apply(lambda x: x["raw"].corr(x["a5"]))})
    gw = below.groupby("w")
    out["by_window"] = pd.DataFrame({"n": gw.size(), "a5": gw["a5"].mean(),
                                     "corr_raw_a5": gw.apply(lambda x: x["raw"].corr(x["a5"]))})
    below["agq"] = pd.qcut(below["agit"], 2, labels=["calm", "agit"])
    below["tr"] = np.where(below["r20"] > 0, "r20up", "r20down")
    ga = below.groupby(["agq", "tr"], observed=True)
    out["by_agit_r20"] = pd.DataFrame({"n": ga.size(), "a5": ga["a5"].mean(), "a10": ga["a10"].mean(), "t5": ga["a5"].apply(tstat),
                                       "corr_raw_a5": ga.apply(lambda x: x["raw"].corr(x["a5"]))})
    # slope by horizon, raw depth vs adj return
    sl = {}
    for h in H:
        x = below[["raw", f"a{h}"]].dropna()
        r = stats.linregress(x["raw"], x[f"a{h}"])
        sl[h] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(x)}
    out["slope_raw_by_h"] = pd.DataFrame(sl).T
    x = below[["fc", "a5"]].dropna(); x = x[x.fc < 0]
    r = stats.linregress(x["fc"], x["a5"])
    out["slope_fc_a5"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(x)})
    return out
