def explore(data):
    import pandas as pd, numpy as np
    bars=data["bars"]; days=data["days"]
    out={}
    # book daily
    rows=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=c; rows.append(dd)
    D=pd.concat(rows)
    D["wn"]=D["w"].str[1:].astype(int)
    B=D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B=B.dropna()
    v=(1+B.book_return).cumprod(); dd=v/v.cummax()-1
    B["dd"]=dd.values
    per=B.groupby("wn").agg(book=("book_return",lambda x:(1+x).prod()-1),hold=("coin_return",lambda x:(1+x).prod()-1),
        bookstd=("book_return","std"),n=("book_return","size"))
    # within-window maxdd
    def mdd(x):
        vv=(1+x).cumprod(); return (vv/vv.cummax()-1).min()
    per["book_mdd"]=B.groupby("wn")["book_return"].apply(mdd)
    per["hold_mdd"]=B.groupby("wn")["coin_return"].apply(mdd)
    out["per_window"]=per.round(4)
    out["chain_mdd"]=float(dd.min())
    # worst book days: coin return on those days
    B["worst"]=B.book_return.rank()<=40
    out["worst40_days"]=B[B.worst][["book_return","coin_return"]].describe().round(4)
    out["corr_book_coin"]=float(B.book_return.corr(B.coin_return))
    # cases
    cs=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change(); vol=b.volume
            vr=vol/vol.shift(1).rolling(20).mean()
            f2=cl.shift(-2)/cl-1; f1=cl.shift(-1)/cl-1; f5=cl.shift(-5)/cl-1
            p20=cl/cl.shift(20)-1; p10=cl/cl.shift(10)-1
            sd=r1.rolling(20).std()
            df=pd.DataFrame({"r1":r1,"vr":vr,"f2":f2,"f1":f1,"f5":f5,"p20":p20,"p10":p10,"sd":sd,"fc":b.forecast,"alloc":b.postRebalance_current_allocation})
            df=df.iloc[::2]; df["coin"]=c; df["wn"]=int(w[1:]); cs.append(df)
    C=pd.concat(cs).dropna(subset=["f2","r1"])
    C["dn"]=C.r1<0
    C["ex2"]=C.f2-C.groupby("coin").f2.transform("mean")
    C["z"]=C.r1/C.sd
    C["tr"]=pd.cut(C.p20,[-9,-0.15,-0.03,0.03,0.15,9],labels=["<-15","-15..-3","-3..3","3..15",">15"])
    C["vt"]=C.groupby("coin").vr.transform(lambda x:pd.qcut(x,3,labels=False,duplicates="drop"))
    g=C.groupby(["tr","dn"]).agg(n=("f2","size"),f2=("f2","mean"),ex2=("ex2","mean"))
    out["trend20_by_downday"]=g.round(4)
    dn=C[C.dn]
    out["down_trend_x_volterc"]=dn.groupby(["tr","vt"]).f2.mean().unstack().round(4)
    dn=dn.copy(); dn["zb"]=pd.cut(dn.z,[-99,-2,-1,-0.5,0],labels=["<-2","-2..-1","-1..-.5",">-.5"])
    out["down_z_x_volterc"]=dn.groupby(["zb","vt"]).f2.agg(["mean","size"]).unstack().round(4)
    out["nondown_volterc"]=C[~C.dn].groupby("vt").f2.agg(["mean","size"]).round(4)
    out["down_horizons_by_vt"]=dn.groupby("vt")[["f1","f2","f5"]].mean().round(4)
    return out
