import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (1,2,3,5)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            ts = pd.to_datetime(df["timestamp"]).dt.floor("D").astype("int64").values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            rng = (hi-lo)/c
            low_lvl = None; used = set()
            for t in range(len(df)):
                if f[t] <= 0:
                    low_lvl = None; continue
                if low_lvl is None: low_lvl = 0.0
                if f[t]-low_lvl >= 2:
                    cell = t//5
                    if cell not in used:
                        used.add(cell)
                        r = {"coin": coin, "win": w, "year": year[t], "fc": f[t], "dayk": ts[t]}
                        for h in (1,2,3,5):
                            if t+h < len(c):
                                r[f"u{h}"] = c[t+h]/c[t]-1-drift[coin][h]
                        r["ret30"] = c[t]/c[t-30]-1 if t>=30 else np.nan
                        r["ret1"] = c[t]/c[t-1]-1 if t>=1 else np.nan
                        r["rng1"] = rng[t]
                        r["rng30"] = rng[max(0,t-29):t+1].mean()
                        rows.append(r)
                    low_lvl = f[t]
                else:
                    low_lvl = min(low_lvl, f[t])
    d = pd.DataFrame(rows)
    d["drop_in_rng"] = -d["ret1"]/d["rng30"]   # last-day fall in units of 30-day mean range
    d["ret30_in_rng"] = -d["ret30"]/d["rng30"]
    def pooled(g, col):
        x = g[[col,"dayk"]].dropna()
        if len(x) < 5: return (x[col].mean() if len(x) else np.nan, np.nan, len(x))
        m = x[col].mean()
        s = (x[col]-m).groupby(x["dayk"]).sum()
        G = len(s)
        se = np.sqrt((s**2).sum()*G/(G-1))/len(x)
        return (m, m/se, G)
    def summ(g):
        out = {}
        for h in (1,2,3,5):
            m,t,G = pooled(g, f"u{h}")
            out[f"m{h}"]=m; out[f"tp{h}"]=t
        out["days"] = g["dayk"].nunique(); out["n"]=len(g)
        return pd.Series(out)
    res = {}
    res["all_pooled"] = summ(d).to_frame().T
    res["corr"] = d[["fc","ret30","ret1","drop_in_rng","ret30_in_rng","rng30","u1","u3","u5"]].corr().round(3)
    for col in ["drop_in_rng","ret30_in_rng","rng30","fc"]:
        d["q"] = pd.qcut(d[col].rank(method="first"), 3, labels=["q1","q2","q3"])
        res[f"by_{col}"] = d.groupby("q").apply(summ)
    d["dq"] = pd.qcut(d["drop_in_rng"].rank(method="first"), 3, labels=["q1","q2","q3"])
    top = d[d["dq"]=="q3"]
    res["topdrop_by_year"] = top.groupby("year").apply(summ)
    res["topdrop_by_coin"] = top.groupby("coin").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 2, labels=["fcLo","fcHi"])
    d["rq"] = pd.qcut((-d["ret30"]).rank(method="first"), 2, labels=["shallow","deep"])
    res["fc_x_ret30"] = d.groupby(["fq","rq"]).apply(summ)
    res["fc_by_year_top"] = d[d["fq"]=="fcHi"].groupby("year").apply(summ)
    return res
