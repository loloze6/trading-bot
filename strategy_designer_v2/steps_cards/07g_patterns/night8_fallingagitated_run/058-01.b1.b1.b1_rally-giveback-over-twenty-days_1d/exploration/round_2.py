def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allsd = []
        for w, b in ws.items():
            c = pd.Series(b["close"].values)
            allsd.append(c.pct_change().rolling(30, min_periods=20).std())
        medsd = pd.concat(allsd).median()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            cs = pd.Series(c)
            r1 = cs.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            sc = cs.pct_change(3) / sd30
            r60 = cs.pct_change(60)
            inprof = (b["regime"] == "unknown").values
            n = len(b)
            for h in [3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(pd.Timestamp(b["timestamp"].iloc[i]).date()),
                                     yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     fwd=c[i + h] / c[i] - 1, sc=sc.iloc[i], prof=inprof[i],
                                     r60=r60.iloc[i], agit=(sd30.iloc[i] > medsd) if pd.notna(sd30.iloc[i]) else np.nan,
                                     sd=sd30.iloc[i]))
    df = pd.DataFrame(rows)
    df = df.join(df.groupby(["coin", "h"])["fwd"].mean().rename("drift"), on=["coin", "h"])
    df["ex"] = df["fwd"] - df["drift"]
    df["exz"] = df["ex"] / (df["sd"] * np.sqrt(df["h"]))
    df = df.dropna(subset=["sc"])
    df["trend"] = np.where(df.r60.isna(), "na", np.where(df.r60 > 0.10, "rising", np.where(df.r60 < -0.10, "falling", "choppy")))
    def ct(g, col="ex"):
        s = g.groupby("day")[col].sum()
        m = g[col].mean(); nd = len(s)
        se = np.sqrt((s - s.size and 0).pow(2).sum()) if False else None
        dev = g[col] - m
        sdev = dev.groupby(g["day"]).sum()
        se = np.sqrt((sdev ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=nd, mean_ex=m, t_day=m / se if se > 0 else np.nan, strength=g["exz"].mean()))
    out = {}
    big = df[df.sc > 2]
    out["bigrise_by_prof_h"] = big.groupby(["prof", "h"]).apply(ct)
    out["bigrise_out_by_trend_h5_10"] = big[(~big.prof) & big.h.isin([5, 10])].groupby(["h", "trend"]).apply(ct)
    out["bigrise_out_by_agit_h5_10"] = big[(~big.prof) & big.h.isin([5, 10])].groupby(["h", "agit"]).apply(ct)
    out["bigrise_out_by_year_h5"] = big[(~big.prof) & (big.h == 5)].groupby("yr").apply(ct)
    # graded slope out of profile on positive scaled rise
    res = {}
    for h in [3, 5, 10, 20]:
        g = df[(~df.prof) & (df.h == h) & (df.sc > 0)]
        x = g["sc"].values; y = g["ex"].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        # cluster by day
        XtX = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for d, idx in g.reset_index().groupby("day").groups.items():
            u = (X[idx].T @ e[idx]).reshape(-1, 1); meat += u @ u.T
        V = XtX @ meat @ XtX
        res[h] = dict(n=len(g), slope=beta[1], t=beta[1] / np.sqrt(V[1, 1]))
    out["out_slope_ex_on_posrise"] = pd.DataFrame(res).T
    # in-profile shorter horizons after rises
    out["inprof_rise_h3"] = df[(df.prof) & (df.h == 3)].assign(q=lambda x: pd.cut(x.sc, [-99, -1, 0, 1, 2, 99])).groupby("q").apply(ct)
    # w16 book: what drove losses
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; tr.append(t)
    T = pd.concat(tr)
    out["w16_trades_by_coin"] = T[T.w == "w16"].groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), worst=("net_profit_loss_percent", "min"))
    return out
