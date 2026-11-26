def explore(data):
    import pandas as pd, numpy as np
    bars=data["bars"]; days=data["days"]
    out={}
    cs=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True).copy()
            ts=pd.to_datetime(df["timestamp"])
            cl=df["close"]
            df["ret_next"]=cl.shift(-1)/cl-1
            df["ret2"]=cl.shift(-2)/cl-1
            df["g20"]=cl/cl.shift(20)-1
            df["r5"]=cl/cl.shift(5)-1
            df["r10"]=cl/cl.shift(10)-1
            df["hi20"]=cl/cl.rolling(20).max()-1
            df["wd"]=ts.dt.weekday
            df["alloc"]=df["postRebalance_current_allocation"]
            df["coin"]=c; df["w"]=w; df["wn"]=int(w[1:]); df["day"]=ts.dt.normalize()
            df["fc"]=df["forecast"]
            cs.append(df[["coin","w","wn","day","wd","ret_next","ret2","g20","r5","r10","hi20","alloc","fc"]])
    A=pd.concat(cs)
    mu=A.groupby("coin")["ret_next"].mean()
    A["ex"]=A["ret_next"]-A["coin"].map(mu)
    A["ex2"]=A["ret2"]-2*A["coin"].map(mu)
    def s(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    F=A[A.wd==4]
    sig=F[F.fc>0]
    # condition alone checks
    out["r5_cond_check"]=pd.DataFrame({
        "sig&r5>0":s(sig[sig.r5>0].ex),"sig&r5<=0":s(sig[sig.r5<=0].ex),
        "fri g20<=0 & r5>0":s(F[(F.g20<=0)&(F.r5>0)].ex),"fri g20<=0 & r5<=0":s(F[(F.g20<=0)&(F.r5<=0)].ex),
        "nonfri g20>0 & r5>0":s(A[(A.wd!=4)&(A.g20>0)&(A.r5>0)].ex),"nonfri g20>0 & r5<=0":s(A[(A.wd!=4)&(A.g20>0)&(A.r5<=0)].ex),
        "nonfri all":s(A[A.wd!=4].ex)}).round(4)
    out["hi20_cond_check"]=pd.DataFrame({
        "sig&hi20=0":s(sig[sig.hi20>=0].ex),"sig&hi20<0":s(sig[sig.hi20<0].ex),
        "fri g20<=0 hi20>-0.03":s(F[(F.g20<=0)&(F.hi20>-0.03)].ex),
        "nonfri g20>0 hi20=0":s(A[(A.wd!=4)&(A.g20>0)&(A.hi20>=0)].ex)}).round(4)
    out["sig_2day"]=pd.DataFrame({"sig 1d":s(sig.ex),"sig 2d (sat+sun)":s(sig.ex2)}).round(4)
    # book simulation: zero book return on Saturday days after a signal with r5<=0
    D=[]
    for c in days:
        for w,df in days[c].items():
            d=df[["day","book_return"]].copy(); d["coin"]=c; d["wn"]=int(w[1:]); d["day"]=pd.to_datetime(d["day"]).dt.normalize(); D.append(d)
    D=pd.concat(D)
    S=sig[["coin","wn","day","r5","hi20","fc"]].copy(); S["day"]=S["day"]+pd.Timedelta(days=1)
    D=D.merge(S,on=["coin","wn","day"],how="left")
    def book(br):
        X=D.assign(br=br).groupby(["wn","day"]).br.mean().dropna().reset_index().sort_values(["wn","day"])
        r=X.br; v=(1+r).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(r))-1
        sh=r.mean()/r.std()*np.sqrt(365)
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":sh})
    base=D.book_return
    keep_r5=np.where(D.r5.notna()&(D.r5<=0),0.0,base)
    keep_hi=np.where(D.hi20.notna()&(D.hi20<-0.03),0.0,base)
    out["book_sim"]=pd.DataFrame({"base":book(base),"only r5>0":book(pd.Series(keep_r5,index=D.index)),"only hi20>=-3%":book(pd.Series(keep_hi,index=D.index))}).round(4)
    # what the book held during its deepest fall windows 16-17
    W=sig[sig.wn.isin([16,17])].copy()
    W["gain"]=W.alloc*W.ret_next
    out["w16_17_by_r5sign"]=W.groupby(np.sign(W.r5)).agg(n=("gain","size"),gain=("gain","sum"),worst=("gain","min"),alloc=("alloc","mean")).round(4)
    out["worst20_sig_gains_r5"]=W.nsmallest(20,"gain")[["r5","hi20","g20","alloc","gain"]].describe().round(4)
    return out
