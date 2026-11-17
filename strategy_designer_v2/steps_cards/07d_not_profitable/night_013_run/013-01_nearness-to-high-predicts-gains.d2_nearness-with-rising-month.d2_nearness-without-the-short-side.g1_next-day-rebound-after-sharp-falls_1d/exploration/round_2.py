def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float)
            allr.append((c.shift(-1)/c-1).dropna())
        cm=pd.concat(allr).mean()
        for w,b in ws.items():
            c=b["close"].astype(float)
            r1=c/c.shift(1)-1
            nxt=c.shift(-1)/c-1
            pos=b["postRebalance_current_allocation"].astype(float)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            vol20=r1.rolling(20).std()
            vol120=r1.rolling(60,min_periods=20).std()
            ret20=c/c.shift(20)-1
            d=pd.DataFrame({"coin":coin,"w":w,"i":range(len(b)),"f":b["forecast"].astype(float),"pos":pos,
                "nxt":nxt,"ex":nxt-cm,"gain":pos*nxt,"net":pos*nxt-fee,"fee":fee,"vol20":vol20,
                "vrat":vol20/vol120,"ret20":ret20,"absr20":(ret20/(vol20*np.sqrt(20))).abs()})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    A=D[D.f>0].dropna(subset=["nxt","vol20","ret20"]).copy()
    A["fq"]=pd.qcut(A.f,5,labels=False)
    def tt(x): return x.mean()/(x.std()/np.sqrt(len(x)))
    out["fq_net"]=A.groupby("fq").agg(n=("ex","size"),gain=("gain","mean"),fee=("fee","mean"),net=("net","mean"),t_ex=("ex",tt))
    A["vq"]=pd.qcut(A.vol20,4,labels=False)
    out["vol_t"]=A.groupby("vq").agg(n=("ex","size"),ex=("ex","mean"),t_ex=("ex",tt),net=("net","mean"),fee=("fee","mean"))
    A["aq"]=pd.qcut(A.absr20,4,labels=False)
    out["abs_trend_scaled"]=A.groupby("aq").agg(n=("ex","size"),a=("absr20","mean"),ex=("ex","mean"),t_ex=("ex",tt),net=("net","mean"))
    A["rq"]=pd.qcut(A.vrat,4,labels=False)
    out["vol_ratio"]=A.groupby("rq").agg(n=("ex","size"),vr=("vrat","mean"),ex=("ex","mean"),t_ex=("ex",tt),net=("net","mean"))
    # slope within vol halves
    for h,g in A.groupby(A.vol20>A.vol20.median()):
        s=stats.linregress(g.f,g.ex); out[f"slope_highvol_{h}"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(g)})
    # book daily with state
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(pd.DataFrame({"coin":coin,"w":w,"i":range(len(t)),"br":t["book_return"].values}))
    B=pd.concat(dd)
    bk=B.groupby(["w","i"]).br.mean().reset_index()
    bk["wn"]=bk.w.str[1:].astype(int)
    bk=bk.sort_values(["wn","i"]).dropna().reset_index(drop=True)
    eq=(1+bk.br).cumprod(); dd_=eq/eq.cummax()-1
    bk["dd"]=dd_.values
    # worst 30 days of book: state of positions
    D2=D.copy(); D2["i2"]=D2.i
    st=D2.groupby(["w","i"]).agg(pos=("pos","mean"),vol=("vol20","mean"),r20=("ret20","mean")).reset_index()
    m=bk.merge(st,on=["w","i"],how="left")
    m["bq"]=pd.qcut(m.br,10,labels=False)
    out["book_deciles_state"]=m.groupby("bq").agg(br=("br","mean"),pos=("pos","mean"),vol=("vol","mean"),r20=("r20","mean"))
    m["indd"]=m.dd< -0.15
    out["deep_dd_state"]=m.groupby("indd").agg(n=("br","size"),br=("br","mean"),pos=("pos","mean"),vol=("vol","mean"),r20=("r20","mean"))
    return out
