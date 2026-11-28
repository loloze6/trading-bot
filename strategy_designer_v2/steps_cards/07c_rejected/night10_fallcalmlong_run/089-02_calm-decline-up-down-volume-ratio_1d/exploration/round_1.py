def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(float); dn = (r1 < 0).astype(float)
            upv = (v*up).rolling(20).sum()/up.rolling(20).sum()
            dnv = (v*dn).rolling(20).sum()/dn.rolling(20).sum()
            lr = np.log(upv/dnv)
            z = (lr - lr.rolling(60, min_periods=20).mean())/lr.rolling(60, min_periods=20).std()
            ret20 = c/c.shift(20)-1
            volshift = np.log(v.rolling(10).mean()/v.rolling(60).mean())
            n = len(b)
            for h in [2,5,10,20]:
                fwd = c.shift(-h)/c - 1
                idx = np.arange(0, n, h)
                for i in idx:
                    if i+h >= n or pd.isna(fwd.iloc[i]): continue
                    rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     fc=b["regime"].iloc[i]=="unknown", lr=lr.iloc[i], z=z.iloc[i],
                                     ret20=ret20.iloc[i], vs=volshift.iloc[i], fwd=fwd.iloc[i],
                                     day=pd.Timestamp(b["timestamp"].iloc[i]).floor("D")))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin","h"])["fwd"].transform("mean")
    out = {}
    def summ(g):
        g = g.dropna(subset=["lr"])
        rho = stats.spearmanr(g["lr"], g["ex"])[0] if len(g)>10 else np.nan
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan, rho_lr=rho))
    fc = df[df.fc]
    out["fc_by_h_and_sign"] = fc.dropna(subset=["lr"]).assign(pos=lambda x: x.lr>0).groupby(["h","pos"]).apply(summ)
    out["all_profiles_by_h"] = df.groupby(["h","fc"]).apply(summ)
    q = fc[fc.h==5].dropna(subset=["lr"]).copy(); q["qb"] = pd.qcut(q["lr"],5,labels=False)
    out["fc_h5_lr_quintile"] = q.groupby("qb")["ex"].agg(["count","mean"])
    out["fc_h5_by_coin"] = fc[fc.h==5].groupby("coin").apply(summ)
    out["fc_h5_by_year"] = fc[fc.h==5].groupby("year").apply(summ)
    for col in ["ret20","vs","z"]:
        g = fc.dropna(subset=[col])
        out[f"fc_spearman_{col}"] = g.groupby("h").apply(lambda x: pd.Series(dict(n=len(x), rho=stats.spearmanr(x[col],x["ex"])[0])))
    q2 = fc[fc.h==5].dropna(subset=["ret20"]).copy(); q2["qb"]=pd.qcut(q2["ret20"],5,labels=False)
    out["fc_h5_ret20_quintile"] = q2.groupby("qb")[["ret20","ex"]].mean().join(q2.groupby("qb").size().rename("n"))
    q3 = fc[fc.h==10].dropna(subset=["ret20"]).copy(); q3["qb"]=pd.qcut(q3["ret20"],5,labels=False)
    out["fc_h10_ret20_quintile"] = q3.groupby("qb")[["ret20","ex"]].mean().join(q3.groupby("qb").size().rename("n"))
    return out
