import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = 7
    out = {}
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i+H]/c[i]-1)
        mu = np.mean(allr); sd = np.std(allr, ddof=1)
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            reg = df["regime"].astype(str).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for off in range(H):
                for i in range(off, len(c) - H, H):
                    if reg[i] == "unknown" and f[i] > 0:
                        rows.append(dict(off=off, coin=coin, w=w, yr=yr[i], day=day[i], f=f[i],
                                         ex=c[i+H]/c[i]-1-mu, z=(c[i+H]/c[i]-1-mu)/sd))
    d = pd.DataFrame(rows)
    def summ(g):
        m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(g)
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=m, t=m/se if se > 0 else np.nan,
                              strength=g["z"].mean(), share_pos=(g["ex"] > 0).mean()))
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["tercile_by_coin"] = d.groupby(["coin", "fq"]).apply(summ)
    nd = d[d.coin != "DOGEUSD"].copy()
    nd["fq2"] = pd.qcut(nd["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["exclDOGE_by_tercile"] = nd.groupby("fq2").apply(summ)
    out["exclDOGE_by_year"] = nd.groupby("yr").apply(summ)
    out["exclDOGE_by_window"] = nd.groupby("w").apply(summ)
    out["share_cases_by_coin"] = d["coin"].value_counts(normalize=True)
    return out
