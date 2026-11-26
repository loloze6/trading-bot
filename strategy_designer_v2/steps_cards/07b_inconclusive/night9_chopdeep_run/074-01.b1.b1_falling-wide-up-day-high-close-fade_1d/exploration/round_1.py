def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            rs.append(pd.Series(c[1:]/c[:-1]-1))
        drift[coin] = pd.concat(rs).mean() if rs else 0.0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df)
            rng = h - l
            mr = pd.Series(rng).rolling(20, min_periods=20).mean().values
            ret = pd.Series(c).pct_change().values
            vol30 = pd.Series(ret).rolling(30).std()
            volpct = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True).values
            r60 = pd.Series(c).pct_change(60).values
            for t in range(n):
                if df["regime"].iat[t] != "mean_reversion": continue
                f = df["forecast"].iat[t]
                if not (f <= -2): continue
                rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iat[t]).year,
                       "f": f, "day": pd.Timestamp(df["timestamp"].iat[t]).floor("D"),
                       "cl": (c[t]-l[t])/rng[t] if rng[t] > 0 else np.nan,
                       "width": rng[t]/mr[t] if mr[t] > 0 else np.nan,
                       "ret1d": ret[t], "r60": r60[t], "volpct": volpct[t],
                       "wd": pd.Timestamp(df["timestamp"].iat[t]).weekday()}
                for hh in [1, 2, 3, 5]:
                    rec[f"x{hh}"] = (-(c[t+hh]/c[t]-1) + hh*drift[coin]) if t+hh < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="x1"):
        x = g[col].dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": x.mean(), "t": np.nan, "hit": np.nan})
        dd = g.dropna(subset=[col]).groupby("day")[col].sum() - g.dropna(subset=[col]).groupby("day")[col].size()*x.mean()
        G = len(dd); se = np.sqrt((dd**2).sum()*G/(G-1))/len(x) if G > 1 else np.nan
        return pd.Series({"n": len(x), "days": G, "mean": x.mean(), "t": x.mean()/se if se else np.nan, "median": x.median(), "hit": (x > 0).mean()})
    out = {}
    out["all"] = pd.DataFrame({h: summ(d, h) for h in ["x1", "x2", "x3", "x5"]}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].abs(), 4, labels=False, duplicates="drop")
    out["by_absf_q"] = d.groupby("fq").apply(summ)
    d["clq"] = pd.qcut(d["cl"], 4, labels=False, duplicates="drop")
    out["by_closeloc_q"] = d.groupby("clq").apply(summ)
    d["wq"] = pd.qcut(d["width"], 4, labels=False, duplicates="drop")
    out["by_width_q"] = d.groupby("wq").apply(summ)
    d["rq"] = pd.qcut(d["ret1d"], 4, labels=False, duplicates="drop")
    out["by_dayret_q"] = d.groupby("rq").apply(summ)
    d["agit"] = np.where(d["volpct"] > 0.5, "agitated", np.where(d["volpct"].notna(), "calm", "na"))
    out["by_agitation"] = d.groupby("agit").apply(summ)
    d["tq"] = pd.qcut(d["r60"], 3, labels=False, duplicates="drop")
    out["by_r60_tercile"] = d.groupby("tq").apply(summ)
    out["corr"] = pd.Series({k: stats.spearmanr(d[k], d["x1"], nan_policy="omit")[0] for k in ["cl", "width", "ret1d", "r60", "f"]})
    xx = d["x1"].dropna()
    out["tail"] = pd.Series({"trim5_mean": stats.trim_mean(xx, 0.05), "max": xx.max(), "min": xx.min(), "std": xx.std()})
    return out
