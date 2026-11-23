def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); r=cl.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":c,"win":w,"wd":ts.dt.weekday,"year":ts.dt.year,"r1":r,
                "vol20":r.rolling(20).std(),"vol60":r.rolling(60).std(),
                "vrel":b["volume"]/b["volume"].rolling(20).mean(),
                "f1":cl.shift(-1)/cl-1,"f2b":cl.shift(-2)/cl.shift(-1)-1,
                "f2":cl.shift(-2)/cl-1,"f3":cl.shift(-3)/cl-1,"f5":cl.shift(-5)/cl-1})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["r1","vol20","vol60","f1"])
    D["z"]=D["r1"]/D["vol20"]
    for h in ["f1","f2","f3","f5"]:
        D["u_"+h]=D[h]-D.groupby("coin")[h].transform("mean")
    def reg(g,y,x="z",norm=True):
        g=g.dropna(subset=[x,y])
        if len(g)<30: return pd.Series({"n":len(g)})
        yy=g[y]/g["vol20"] if norm else g[y]
        s=stats.linregress(g[x],yy)
        return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out={}
    Sa=D[D.wd==5].copy()
    out["sat_f1_by_year"]=Sa.groupby("year").apply(lambda g:reg(g,"u_f1"))
    out["sat_f1_by_coin"]=Sa.groupby("coin").apply(lambda g:reg(g,"u_f1"))
    out["sat_f1_raw_return_on_raw_r1"]=reg(Sa,"u_f1","r1",False).to_frame().T
    out["sat_f1_by_vrel_q"]=Sa.groupby(pd.qcut(Sa["vrel"],4,labels=False)).apply(lambda g:reg(g,"u_f1"))
    out["sat_horizons"]=pd.DataFrame({h:reg(Sa,"u_"+h) for h in ["f1","f2","f3","f5"]}).T
    out["sat_f1_by_absz_q"]=Sa.groupby(pd.qcut(Sa["z"].abs(),4,labels=False)).apply(lambda g:pd.Series({"n":len(g),"mean_against":(-np.sign(g["z"])*g["u_f1"]).mean(),"t":stats.ttest_1samp(-np.sign(g["z"])*g["u_f1"],0).statistic}))
    We=D[D.wd==2].copy()
    out["wed_f5_by_year"]=We.groupby("year").apply(lambda g:reg(g,"u_f5"))
    out["wed_f5_by_coin"]=We.groupby("coin").apply(lambda g:reg(g,"u_f5"))
    out["wed_horizons"]=pd.DataFrame({h:reg(We,"u_"+h) for h in ["f1","f2","f3","f5"]}).T
    out["wed_f5_raw"]=reg(We,"u_f5","r1",False).to_frame().T
    out["wed_by_absz_q"]=We.groupby(pd.qcut(We["z"].abs(),4,labels=False)).apply(lambda g:pd.Series({"n":len(g),"mean_with":(np.sign(g["z"])*g["u_f5"]).mean(),"t":stats.ttest_1samp(np.sign(g["z"])*g["u_f5"],0).statistic}))
    # placebo: thursday-tuesday f5 slope already ~; also Friday f1
    return out
