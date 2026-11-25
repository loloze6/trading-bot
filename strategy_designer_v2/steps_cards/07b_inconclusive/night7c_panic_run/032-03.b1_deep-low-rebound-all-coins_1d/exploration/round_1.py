import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (1,3,5,10,20)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: (np.mean(v), np.std(v)) for h, v in allr.items()}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
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
                        r = {"coin": coin, "win": w, "year": year[t], "t": t, "fc": f[t],
                             "day": t}
                        for h in (1,3,5,10,20):
                            if t+h < len(c):
                                r[f"u{h}"] = c[t+h]/c[t]-1-drift[coin][h][0]
                        r["ret30"] = c[t]/c[t-30]-1 if t>=30 else np.nan
                        r["rng10"] = rng[max(0,t-9):t+1].mean()
                        r["rng_prev"] = rng[max(0,t-29):max(1,t-9)].mean()
                        r["ret1"] = c[t]/c[t-1]-1 if t>=1 else np.nan
                        rows.append(r)
                    low_lvl = f[t]
                else:
                    low_lvl = min(low_lvl, f[t])
    d = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in (1,3,5,10,20):
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    res = {}
    res["all"] = summ(d).to_frame().T
    res["by_coin"] = d.groupby("coin").apply(summ)
    res["by_year"] = d.groupby("year").apply(summ)
    res["by_win"] = d.groupby("win").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["lo","mid","hi"])
    res["by_fc"] = d.groupby("fq").apply(summ)
    d["r30q"] = pd.qcut(d["ret30"].rank(method="first"), 3, labels=["shallow","mid","deep"])
    res["by_ret30"] = d.groupby("r30q").apply(summ)
    d["rngexp"] = pd.qcut((d["rng10"]/d["rng_prev"]).rank(method="first"), 3, labels=["contract","mid","expand"])
    res["by_range_expansion"] = d.groupby("rngexp").apply(summ)
    d["r1q"] = pd.qcut(d["ret1"].rank(method="first"), 3, labels=["bigdrop","mid","small"])
    res["by_lastday"] = d.groupby("r1q").apply(summ)
    res["corr_fc_u5"] = float(d[["fc","u5"]].corr().iloc[0,1])
    res["corr_ret30_u5"] = float(d[["ret30","u5"]].corr().iloc[0,1])
    return res
