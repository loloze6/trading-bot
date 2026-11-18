def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float); v=b["volume"].astype(float)
            r1=cl.pct_change()
            lvr=np.log(v/v.shift(1).rolling(30,min_periods=20).mean())
            sd=r1.rolling(60,min_periods=20).std()
            fwd=cl.shift(-5)/cl-1
            n=len(b)
            for i in range(0,n,5):
                if i+5<n:
                    rows.append(dict(coin=c,win=w,r1=r1[i],z=r1[i]/sd[i] if sd[i]>0 else np.nan,lvr=lvr[i],
                        fwd=fwd[i],yr=pd.Timestamp(b["timestamp"][i]).year,wn=int(w[1:])))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d=d.dropna(subset=["z","lvr","ex"])
    out={}
    up=d[d.z>0].copy(); dn=d[d.z<0].copy()
    up["s"]=up.z*up.lvr; dn["s"]=dn.z*dn.lvr
    for nm,df in [("up",up),("dn",dn)]:
        r=stats.spearmanr(df["s"],df["ex"]); 
        out[nm+" spearman z*lvr vs ex"]=f"{r.correlation:.4f} p={r.pvalue:.4f} n={len(df)}"
        r=stats.spearmanr(df["lvr"],df["ex"])
        out[nm+" spearman lvr vs ex"]=f"{r.correlation:.4f} p={r.pvalue:.4f} n={len(df)}"
        X=np.column_stack([np.ones(len(df)),df.z,df.lvr,df.z*df.lvr])
        beta,res,_,_=np.linalg.lstsq(X,df.ex.values,rcond=None)
        e=df.ex.values-X@beta; s2=(e@e)/(len(df)-4)
        se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        out[nm+" OLS ex~z+lvr+z*lvr"]=pd.DataFrame({"b":beta,"t":beta/se},index=["c","z","lvr","zxlvr"]).round(4)
    # graded buckets among up days by lvr within coin
    up["lq"]=up.groupby("coin")["lvr"].transform(lambda s: pd.qcut(s,4,labels=False))
    up["zq"]=up.groupby("coin")["z"].transform(lambda s: pd.qcut(s,2,labels=False))
    def g(df,key):
        o=df.groupby(key)["ex"].agg(["mean","std","count"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"])); return o.round(4)
    out["up: z half x lvr quartile"]=g(up,["zq","lq"])
    hot=up[(up.zq==1)&(up.lq==3)]
    out["up big heavy by year"]=g(hot,"yr")
    out["up big heavy by coin"]=g(hot,"coin")
    out["up big heavy first/second half windows"]=g(hot.assign(h=(hot.wn>12).astype(int)),"h")
    return out
