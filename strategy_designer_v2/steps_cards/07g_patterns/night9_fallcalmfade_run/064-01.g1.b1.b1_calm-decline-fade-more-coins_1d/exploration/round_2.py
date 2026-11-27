def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            sd30=r.rolling(30).std()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"zr":r/sd,"r":r,
                             "tr60":c/c.shift(60)-1,"sd30":sd30,
                             "regime":b["regime"].values,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year,
                             "clpos":(c-b["low"])/(b["high"]-b["low"])})
            for h in [1,2,3,4,5]:
                df[f"f{h}"]=c.shift(-h)/c-1
            df["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            # agitation proxy within window: sd30 vs its expanding median
            df["agit"]=sd30>sd30.expanding(60).median()
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    for h in [1,2,3,4,5]:
        d=A.groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"]=A[f"f{h}"]-A["coin"].map(d)
    def ts(sub,col,h,off=0):
        s=sub[(sub["pos"]-off)%h==0].dropna(subset=[col])
        n=len(s)
        if n<5: return (n,np.nan,np.nan)
        g=s.groupby("day")[col].sum()
        m=s[col].mean(); se=g.std(ddof=1)*np.sqrt(len(g))/n
        return (n,m,m/se if se>0 else np.nan)
    out={}
    F=A[(A.tr60<-0.1)]
    res=[]
    for lab,s in [("fall z1-2",F[(F.zr>1)&(F.zr<=2)]),("fall z>1",F[F.zr>1]),("fall z>2",F[F.zr>2]),
                  ("fall z1-2 calm",F[(F.zr>1)&(F.zr<=2)&(~F.agit)]),("fall z1-2 agit",F[(F.zr>1)&(F.zr<=2)&(F.agit)]),
                  ("fall z0.3-1",F[(F.zr>0.3)&(F.zr<=1)])]:
        for h in [2,3,4]:
            for off in range(h):
                n,m,t=ts(s,f"u{h}",h,off); res.append([lab,h,off,n,m,t])
    out["fall_rises_offsets"]=pd.DataFrame(res,columns=["grp","h","off","n","mean","t"])
    s=F[(F.zr>1)]
    res=[]
    for y,g in s.groupby("yr"):
        n,m,t=ts(g,"u3",3); res.append([y,n,m,t])
    out["fall_z>1_u3_year"]=pd.DataFrame(res,columns=["yr","n","mean","t"])
    res=[]
    for cn,g in s.groupby("coin"):
        n,m,t=ts(g,"u3",3); res.append([cn,n,m,t])
    out["fall_z>1_u3_coin"]=pd.DataFrame(res,columns=["coin","n","mean","t"])
    # grading: correlation of zr with u3 among fall z>0
    g=F[(F.zr>0)&(F.pos%3==0)].dropna(subset=["u3","zr"])
    out["fall_pos_zr_corr_u3"]=float(np.corrcoef(g.zr,g.u3)[0,1])
    out["fall_pos_n"]=len(g)
    return out
