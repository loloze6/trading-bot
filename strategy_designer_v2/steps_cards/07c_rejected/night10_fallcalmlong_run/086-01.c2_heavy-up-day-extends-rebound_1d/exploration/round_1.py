def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for H in [1,3,5,10,20]:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c)-H, H):
                    rs.append(c[i+H]/c[i]-1)
            drift[(coin,H)] = np.mean(rs) if rs else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            vr = v / v.shift(1).rolling(20).mean()
            r1 = c.pct_change()
            r5p = c.shift(1)/c.shift(6)-1
            fc = b["regime"] != "chop"
            for i in range(len(b)):
                if not fc.iloc[i] or np.isnan(vr.iloc[i]) or np.isnan(r1.iloc[i]): continue
                d = {"coin":coin,"w":w,"i":i,"cell10":i//10,"day":str(b["timestamp"].iloc[i])[:10],
                     "up":r1.iloc[i]>0,"r1":r1.iloc[i],"vr":vr.iloc[i],"r5p":r5p.iloc[i],
                     "year":str(b["timestamp"].iloc[i])[:4]}
                for H in [1,3,5,10,20]:
                    d[f"f{H}"] = c.iloc[i+H]/c.iloc[i]-1 - drift[(coin,H)] if i+H < len(b) else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    out = {}
    out["fc_bars_by_coin"] = df.groupby("coin").size()
    def summ(g):
        r = {}
        for H in [1,3,5,10,20]:
            x = g[f"f{H}"].dropna()
            r[f"m{H}"] = x.mean(); r[f"t{H}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        r["n"] = len(g)
        return pd.Series(r)
    # one per 10-bar cell per group
    df["vrq"] = pd.cut(df["vr"], [0,0.7,1.0,1.5,2.5,100], labels=["<0.7","0.7-1","1-1.5","1.5-2.5",">2.5"])
    df["r5s"] = np.where(df["r5p"]>0,"r5+","r5-")
    up = df[df.up]
    dedup = lambda g: g.drop_duplicates(["coin","w","cell10"])
    out["up_by_vr"] = dedup(up.sort_values("i")).groupby("vrq").apply(summ) if False else up.groupby("vrq").apply(lambda g: summ(dedup(g)))
    out["up_by_vr_r5"] = up.groupby(["r5s","vrq"]).apply(lambda g: summ(dedup(g)))
    dn = df[~df.up]
    out["down_by_vr"] = dn.groupby("vrq").apply(lambda g: summ(dedup(g)))
    out["all_fc_grid"] = summ(dedup(df))
    hv = up[up.vr>=1.5]
    out["heavyup_by_coin"] = hv.groupby("coin").apply(lambda g: summ(dedup(g)))
    out["heavyup_by_year"] = hv.groupby("year").apply(lambda g: summ(dedup(g)))
    out["spearman_vr_f_up"] = pd.Series({f"f{H}": stats.spearmanr(up["vr"], up[f"f{H}"], nan_policy="omit")[0] for H in [1,3,5,10,20]})
    out["spearman_r1_f_heavyup"] = pd.Series({f"f{H}": stats.spearmanr(hv["r1"], hv[f"f{H}"], nan_policy="omit")[0] for H in [1,3,5,10,20]})
    hv2 = hv.copy(); hv2["r1q"] = pd.qcut(hv2["r1"],3,labels=["small","mid","big"])
    out["heavyup_by_r1size"] = hv2.groupby("r1q").apply(lambda g: summ(dedup(g)))
    return out
