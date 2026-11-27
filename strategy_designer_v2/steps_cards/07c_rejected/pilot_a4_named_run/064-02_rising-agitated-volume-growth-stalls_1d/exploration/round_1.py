import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon over all windows
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].values
            n = len(df)
            vs = pd.Series(v)
            m1 = vs.rolling(30).mean()
            m0 = vs.shift(30).rolling(30).mean()
            lvr = np.log(m1 / m0)
            r5p = pd.Series(c).pct_change(5)
            r30p = pd.Series(c).pct_change(30)
            for i in range(n):
                rec = {"coin": coin, "w": w, "i": i, "inprof": df["regime"].iloc[i] == "unknown",
                       "fc": df["forecast"].iloc[i], "lvr": lvr.iloc[i],
                       "rec": df["debug_info.components.vol_change.last_history_value"].iloc[i] if "debug_info.components.vol_change.last_history_value" in df else np.nan,
                       "r5p": r5p.iloc[i], "r30p": r30p.iloc[i],
                       "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D")}
                for h in (1, 3, 5, 10, 20):
                    rec[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    res = []
    for h in (1, 3, 5, 10, 20):
        g = d[d["i"] % h == 0].copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        p = g[g.inprof & g.lvr.notna() & g.ex.notna()]
        sl = stats.linregress(p["lvr"], p["ex"])
        hi = p[p.lvr > 0]["ex"]; lo = p[p.lvr <= 0]["ex"]
        res.append({"h": h, "n": len(p), "slope_lvr": sl.slope, "t": sl.slope / sl.stderr,
                    "ex_growth": hi.mean(), "n_g": len(hi), "ex_shrink": lo.mean(), "n_s": len(lo),
                    "mean_ex_all_prof": p["ex"].mean(), "t_all": p["ex"].mean() / (p["ex"].std() / np.sqrt(len(p))),
                    "slope_r30": stats.linregress(p["r30p"], p["ex"]).slope,
                    "t_r30": (lambda s: s.slope / s.stderr)(stats.linregress(p["r30p"], p["ex"])),
                    "t_r5p": (lambda s: s.slope / s.stderr)(stats.linregress(p["r5p"].fillna(0), p["ex"]))})
    out["by_horizon"] = pd.DataFrame(res)
    g = d[d["i"] % 5 == 0].copy()
    drift = g.groupby("coin")["f5"].mean()
    g["ex"] = g["f5"] - g["coin"].map(drift)
    p = g[g.inprof & g.lvr.notna() & g.ex.notna()].copy()
    def sl(x):
        if len(x) < 8: return pd.Series({"n": len(x)})
        s = stats.linregress(x["lvr"], x["ex"])
        return pd.Series({"n": len(x), "slope": s.slope, "t": s.slope / s.stderr, "mean_ex": x["ex"].mean(), "mean_raw": x["f5"].mean()})
    out["by_coin"] = p.groupby("coin").apply(sl)
    out["by_year"] = p.groupby("year").apply(sl)
    p["q"] = pd.qcut(p["lvr"], 5, labels=False)
    out["lvr_quintiles"] = p.groupby("q").agg(n=("ex", "size"), lvr=("lvr", "mean"), ex=("ex", "mean"), raw=("f5", "mean"), up_share=("f5", lambda s: (s > 0).mean()))
    p["q30"] = pd.qcut(p["r30p"], 5, labels=False)
    out["r30_quintiles"] = p.groupby("q30").agg(n=("ex", "size"), r30=("r30p", "mean"), ex=("ex", "mean"), raw=("f5", "mean"))
    p["q5"] = pd.qcut(p["r5p"], 5, labels=False)
    out["r5_quintiles"] = p.groupby("q5").agg(n=("ex", "size"), r5=("r5p", "mean"), ex=("ex", "mean"), raw=("f5", "mean"))
    out["corr_rec_lvr"] = float(p[["rec", "lvr"]].corr().iloc[0, 1]) if p["rec"].notna().sum() > 5 else np.nan
    return out
