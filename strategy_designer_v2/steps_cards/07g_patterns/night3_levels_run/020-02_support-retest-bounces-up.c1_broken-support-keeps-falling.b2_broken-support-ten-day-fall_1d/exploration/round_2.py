def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    def grid(H,look):
        rows=[]
        for coin,ws in data["bars"].items():
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                c=b["close"].astype(float)
                f=pd.DataFrame({"coin":coin,"w":w,"fwd":c.shift(-H)/c-1,
                    "past":c/c.shift(look)-1,"fc":b["forecast"].astype(float),
                    "year":pd.to_datetime(b["timestamp"]).dt.year,
                    "vol":c.pct_change().rolling(30).std()})
                rows.append(f.iloc[::H])
        g=pd.concat(rows).dropna(subset=["fwd"])
        g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
        return g
    res=[]
    for H in [5,10,20]:
        for look in [5,10,20,30]:
            g=grid(H,look).dropna(subset=["past"])
            g["z"]=g["past"]/(g["vol"]*np.sqrt(look))
            g=g.dropna(subset=["z"])
            rho=g.groupby("coin").apply(lambda x: stats.spearmanr(x.z,x.ex).correlation)
            q=g.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
            top=g[q==4].ex; bot=g[q==0].ex
            res.append({"H":H,"look":look,"n":len(g),"rho_mean":rho.mean(),"coins_pos":(rho>0).sum(),
                        "top_bot":top.mean()-bot.mean(),"t":stats.ttest_ind(top,bot,equal_var=False).statistic,
                        "top_mean":top.mean()})
    out["momentum_grid"]=pd.DataFrame(res).round(4)
    g=grid(10,10).dropna(subset=["past"])
    g["z"]=g["past"]/(g["vol"]*np.sqrt(10)); g=g.dropna(subset=["z"])
    out["mom10_by_year_rho"]=g.groupby("year").apply(lambda x: pd.Series({"rho":stats.spearmanr(x.z,x.ex).correlation,"n":len(x)})).round(3)
    # zero forecast vs negative, per coin
    g2=grid(10,10)
    def zt(x):
        a=x[x.fc==0].ex; b_=x[x.fc<0].ex
        return pd.Series({"zero":a.mean(),"neg":b_.mean(),"n0":len(a),"nneg":len(b_),"t":stats.ttest_ind(a,b_,equal_var=False).statistic})
    out["zero_vs_neg_by_coin"]=g2.groupby("coin").apply(zt).round(4)
    out["zero_vs_neg_by_year"]=g2.groupby("year").apply(zt).round(4)
    return out
