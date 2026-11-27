def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}; vmed = {}
    for coin, wins in bars.items():
        rs = []; vs = []
        for w, df in wins.items():
            c = df["close"].values
            r = pd.Series(c[1:]/c[:-1]-1)
            rs.append(r); vs.append(r.rolling(30).std())
        drift[coin] = pd.concat(rs).mean()
        vmed[coin] = pd.concat(vs).median()
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df); rng = h - l
            mr = pd.Series(rng).rolling(20, min_periods=20).mean().values
            ret = pd.Series(c).pct_change()
            v30 = ret.rolling(30).std().values
            for t in range(n - 1):
                if df["regime"].iat[t] != "mean_reversion": continue
                if not (df["forecast"].iat[t] <= -2): continue
                ts = pd.Timestamp(df["timestamp"].iat[t])
                rows.append({"coin": coin, "win": w, "year": ts.year, "day": ts.floor("D"),
                             "cl": (c[t]-l[t])/rng[t] if rng[t] > 0 else np.nan,
                             "width": rng[t]/mr[t] if mr[t] > 0 else np.nan,
                             "v30rel": v30[t]/vmed[coin] if not np.isnan(v30[t]) else np.nan,
                             "x1": -(c[t+1]/c[t]-1) + drift[coin]})
    d = pd.DataFrame(rows).dropna(subset=["width", "x1"])
    def summ(g, col="x1"):
        x = g[col].dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": x.mean()})
        dd = g.groupby("day")[col].sum() - g.groupby("day")[col].size()*x.mean()
        G = len(dd); se = np.sqrt((dd**2).sum()*G/(G-1))/len(x)
        return pd.Series({"n": len(x), "days": G, "mean": x.mean(), "t": x.mean()/se, "median": x.median(), "hit": (x > 0).mean()})
    out = {}
    med = d["width"].median()
    d["wide"] = np.where(d["width"] > med, "upper", "lower")
    out["width_median"] = med
    out["width_half"] = d.groupby("wide").apply(summ)
    a, b = d.loc[d.wide == "upper", "x1"], d.loc[d.wide == "lower", "x1"]
    out["upper_minus_lower"] = pd.Series({"diff": a.mean()-b.mean(), "welch_t": stats.ttest_ind(a, b, equal_var=False)[1] if False else stats.ttest_ind(a, b, equal_var=False)[0]})
    out["width_half_by_year"] = d.groupby(["wide", "year"]).apply(summ)
    d["wq5"] = pd.qcut(d["width"], 5, labels=False, duplicates="drop")
    out["width_quintile"] = d.groupby("wq5").apply(summ)
    out["width_q_range"] = d.groupby("wq5")["width"].agg(["min", "max"])
    sr = stats.spearmanr(d["width"], d["x1"])
    out["spearman_width"] = pd.Series({"rho": sr[0], "p": sr[1]})
    d["clh"] = np.where(d["cl"] > d["cl"].median(), "nearhigh", "nearlow")
    out["width_x_cl"] = d.groupby(["wide", "clh"]).apply(summ)
    d["ag"] = np.where(d["v30rel"] > 1, "agit", np.where(d["v30rel"].notna(), "calm", "na"))
    out["agit_proxy"] = d.groupby("ag").apply(summ)
    out["agit_x_width"] = d.groupby(["ag", "wide"]).apply(summ)
    # trimmed: drop the single worst case
    out["upper_wo_extremes"] = pd.Series({"trim5": stats.trim_mean(a, 0.05), "lower_trim5": stats.trim_mean(b, 0.05)})
    return out
