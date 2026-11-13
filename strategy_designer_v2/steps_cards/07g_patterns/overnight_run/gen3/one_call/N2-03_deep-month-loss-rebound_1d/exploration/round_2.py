def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    daily = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            s = pd.Series(c)
            r1 = s.pct_change()
            vol20 = r1.rolling(20).std()
            ch20 = s.pct_change(20)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(1, n - 1):
                daily.append(dict(coin=coin, w=w, wd=ts.iloc[i].weekday(), year=ts.iloc[i].year,
                                  r=r1.iloc[i], nxt=c[i+1]/c[i]-1, vol=vol20.iloc[i], ch20=ch20.iloc[i],
                                  f=b["forecast"].iloc[i]))
    D = pd.DataFrame(daily).dropna(subset=["r", "vol", "nxt"])
    D["z"] = D["r"] / D["vol"]
    D["down"] = D["z"] <= -1
    D["nxt_ex"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    def ag(g):
        return pd.Series({"n": len(g), "mean_ex": g["nxt_ex"].mean(), "t": stats.ttest_1samp(g["nxt_ex"], 0).statistic, "hit": (g["nxt"] > 0).mean()})
    dn = D[D.down]
    out["z<=-1 next-day excess by coin"] = dn.groupby("coin").apply(ag)
    out["z<=-1 next-day excess by year"] = dn.groupby("year").apply(ag)
    D["vq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["z<=-1 by vol tercile"] = dn.assign(vq=D.loc[dn.index, "vq"]).groupby("vq").apply(ag)
    D["c20"] = np.where(D["ch20"].isna(), np.nan, np.where(D["ch20"] < 0, 0, 1))
    out["z<=-1 by 20d trend sign (0=down)"] = D[D.down].groupby("c20").apply(ag)
    out["z>=1 next-day excess by 20d sign"] = D[D["z"] >= 1].groupby("c20").apply(ag)
    out["z<=-1 by weekday"] = dn.groupby("wd").apply(ag)
    out["z>-1 (not down) next-day excess"] = ag(D[~D.down]).to_frame().T
    # two consecutive down days
    D["prev_down"] = D.groupby(["coin", "w"])["down"].shift(1)
    out["down today & prev_down"] = D[D.down].groupby("prev_down").apply(ag)
    # weekday by year for Thu/Fri
    D["thfr"] = D["wd"].isin([3, 4])
    out["Thu+Fri next-day excess by year"] = D[D.thfr].groupby("year").apply(ag)
    # book: book return conditional on whether forecast>0, split by days in position
    Bk = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    out["book vs coin daily corr"] = Bk[["book_return", "coin_return"]].corr().iloc[0, 1]
    return out
