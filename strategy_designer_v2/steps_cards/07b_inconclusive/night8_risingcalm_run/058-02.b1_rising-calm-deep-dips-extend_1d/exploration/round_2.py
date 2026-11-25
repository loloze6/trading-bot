def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; allg = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c)
            hi5 = pd.Series(c).rolling(5, min_periods=5).max().values
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30, min_periods=20).std().values
            raw = (c - hi5) / hi5 / sd30
            lhv = df.get("debug_info.components.scaled_pullback.last_history_value")
            ts = pd.to_datetime(df["timestamp"])
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    allg.append((coin, h, c[i + h] / c[i] - 1))
            for i in range(0, n - 5, 5):
                rows.append(dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                    regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i], raw=raw[i],
                    lhv=(lhv.iloc[i] if lhv is not None else np.nan),
                    r5=c[i+5]/c[i]-1, r10=(c[i+10]/c[i]-1 if i+10<n else np.nan)))
    d = pd.DataFrame(rows)
    g = pd.DataFrame(allg, columns=["coin","h","ret"]).groupby(["coin","h"])["ret"].mean()
    d["x5"] = d.r5 - d.coin.map(g.xs(5, level="h")); d["x10"] = d.r10 - d.coin.map(g.xs(10, level="h"))
    def slope(s, x, y):
        s = s[[x, y, "day"]].dropna()
        if len(s) < 10: return dict(n=len(s), slope=np.nan, t=np.nan)
        X = s[x].values; Y = s[y].values; Xc = X - X.mean()
        b = (Xc*(Y-Y.mean())).sum()/(Xc**2).sum(); e = Y-Y.mean()-b*Xc
        sc = pd.Series(Xc*e).groupby(s.day.values).sum(); G=len(sc)
        se = np.sqrt((sc**2).sum()/(Xc**2).sum()**2*G/(G-1))
        return dict(n=len(s), days=G, slope=b, t=b/se, meany=s[y].mean())
    rc = d[d.regime=="unknown"]
    out = {}
    res = []
    for lab, sub, x in [("plan: fc<0 on fc", rc[rc.fc<0], "fc"),
                        ("fc<0 on raw", rc[rc.fc<0], "raw"),
                        ("raw<0 on raw", rc[rc.raw<0], "raw"),
                        ("raw<=0 incl highs on raw", rc[rc.raw<=0], "raw"),
                        ("raw<0 on rank raw", rc[rc.raw<0].assign(rk=rc[rc.raw<0].raw.rank(pct=True)), "rk")]:
        for y in ["x5","x10"]:
            res.append(dict(case=lab, y=y, **slope(sub, x, y)))
    out["slopes_variants"] = pd.DataFrame(res).round(4)
    out["fc_vs_raw_corr_in_rc"] = f"{rc[['fc','raw']].dropna().corr().iloc[0,1]:.3f}; share fc<0 among raw<0: {(rc[rc.raw<0].fc<0).mean():.3f}; n fc<0 {int((rc.fc<0).sum())}"
    s = rc[rc.fc<0].copy(); s["q"] = pd.qcut(s.fc.rank(method="first"), 3, labels=["deepest","mid","shallow"])
    out["plan_cases_by_fc_tercile"] = s.groupby("q")[["fc","raw","x5","x10"]].agg(["mean","count"]).round(4)
    s = rc[rc.raw<0].copy(); s["q"] = pd.qcut(s.raw, 4, labels=["deepest","q2","q3","shallow"])
    out["deepest_quartile_by_year_x5"] = s[s.q=="deepest"].groupby("year")["x5"].agg(["mean","count"]).round(4)
    out["deepest_quartile_median_x5_and_t"] = (lambda z: f"median {z.median():.4f}, mean {z.mean():.4f}, t {z.mean()/z.std()*np.sqrt(len(z)):.2f}, n {len(z)}, share<0 {(z<0).mean():.2f}")(s[s.q=="deepest"].x5)
    res = []
    for k, sub in rc[rc.raw<0].groupby("coin"):
        q = sub.raw.rank(pct=True)
        res.append(dict(coin=k, deep_half_x5=sub[q<=0.5].x5.mean(), shallow_half_x5=sub[q>0.5].x5.mean(), n=len(sub)))
    out["by_coin_deep_vs_shallow_half"] = pd.DataFrame(res).round(4)
    return out
