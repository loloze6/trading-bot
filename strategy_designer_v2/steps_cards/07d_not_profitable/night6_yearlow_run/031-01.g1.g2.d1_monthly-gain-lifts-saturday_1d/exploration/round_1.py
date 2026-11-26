def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    # book daily returns: mean over coins per (window, day)
    rows=[]
    for c in days:
        for w,df in days[c].items():
            d=df[["day","book_return","coin_return"]].copy(); d["coin"]=c; d["w"]=w; rows.append(d)
    D=pd.concat(rows)
    D["wn"]=D["w"].str[1:].astype(int)
    B=D.groupby(["wn","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B=B.dropna(subset=["br"])
    v=(1+B["br"]).cumprod(); peak=v.cummax(); dd=v/peak-1
    B["dd"]=dd.values; B["v"]=v.values
    out["maxdd"]=float(dd.min())
    # deepest-fall episode: from peak to trough
    ti=dd.idxmin(); B=B.reset_index(drop=True); dd=B["dd"]; ti=dd.idxmin()
    pi=B.loc[:ti,"v"].idxmax()
    out["dd_episode"]=pd.Series({"peak_w":B.loc[pi,"wn"],"trough_w":B.loc[ti,"wn"],"days":ti-pi,"peak_year":pd.Timestamp(B.loc[pi,"day"]).year,"trough_year":pd.Timestamp(B.loc[ti,"day"]).year})
    B["year"]=pd.to_datetime(B["day"]).dt.year
    out["by_window"]=B.groupby("wn").agg(sum_br=("br","sum"),mdd=("dd","min"),coin=("cr","sum")).round(4)
    # cases
    cs=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True).copy()
            ts=pd.to_datetime(df["timestamp"])
            cl=df["close"]
            df["ret_next"]=cl.shift(-1)/cl-1
            df["g20"]=cl/cl.shift(20)-1
            df["r1"]=cl/cl.shift(1)-1
            df["r5"]=cl/cl.shift(5)-1
            df["g60"]=cl/cl.shift(60)-1
            lr=np.log(cl).diff()
            df["vol20"]=lr.rolling(20).std()
            df["vol60"]=lr.rolling(60).std()
            df["hi20"]=cl/cl.rolling(20).max()-1
            df["wd"]=ts.dt.weekday
            df["alloc"]=df["postRebalance_current_allocation"]
            df["coin"]=c; df["w"]=w; df["year"]=ts.dt.year
            df["fc"]=df["forecast"]
            cs.append(df[["coin","w","year","wd","ret_next","g20","r1","r5","g60","vol20","vol60","hi20","alloc","fc","timestamp"]])
    A=pd.concat(cs)
    mu=A.groupby("coin")["ret_next"].mean()
    A["ex"]=A["ret_next"]-A["coin"].map(mu)
    A["gain"]=A["alloc"]*A["ret_next"]
    F=A[A.wd==4].dropna(subset=["ret_next","g20"])
    sig=F[F.fc>0]
    nos=F[F.g20<=0]
    def s(x): 
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["fri_sig_vs_not"]=pd.DataFrame({"sig":s(sig.ex),"g20<=0":s(nos.ex),"g20>0 fc=0":s(F[(F.g20>0)&(F.fc<=0)].ex)}).round(4)
    out["sig_by_year_gain"]=sig.groupby("year").agg(n=("ex","size"),ex=("ex","mean"),gain=("gain","sum"),alloc=("alloc","mean")).round(4)
    sig=sig.copy()
    for col in ["g20","r1","r5","g60","vol20","hi20","fc","alloc"]:
        q=pd.qcut(sig[col].rank(method="first"),4,labels=False)
        out["sig_q_"+col]=sig.groupby(q).agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),ex=("ex","mean"),sd=("ex","std"),gain=("gain","sum"),worst=("gain","min")).round(4)
    # same conditions on non-signal Fridays and all non-Friday days for r1 / g60
    Fn=F[F.g20<=0].copy()
    for col in ["r1","g60"]:
        out["nosig_fri_sign_"+col]=Fn.groupby(np.sign(Fn[col])).ex.agg(["size","mean"]).round(4)
        out["sig_sign_"+col]=sig.groupby(np.sign(sig[col])).agg(n=("ex","size"),ex=("ex","mean"),gain=("gain","sum"),worst=("gain","min")).round(4)
    # worst book days
    wd_=B.nsmallest(15,"br")
    out["worst_days_share_of_loss"]=float(wd_.br.sum())
    return out
