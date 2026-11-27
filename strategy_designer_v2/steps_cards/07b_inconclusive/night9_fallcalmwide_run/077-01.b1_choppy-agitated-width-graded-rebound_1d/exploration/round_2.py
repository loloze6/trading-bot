def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        rets = [pd.Series(b["close"].astype(float).values[1:] / b["close"].astype(float).values[:-1] - 1) for b in ws.values()]
        drift[coin] = pd.concat(rets).mean()
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values; h = b["high"].astype(float).values; l = b["low"].astype(float).values
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            mr = pd.Series(rng).rolling(30, min_periods=30).mean().values
            r1 = pd.Series(c).pct_change().values
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            n = len(c)
            nx = np.array([c[t+1]/c[t]-1 if t+1 < n else np.nan for t in range(n)])
            df = pd.DataFrame(dict(coin=coin, w=w, f=b["forecast"].astype(float).values, loc=loc,
                                   width=rng/mr, ris=(rng/c)/sd30, r1=nx,
                                   day=pd.to_datetime(b["timestamp"]).dt.floor("D"),
                                   year=pd.to_datetime(b["timestamp"]).dt.year))
            rows.append(df)
    df = pd.concat(rows, ignore_index=True)
    df["x1"] = df["r1"] - df["coin"].map(drift)
    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(n=len(g), days=np.nan, mean=np.nan, t=np.nan))
        s = g.groupby("day")[col].apply(lambda v: (v - g[col].mean()).sum())
        D = len(s); se = np.sqrt((s**2).sum()*D/max(D-1,1))/len(g)
        return pd.Series(dict(n=len(g), days=D, mean=g[col].mean(), t=g[col].mean()/se))
    cases = df[(df.f > 0)].dropna(subset=["x1"]).copy()
    out = {}
    cases["closeness"] = 0.5 - cases["loc"]
    for k in ("closeness", "ris", "width"):
        r, p = stats.spearmanr(cases[k], cases["x1"], nan_policy="omit")
        out[f"spearman_{k}"] = pd.Series(dict(rho=r, p=p, n=len(cases)))
    cases["loch"] = np.where(cases["loc"] < 0.25, "loc<0.25", "loc>=0.25")
    out["by_loc_half"] = cases.groupby("loch").apply(summ).round(4)
    out["low_loc_by_year"] = cases[cases["loc"] < 0.25].groupby("year").apply(summ).round(4)
    out["high_loc_by_year"] = cases[cases["loc"] >= 0.25].groupby("year").apply(summ).round(4)
    out["low_loc_by_coin"] = cases[cases["loc"] < 0.25].groupby("coin").apply(summ).round(4)
    # loc-weighted mean: weight by closeness
    wgt = cases["closeness"].clip(lower=0)
    out["closeness_weighted_mean_x1"] = float((cases["x1"]*wgt).sum()/wgt.sum())
    out["plain_mean_x1"] = float(cases["x1"].mean())
    # width within low-loc cases
    lo = cases[cases["loc"] < 0.25]
    r, p = stats.spearmanr(lo["ris"], lo["x1"])
    out["spearman_ris_in_lowloc"] = pd.Series(dict(rho=r, p=p, n=len(lo)))
    # all profiles: wide low closes graded by loc
    wide = df[(df.width >= 1) & (df["loc"] < 0.5)].dropna(subset=["x1"]).copy()
    wide["lq"] = pd.cut(wide["loc"], [0, 0.1, 0.25, 0.5], include_lowest=True)
    out["all_profiles_wide_low_by_loc"] = wide.groupby("lq").apply(summ).round(4)
    return out
