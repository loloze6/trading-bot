def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            df["ts"]=pd.to_datetime(b["timestamp"])
            df["ret30"]=c/c.shift(30)-1; df["ret60"]=c/c.shift(60)-1
            df["vol30"]=r1.rolling(30).std()
            df["z1"]=r1/r1.rolling(30).std().shift(1)
            df["r3"]=c/c.shift(3)-1
            df["z3"]=df["r3"]/(df["vol30"].shift(3)*np.sqrt(3))
            for k in (1,3,10): df[f"f{k}"]=c.shift(-k)/c-1
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["wd"]=A.ts.dt.dayofweek; A["yr"]=A.ts.dt.year; A["day"]=A.ts.dt.normalize()
    for k in (1,3,10):
        A[f"d{k}"]=A.groupby("coin")[f"f{k}"].transform(lambda s: s[A.loc[s.index,"pos"]%k==0].mean())
        A[f"x{k}"]=A[f"f{k}"]-A[f"d{k}"]
    A["vmed"]=A.groupby("coin")["vol30"].transform("median")
    A["agit"]=A.vol30>A.vmed
    A["trend"]=np.where(A.ret60>0.10,"rise",np.where(A.ret60<-0.10,"fall",np.where(A.ret60.notna(),"chop",None)))
    out={}
    def dayt(g,col):
        g=g.dropna(subset=[col]); s=g.groupby("day")[col].sum()
        m=g[col].mean(); 
        # day-clustered t of mean
        n=len(g); e=(g[col]-m); se=np.sqrt((e.groupby(g["day"]).sum()**2).sum())/n
        return pd.Series({"n":n,"days":g.day.nunique(),"mean%":100*m,"t_day":m/se if se>0 else np.nan})
    # 1: chop monthly continuation by side of ret30, scaled
    G=A[(A.pos%10==0)].dropna(subset=["ret30","ret60","x10","vol30"]).copy()
    G["s30"]=G.ret30/(G.vol30*np.sqrt(30))
    C=G[G.trend=="chop"]
    r=[]
    for nm,g in [("all",C),("ret30>0",C[C.ret30>0]),("ret30<0",C[C.ret30<0])]:
        res=stats.linregress(g.s30,g.x10); r.append([nm,len(g),res.slope,res.slope/res.stderr])
    out["chop: x10 on scaled ret30, by side"]=pd.DataFrame(r,columns=["grp","n","slope","t"])
    C=C.assign(sx=np.sign(C.ret30)*C.x10)
    out["chop: signed x10 (in month's direction) by window"]=C.groupby("w").apply(lambda g: pd.Series({"n":len(g),"mean%":100*g.sx.mean()})).round(2)
    out["chop: signed x10 by agitation"]=C.groupby("agit").apply(lambda g: dayt(g,"sx")).round(3)
    # 2: next day after scaled up/down days by trend x agitation
    D=A.dropna(subset=["z1","x1","trend"]).copy()
    D["zb"]=pd.cut(D.z1,[-99,-2,-1,1,2,99],labels=["<-2","-2..-1","mid","1..2",">2"])
    out["next-day x1 by z1 bin, trend x agit"]=D.groupby(["trend","agit","zb"]).apply(lambda g: dayt(g,"x1")).round(3)
    # 3: 3-day return after 3-day scaled move, chop agitated, grid 3
    E=A[(A.pos%3==0)].dropna(subset=["z3","x3","trend"]).copy()
    E["zb"]=pd.qcut(E.z3,5,labels=False)
    out["x3 by z3 quintile, chop agitated"]=E[(E.trend=="chop")&E.agit].groupby("zb").apply(lambda g: dayt(g,"x3")).round(3)
    out["x3 by z3 quintile, all"]=E.groupby("zb").apply(lambda g: dayt(g,"x3")).round(3)
    # 4: weekday Wed consistency
    W=A.dropna(subset=["x1"])
    out["Wed x1 by year"]=W[W.wd==2].groupby("yr").apply(lambda g: dayt(g,"x1")).round(3)
    out["x1 by weekday, day-clustered"]=W.groupby("wd").apply(lambda g: dayt(g,"x1")).round(3)
    return out
