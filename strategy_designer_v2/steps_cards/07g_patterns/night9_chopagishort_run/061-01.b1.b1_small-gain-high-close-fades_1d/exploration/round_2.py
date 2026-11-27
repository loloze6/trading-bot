def explore(data):
    import numpy as np, pandas as pd
    H = 5
    recs = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            reg = b["regime"].astype(str).values
            r1 = pd.Series(c).pct_change().values
            absr = pd.Series(np.abs(r1)).rolling(30, min_periods=10).mean().values
            ts = pd.to_datetime(b["timestamp"])
            rng = h - l
            cl = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            for t in range(n - 1):
                cell = t // H
                f5 = c[min(t + H, n - 1)] / c[t] - 1 if t + H < n else np.nan
                f2 = c[t + 2] / c[t] - 1 if t + 2 < n else np.nan
                recs.append(dict(coin=coin, w=w, cell=cell, t=t, day=str(ts[t].date()),
                                 inprof=(reg[t] != "chop"), cl=cl[t],
                                 sr=r1[t] / absr[t] if absr[t] > 0 else np.nan,
                                 f5=f5, f2=f2, grid=(t % H == 0)))
    df = pd.DataFrame(recs)
    g = df[df["grid"]].dropna(subset=["f5"])
    drift5 = g.groupby("coin")["f5"].mean(); usual5 = g.groupby("coin")["f5"].std()
    drift2 = df[df["t"] % 2 == 0].groupby("coin")["f2"].mean()
    df["u5"] = df["f5"] - df["coin"].map(drift5)
    df["s5"] = df["u5"] / df["coin"].map(usual5)
    df["u2"] = df["f2"] - df["coin"].map(drift2)

    def cases(mask):
        x = df[mask].dropna(subset=["u5"])
        return x.sort_values("t").groupby(["coin", "w", "cell"]).head(1)

    def tday(x, col="u5"):
        x = x.dropna(subset=[col]); N = len(x); D = x["day"].nunique()
        if N < 5 or D < 3: return pd.Series(dict(n=N, days=D, mean=np.nan, t=np.nan))
        m = x[col].mean(); rd = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((rd ** 2).sum() * D / (D - 1)) / N
        return pd.Series(dict(n=N, days=D, mean=m, t=m / se))

    out = {}
    out["share_bars_in_profile"] = float(df["inprof"].mean())
    rows = {}
    bins = [(-.01, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)]
    for prof in [True, False]:
        for lo, hi in bins:
            x = cases((df["inprof"] == prof) & (df["cl"] > lo) & (df["cl"] <= hi))
            rows[f"{'in' if prof else 'out'} cl({lo},{hi}] 5d"] = tday(x)
    out["close_loc_by_profile_5d"] = pd.DataFrame(rows).T
    rows = {}
    for prof in [True, False]:
        for lo, hi in bins:
            x = df[(df["inprof"] == prof) & (df["cl"] > lo) & (df["cl"] <= hi) & (df["t"] % 2 == 0)]
            rows[f"{'in' if prof else 'out'} cl({lo},{hi}] 2d"] = tday(x, "u2")
    out["close_loc_by_profile_2d"] = pd.DataFrame(rows).T
    hc = cases(df["inprof"] & (df["cl"] >= .8)).dropna(subset=["sr"])
    out["inprof_hiclose_by_sr"] = hc.groupby(pd.qcut(hc["sr"], 3)).apply(tday)
    lc = cases(df["inprof"] & (df["cl"] <= .2)).dropna(subset=["sr"])
    if len(lc) > 15:
        out["inprof_loclose_by_sr"] = lc.groupby(pd.qcut(lc["sr"], 2)).apply(tday)
    ip = cases(df["inprof"]).dropna(subset=["cl"])
    out["inprof_corr_cl_u5"] = pd.Series(dict(n=len(ip), rho=ip[["cl", "u5"]].corr(method="spearman").iloc[0, 1]))
    # book's best and worst days
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    act = D[D["book_return"].abs() > 0]
    out["book_active_days"] = pd.Series(dict(n=len(act), mean=act["book_return"].mean(),
                                             corr_coin=act[["book_return", "coin_return"]].corr().iloc[0, 1]))
    return out
