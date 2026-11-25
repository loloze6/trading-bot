def explore(data):
    import pandas as pd, numpy as np
    rows=[]; days=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            rng=(b.high-b.low)
            clh=(b.high-b.close)/rng.replace(0,np.nan)
            r=b.close.pct_change()
            nxt=b.close.shift(-1)/b.close-1
            nxt2=b.close.shift(-2)/b.close-1
            tr60=b.close/b.close.shift(60)-1
            vol30=r.rolling(30,min_periods=20).std()
            vol20=r.rolling(20,min_periods=10).std()
            rngrel=(rng/b.close)/vol20
            d=pd.DataFrame({"coin":coin,"w":w,"clh":clh,"nxt":nxt,"nxt2":nxt2,"tr60":tr60,"vol30":vol30,
                "rngrel":rngrel,"alloc":b.postRebalance_current_allocation,"pos":np.arange(len(b))})
            rows.append(d)
        for w,dd in data["days"][coin].items():
            days.append(dd.assign(coin=coin,w=w))
    D=pd.concat(rows)
    D["volmed"]=D.coin.map(D.groupby("coin").vol30.median())
    D["agit"]=np.where(D.vol30.isna(),np.nan,np.where(D.vol30>D.volmed,"agit","calm"))
    D["trend"]=pd.cut(D.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    D["clmean"]=D.coin.map(D.groupby("coin").clh.mean())
    D["sig"]=D.clh-D.clmean
    m1=D.groupby("coin").nxt.mean(); D["ex"]=D.nxt-D.coin.map(m1)
    out={}
    def tt(x): 
        x=x.dropna(); return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    E=D.dropna(subset=["ex","sig"])
    E["sx"]=E.sig*E.ex
    out["graded sig*ex by agit"]=E.groupby("agit").sx.apply(tt).unstack()
    out["graded sig*ex by trend"]=E.groupby("trend").sx.apply(tt).unstack()
    out["graded sig*ex by trend x agit"]=E.groupby(["trend","agit"]).sx.apply(tt).unstack()
    # condition alone: plain ex by profile (what holding long earns there)
    out["condition alone: ex mean by agit"]=E.groupby("agit").ex.apply(tt).unstack()
    out["condition alone: ex mean by trend"]=E.groupby("trend").ex.apply(tt).unstack()
    # long side only (clh above coin mean) vs not, in agit
    E["side"]=np.where(E.sig>0,"long","short")
    E["dir"]=np.where(E.side=="long",E.ex,-E.ex)
    out["directional ex by side x agit"]=E.groupby(["side","agit"]).dir.apply(tt).unstack()
    out["directional ex by side x trend"]=E.groupby(["side","trend"]).dir.apply(tt).unstack()
    # 2-day horizon non-overlapping
    m2=D.groupby("coin").nxt2.mean(); D["ex2"]=D.nxt2-D.coin.map(m2)
    G=D[(D.pos%2==0)].dropna(subset=["ex2","sig"])
    out["2day graded sig*ex2 (non-overlap) by agit"]=G.assign(s=G.sig*G.ex2).groupby("agit").s.apply(tt).unstack()
    # strength per usual move, agit long-side
    usual=D.groupby("coin").nxt.std()
    E["str"]=E.dir/E.coin.map(usual)
    out["strength by side x agit (extreme |sig|>0.3)"]=E[E.sig.abs()>0.3].groupby(["side","agit"]).str.apply(tt).unstack()
    # simulated full-size graded position: pos = clip(sig/0.5,-1,1), net of 0.095% per unit turnover
    for name,mask in [("all",E.index==E.index),("agit only",(E.agit=="agit").values),("agit long only",((E.agit=="agit")&(E.sig>0)).values),("fall-or-agit long",(((E.agit=="agit")|(E.trend=="fall"))&(E.sig>0)).values)]:
        S=E.copy(); S["p"]=np.clip(S.sig/0.5,-1,1)*mask
        S=S.sort_values(["coin","w","pos"])
        S["turn"]=S.groupby(["coin","w"]).p.diff().abs().fillna(S.p.abs())
        S["net"]=S.p*S.nxt-S.turn*0.00095
        out["sim "+name]=pd.Series({"gross/bar":(S.p*S.nxt).mean(),"net/bar":S.net.mean(),"share in pos":(S.p!=0).mean(),
            "net per bar in pos":S.net[S.p!=0].mean(),"t net":S.net.mean()/S.net.std()*np.sqrt(len(S))})
    # book falls: deepest drawdown per window, profile composition of losing book days
    DD=pd.concat(days)
    bd=DD.groupby(["w","day"]).book_return.mean().dropna()
    eq=(1+bd).cumprod(); ddn=eq/eq.cummax()-1
    out["book max dd, yearly"]=pd.Series({"maxdd":ddn.min(),"mean daily":bd.mean(),"sd":bd.std()})
    out["book worst dd by window"]=ddn.groupby(level=0).min()
    return out
