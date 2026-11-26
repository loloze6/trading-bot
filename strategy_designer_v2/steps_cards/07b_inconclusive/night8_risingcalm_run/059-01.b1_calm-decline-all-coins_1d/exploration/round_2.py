def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            z = s.pct_change(14) / (r1.rolling(30).std() * np.sqrt(14))
            r60 = s.pct_change(60)
            r3 = s.pct_change(3)
            for h in (2, 3, 5):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     ret=c[i+h]/c[i]-1, fc=float(b["forecast"].iloc[i]),
                                     reg=b["regime"].iloc[i], z=z.iloc[i], r60=r60.iloc[i],
                                     r3=r3.iloc[i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin","h"])["ret"].transform("mean")
    df["ex"] = -(df["ret"] - df["drift"])
    def wt(g, wcol=None):
        v = g["ex"].values
        wv = np.abs(g[wcol].values) if wcol else np.ones(len(v))
        m = (v*wv).sum()/wv.sum()
        dev = pd.Series((v-m)*wv).groupby(g["day"].values).sum()
        se = np.sqrt((dev**2).sum())/wv.sum()
        return m, m/se, len(v), dev.shape[0]
    out = {}
    cases = df[(df.reg=="unknown") & (df.fc < 0)].copy()
    res = []
    for h, g in cases.groupby("h"):
        m, t, n, d = wt(g, "fc")
        med = g["fc"].abs().median()
        deep = g[g.fc.abs() > med]["ex"].mean(); sh = g[g.fc.abs() <= med]["ex"].mean()
        res.append(dict(h=h, wmean=m, t=t, n=n, days=d, deep_minus_shallow_ex=deep-sh))
    out["step5_measure_by_h"] = pd.DataFrame(res)
    core = ["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]
    g = cases[(cases.h==5)]
    for name, sub in [("core", g[g.coin.isin(core)]), ("others", g[~g.coin.isin(core)])]:
        m, t, n, d = wt(sub, "fc"); out["h5_"+name] = pd.Series(dict(wmean=m, t=t, n=n, days=d))
    # same day-relative condition in agitated markets: fc not recorded; use bars where z<0 and z below its 60-bar ranks? use z<0
    g5 = cases[cases.h==5].dropna(subset=["r3"]).copy()
    g5["recent3"] = np.where(g5.r3 < 0, "last3_down", "last3_up")
    out["h5_by_last3days"] = g5.groupby("recent3").apply(lambda x: pd.Series(dict(zip(["wmean","t","n","days"], wt(x,"fc")))))
    g5["trend"] = np.where(g5.r60 > 0.10, "rising", np.where(g5.r60 < -0.10, "falling", "choppy"))
    out["h5_step5_by_trend"] = g5.dropna(subset=["r60"]).groupby("trend").apply(lambda x: pd.Series(dict(zip(["wmean","t","n","days"], wt(x,"fc")))))
    return out
