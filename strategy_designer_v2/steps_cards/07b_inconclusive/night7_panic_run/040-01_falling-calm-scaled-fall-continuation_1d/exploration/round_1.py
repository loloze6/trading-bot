import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    sd = {}
    for coin, ws in bars.items():
        for h in [1,3,5,10]:
            rr = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                rr.extend(list(c[idx+h]/c[idx]-1))
            drift[(coin,h)] = np.mean(rr); sd[(coin,h)] = np.std(rr, ddof=1)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            n = len(c)
            r3p = np.full(n, np.nan); r3p[3:] = c[3:]/c[:-3]-1
            for i in range(0, n, 3):
                if not (f[i] < 0): continue
                d = {"coin": coin, "win": w, "fc": f[i], "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()), "past3": r3p[i]}
                for h in [1,3,5,10]:
                    if i+h < n:
                        d[f"u{h}"] = -((c[i+h]/c[i]-1) - drift[(coin,h)])
                        d[f"s{h}"] = d[f"u{h}"]/sd[(coin,h)]
                    else:
                        d[f"u{h}"] = np.nan; d[f"s{h}"] = np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    def clt(s, days):
        g = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna().groupby("d")["v"].sum()
        G = len(g); se = np.sqrt((g**2).sum()*G/(G-1))/len(s.dropna())
        return s.mean()/se if se > 0 else np.nan
    out = {}
    hz = pd.DataFrame({h: {"mean": X[f"u{h}"].mean(), "t_cl": clt(X[f"u{h}"], X["day"]),
                          "strength": X[f"s{h}"].mean(), "n": X[f"u{h}"].notna().sum()} for h in [1,3,5,10]}).T
    out["by horizon"] = hz
    def grp(key):
        return X.groupby(key).apply(lambda g: pd.Series({"n": len(g), "mean3": g["u3"].mean(),
            "t3": clt(g["u3"], g["day"]), "mean10": g["u10"].mean(), "t10": clt(g["u10"], g["day"])}))
    out["by coin"] = grp("coin")
    out["by window"] = grp("win")
    out["by year"] = grp("year")
    X["fq"] = pd.qcut(X["fc"], 4, labels=["q1 strongest", "q2", "q3", "q4 weakest"])
    out["by forecast quartile"] = grp("fq")
    X["pq"] = pd.qcut(X["past3"], 4, labels=["p1 biggest fall", "p2", "p3", "p4"])
    out["by raw past 3d quartile"] = grp("pq")
    out["share past3<0"] = float((X["past3"] < 0).mean())
    return out
