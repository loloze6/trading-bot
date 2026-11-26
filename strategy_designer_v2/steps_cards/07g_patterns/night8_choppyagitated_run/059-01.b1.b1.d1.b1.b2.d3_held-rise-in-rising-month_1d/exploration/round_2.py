import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame(dict(coin=coin,win=w,day=pd.to_datetime(b["timestamp"]).dt.floor("D"),
                                 wd=pd.to_datetime(b["timestamp"]).dt.weekday,year=pd.to_datetime(b["timestamp"]).dt.year))
            df["fwd"]=c.shift(-7)/c-1
            df["f1"]=r1.shift(-1)
            df["vr_30_90"]=r1.rolling(30).std()/r1.rolling(90).std()
            df["vr_7_30"]=r1.rolling(7).std()/r1.rolling(30).std()
            df["vr_14_60"]=r1.rolling(14).std()/r1.rolling(60).std()
            df["r30"]=c/c.shift(30)-1
            df["r7"]=c/c.shift(7)-1
            df["inprof"]=(b["regime"]!="chop").astype(int)
            df["grid"]=(np.arange(len(df))%7==0)
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    G=A[A.grid & A.fwd.notna()].copy()
    G["ex"]=G.fwd-G.groupby("coin").fwd.transform("mean")
    A["ex1"]=A.f1-A.groupby("coin").f1.transform("mean")
    def ct(g,col="ex"):
        g=g[g[col].notna()]
        n=len(g)
        if n<5: return pd.Series(dict(n=n,mean=np.nan,t_day=np.nan,days=0))
        m=g[col].mean()
        s=(g[col]-m).groupby(g.day).sum()
        se=np.sqrt((s**2).sum())/n
        return pd.Series(dict(n=n,mean=m,t_day=m/se,days=s.size))
    out={}
    for v in ["vr_30_90","vr_14_60","vr_7_30"]:
        H=G[G[v].notna()].copy(); H["q"]=pd.qcut(H[v],5,labels=False)
        out[v+"_quint"]=H.groupby("q").apply(ct)
        H["low"]=(H.q==0).astype(int)
        out[v+"_lowq_by_window"]=H[H.low==1].groupby("win").apply(ct)
        if v=="vr_14_60":
            out[v+"_lowq_by_coin"]=H[H.low==1].groupby("coin").apply(ct)
            out[v+"_q_by_prof"]=H.groupby(["inprof","q"]).apply(ct)
            out[v+"_lowq_by_r30sign"]=H[H.low==1].groupby(H.r30>0).apply(ct)
            out[v+"_corr_spearman"]=float(H[[v,"ex"]].corr(method="spearman").iloc[0,1])
    out["next_day_by_wd_dayclustered"]=A.groupby("wd").apply(lambda g: ct(g,"ex1"))
    out["sat_ret_by_year"]=A[A.wd==4].groupby("year").apply(lambda g: ct(g,"ex1"))
    out["fri_ret_by_year"]=A[A.wd==3].groupby("year").apply(lambda g: ct(g,"ex1"))
    return out
