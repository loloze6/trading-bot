def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for H in [3,5,10]:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c)-H, H):
                    rs.append(c[i+H]/c[i]-1)
            drift[(coin,H)] = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            vr = v / v.shift(1).rolling(20).mean()
            r1 = c.pct_change()
            r5 = c/c.shift(5)-1
            r5p = c.shift(1)/c.shift(6)-1
            sd = r1.rolling(20).std()
            fc = b["regime"] != "chop"
            for i in range(len(b)):
                if not fc.iloc[i] or np.isnan(vr.iloc[i]) or np.isnan(r5p.iloc[i]): continue
                d = {"coin":coin,"w":w,"i":i,"day":str(b["timestamp"].iloc[i])[:10],
                     "r1":r1.iloc[i],"vr":vr.iloc[i],"r5":r5.iloc[i],"r5p":r5p.iloc[i],"r5z":r5.iloc[i]/(sd.iloc[i]*np.sqrt(5)),
                     "year":str(b["timestamp"].iloc[i])[:4]}
                for H in [3,5,10]:
                    d[f"f{H}"] = c.iloc[i+H]/c.iloc[i]-1 - drift[(coin,H)] if i+H < len(b) else np.nan
                    d[f"cell{H}"] = i//H
                rows.append(d)
    df = pd.DataFrame(rows)
    out = {}
    def ct(g, H):
        g = g.drop_duplicates(["coin","w",f"cell{H}"]).dropna(subset=[f"f{H}"])
        x = g[f"f{H}"]; m = x.mean()
        dev = (x-m).groupby(g["day"]).sum()
        D = len(dev); se = np.sqrt((dev**2).sum())/len(x)*np.sqrt(D/(D-1)) if D>1 else np.nan
        return pd.Series({"m":m,"t_day":m/se,"n":len(x),"days":D})
    out["all_fc_5"] = ct(df,5); out["all_fc_10"] = ct(df,10)
    up = df[df.r1>0]
    for H in [5,10]:
        a = up[up.r5p>0]
        out[f"up_r5pos_H{H}"] = ct(a,H)
        out[f"up_r5pos_lightvr<1_H{H}"] = ct(a[a.vr<1],H)
        out[f"up_r5pos_heavy>=1_H{H}"] = ct(a[a.vr>=1],H)
    # graded by r5 (rebound strength incl. day) on all fc days
    df["r5q"] = pd.qcut(df["r5z"],5,labels=False)
    out["by_r5z_quint_H5"] = df.groupby("r5q").apply(lambda g: ct(g,5))
    out["by_r5z_quint_H10"] = df.groupby("r5q").apply(lambda g: ct(g,10))
    out["spearman_r5z_f"] = pd.Series({f"f{H}": stats.spearmanr(df["r5z"],df[f"f{H}"],nan_policy="omit")[0] for H in [3,5,10]})
    pos = df[df.r5z>0]
    out["pos_r5_by_coin_H5"] = pos.groupby("coin").apply(lambda g: ct(g,5))
    out["pos_r5_by_year_H5"] = pos.groupby("year").apply(lambda g: ct(g,5))
    out["pos_r5_light_vs_heavy_H5"] = pos.assign(l=np.where(pos.vr<1,"light","heavy")).groupby("l").apply(lambda g: ct(g,5))
    out["spearman_vr_f5_r5pos_up"] = stats.spearmanr(up[up.r5p>0]["vr"], up[up.r5p>0]["f5"], nan_policy="omit")[0]
    return out
