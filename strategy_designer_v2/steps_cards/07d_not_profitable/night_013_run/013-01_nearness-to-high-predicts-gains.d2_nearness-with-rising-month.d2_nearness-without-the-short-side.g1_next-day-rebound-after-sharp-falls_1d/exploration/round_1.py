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
            b=b.copy()
            c=b["close"].astype(float)
            r1=c/c.shift(1)-1
            nxt=c.shift(-1)/c-1
            pos=b["postRebalance_current_allocation"].astype(float)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            vol20=r1.rolling(20).std()
            ret20=c/c.shift(20)-1
            ret5=c.shift(1)/c.shift(6)-1
            hi20=c.rolling(20).max()
            near=c/hi20-1
            d=pd.DataFrame({"coin":coin,"w":w,"f":b["forecast"].astype(float),"pos":pos,
                "nxt":nxt,"ex":nxt-cm,"gain":pos*nxt,"fee":fee,"r1":r1,"vol20":vol20,
                "ret20":ret20,"near":near,"ret5":ret5,"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    A=D[D.f>0].dropna(subset=["nxt"])
    A["fq"]=pd.qcut(A.f,5,labels=False,duplicates="drop")
    out["fq_next"]=A.groupby("fq").agg(n=("ex","size"),fmean=("f","mean"),ex=("ex","mean"),pos=("pos","mean"),gain=("gain","mean"))
    D["held"]=D.pos.abs()>1e-9
    out["held_vs_f"]=D.groupby([D.f>0,D.held]).agg(n=("nxt","size"),gain=("gain","mean"),ex=("ex","mean"),pos=("pos","mean"))
    out["gain_fee"]=pd.Series({"mean_gain_per_bar":D.gain.mean(),"mean_fee_per_bar":D.fee.mean(),"share_held":D.held.mean()})
    # regime: 20d trend
    A=A.dropna(subset=["ret20"])
    A["t20"]=pd.qcut(A.ret20,4,labels=False)
    out["by_ret20"]=A.groupby("t20").agg(n=("ex","size"),r20=("ret20","mean"),ex=("ex","mean"),gain=("gain","mean"),fee=("fee","mean"))
    A["nq"]=pd.qcut(A.near,4,labels=False)
    out["by_near"]=A.groupby("nq").agg(n=("ex","size"),near=("near","mean"),ex=("ex","mean"),gain=("gain","mean"))
    A["vq"]=pd.qcut(A.vol20,4,labels=False)
    out["by_vol"]=A.groupby("vq").agg(n=("ex","size"),vol=("vol20","mean"),ex=("ex","mean"),gain=("gain","mean"))
    out["by_year"]=A.groupby("year").agg(n=("ex","size"),ex=("ex","mean"),gain=("gain","mean"))
    out["by_coin"]=A.groupby("coin").agg(n=("ex","size"),ex=("ex","mean"),gain=("gain","mean"))
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(pd.DataFrame({"coin":coin,"w":w,"i":range(len(t)),"br":t["book_return"].values,"cr":t["coin_return"].values}))
    B=pd.concat(dd)
    bk=B.groupby(["w","i"]).agg(br=("br","mean"),cr=("cr","mean")).reset_index()
    bk["wn"]=bk.w.str[1:].astype(int)
    bk=bk.sort_values(["wn","i"]).dropna()
    eq=(1+bk.br).cumprod(); dd_=eq/eq.cummax()-1
    out["book"]=pd.Series({"mean":bk.br.mean(),"sd":bk.br.std(),"maxdd":dd_.min(),"n":len(bk)})
    out["book_by_window"]=bk.groupby("wn").agg(br=("br","mean"),cr=("cr","mean"),n=("br","size"))
    return out
