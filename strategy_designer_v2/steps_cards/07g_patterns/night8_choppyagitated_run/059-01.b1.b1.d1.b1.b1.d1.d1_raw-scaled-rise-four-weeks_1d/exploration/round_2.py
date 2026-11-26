def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30, min_periods=20).mean()
            mult = r7 / mabs
            vol30 = r1.rolling(30, min_periods=20).std()
            tr60 = c / c.shift(60) - 1
            n = len(b)
            for h in [3, 7]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if np.isnan(fwd.iloc[i]):
                        continue
                    ts = pd.Timestamp(b["timestamp"].iloc[i])
                    rows.append(dict(coin=coin, w=w, h=h, day=ts.normalize(),
                                     yr=ts.year, inprof=b["regime"].iloc[i] == "unknown",
                                     mult=mult.iloc[i], sc1=r1.iloc[i] / vol30.iloc[i],
                                     tr60=tr60.iloc[i], fwd=fwd.iloc[i]))
    df = pd.DataFrame(rows)
    df["fwd_d"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["fwd_z"] = df["fwd_d"] / df.groupby(["coin", "h"])["fwd"].transform("std")

    def clustered(sub, x):
        s = sub[[x, "fwd_z", "day"]].dropna()
        if len(s) < 30:
            return dict(n=len(s), days=np.nan, slope=np.nan, t_cl=np.nan)
        X = s[x] - s[x].mean(); y = s["fwd_z"] - s["fwd_z"].mean()
        b = (X * y).sum() / (X * X).sum()
        e = y - b * X
        sc = (X * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X * X).sum()
        return dict(n=len(s), days=s["day"].nunique(), slope=b, t_cl=b / se)

    tab = []
    for h in [3, 7]:
        for lab, m in [("out_all", ~df.inprof), ("in_prof", df.inprof),
                       ("out_tr_up", (~df.inprof) & (df.tr60 > 0.10)),
                       ("out_tr_chop", (~df.inprof) & (df.tr60.abs() <= 0.10)),
                       ("out_tr_down", (~df.inprof) & (df.tr60 < -0.10)),
                       ("all", df.h > 0)]:
            for x in ["mult", "sc1"]:
                d = clustered(df[(df.h == h) & m], x); d.update(h=h, grp=lab, x=x); tab.append(d)
    out["clustered_slopes"] = pd.DataFrame(tab)

    tab = []
    for h in [3, 7]:
        for y in sorted(df.yr.unique()):
            d = clustered(df[(df.h == h) & (df.yr == y)], "mult"); d.update(h=h, yr=y); tab.append(d)
    out["mult_by_year"] = pd.DataFrame(tab)

    # weekday, day-clustered (mean over coins per day)
    D = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()])
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday
    D["cr_d"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    P = D.groupby("day").agg(cr=("cr_d", "mean")).reset_index()
    P["wd"] = P["day"].dt.weekday; P["yr"] = P["day"].dt.year
    g = P.groupby("wd")["cr"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_day_clustered"] = g.drop(columns="std")
    P["frisat"] = P.wd.isin([4, 5])
    g = P.groupby(["yr", "frisat"])["cr"].mean().unstack()
    out["frisat_by_year"] = g
    g = D[D.wd.isin([4, 5])].groupby("coin")["cr_d"].agg(["count", "mean"])
    out["frisat_by_coin"] = g
    # book by in-profile side
    B = pd.concat([b.assign(coin=c) for c, ws in data["bars"].items() for b in ws.values()])
    B["nxt"] = B.groupby(["coin"])["close"].shift(-1) / B["close"] - 1
    B["pos"] = B["postRebalance_current_allocation"]
    B["side"] = np.sign(B["pos"])
    g = B.dropna(subset=["nxt"]).assign(g=lambda x: x.pos * x.nxt).groupby("side")["g"].agg(["count", "mean", "sum"])
    out["bar_gain_by_side"] = g
    return out
