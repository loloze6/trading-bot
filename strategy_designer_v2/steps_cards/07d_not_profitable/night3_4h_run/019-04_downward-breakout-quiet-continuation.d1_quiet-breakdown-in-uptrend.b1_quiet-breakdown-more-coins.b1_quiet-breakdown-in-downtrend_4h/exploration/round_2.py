def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}
    for coin, wins in data["bars"].items():
        r18 = []; r72 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c)-18, 18); r18 += list(c[idx+18]/c[idx]-1)
            idx = np.arange(0, len(c)-72, 72); r72 += list(c[idx+72]/c[idx]-1)
        drift[coin] = (np.mean(r18), np.std(r18), np.mean(r72))
    rows = []; ag = []
    for coin, wins in data["bars"].items():
        d18, s18, d72 = drift[coin]
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            plow = l.shift(1).rolling(12).min(); phigh = h.shift(1).rolling(12).max()
            narrow = ((h-l)/c).rolling(180).mean()/((phigh-plow)/c)
            ret180 = c/c.shift(180)-1; ret7 = c/c.shift(42)-1
            f18 = c.shift(-18)/c-1; f72 = c.shift(-72)/c-1
            fc = b["forecast"].values
            for start in range(0, len(b)-18, 18):
                m = np.where(fc[start:start+18] <= -2)[0]
                if len(m):
                    i = start+m[0]
                    rows.append(dict(fc=fc[i], narrow=narrow.iloc[i], ret180=ret180.iloc[i], ret7=ret7.iloc[i],
                                     s18=-f18.iloc[i], u18=-(f18.iloc[i]-d18), s72=-f72.iloc[i], u72=-(f72.iloc[i]-d72)))
                # every bar of the cell scanned for the first break of either side, any regime
                for side in ("down", "up"):
                    seg = range(start, start+18)
                    hit = [j for j in seg if (c.iloc[j] < plow.iloc[j] if side == "down" else c.iloc[j] > phigh.iloc[j]) and not np.isnan(ret180.iloc[j]) and not np.isnan(narrow.iloc[j])]
                    if hit:
                        j = hit[0]
                        ag.append(dict(side=side, narrow=narrow.iloc[j], ret7=ret7.iloc[j], ret180=ret180.iloc[j],
                                       tot18=f18.iloc[j], unus18=f18.iloc[j]-d18, tot72=f72.iloc[j], s18=s18))
    df = pd.DataFrame(rows)
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    df["nq"] = pd.qcut(df["narrow"], 3, labels=["wide", "mid", "narrow"])
    df["r7q"] = pd.qcut(df["ret7"], 3, labels=["deep7", "mid7", "mild7"])
    out["short_total18_narrow_x_ret7"] = df.groupby(["nq", "r7q"])["s18"].apply(summ).unstack()
    out["short_total72_narrow_x_ret7"] = df.groupby(["nq", "r7q"])["s72"].apply(summ).unstack()
    out["fc_saturated_share_by_nq"] = df.groupby("nq")["fc"].apply(lambda x: (x <= -19.99).mean())
    A = pd.DataFrame(ag)
    A["nq"] = A.groupby("side")["narrow"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["breaks_all_by_narrow_q5_tot18_longdir"] = A.groupby(["side", "nq"])["tot18"].apply(summ).unstack()
    out["breaks_all_by_narrow_q5_unus18_longdir"] = A.groupby(["side", "nq"])["unus18"].apply(summ).unstack()
    A["r7q"] = A.groupby("side")["ret7"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["breaks_all_by_ret7_q5_tot18_longdir"] = A.groupby(["side", "r7q"])["tot18"].apply(summ).unstack()
    out["breaks_all_by_ret7_q5_tot72_longdir"] = A.groupby(["side", "r7q"])["tot72"].apply(summ).unstack()
    out["break_usual_move18"] = A["s18"].median()
    return out
