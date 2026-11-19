def explore(data):
    import numpy as np, pandas as pd
    rows=[]; drow=[]; grid=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            cl=b["close"].astype(float)
            r=cl.shift(-1)/cl-1
            a=b["postRebalance_current_allocation"].fillna(0)
            pa=b["previous_allocation"].fillna(0)
            g=a*r
            tpv=b["total_portfolio_value"]; ptv=b["postRebalance_total_value"]
            fee=((tpv-ptv)/tpv).clip(lower=0)
            turn=(a-pa).abs()
            d=cl.diff(); up=d.clip(lower=0).rolling(336,min_periods=100).mean(); dn=(-d).clip(lower=0).rolling(336,min_periods=100).mean()
            rsi=100-100/(1+up/dn)
            ret60=cl/cl.shift(1440)-1
            hr=pd.to_datetime(b["timestamp"]).dt.hour
            df=pd.DataFrame({"coin":c,"w":w,"g":g,"fee":fee,"a":a,"turn":turn,"r":r,"regime":b["regime"].values,"rsi":rsi,"fc":b["forecast"],"dfc":b["forecast"].diff().abs()})
            rows.append(df)
            dd=data["days"][c][w]
            drow.append(pd.DataFrame({"coin":c,"w":w,"br":dd["book_return"].values,"cr":dd["coin_return"].values}))
            n=len(cl); cv=cl.values
            for i in range(0,n-240,240):
                grid.append({"coin":c,"w":w,"fc":b["forecast"].iloc[i],"rsi":rsi.iloc[i],"f240":cv[i+240]/cv[i]-1,"tr":b["regime"].iloc[i]=="trending"})
    A=pd.concat(rows,ignore_index=True); D=pd.concat(drow,ignore_index=True).dropna(); G=pd.DataFrame(grid)
    out={}
    out["totals"]=pd.Series({"gross/bar":A.g.mean(),"fee/bar":A.fee.mean(),"gross/day":A.g.mean()*24,"fee/day":A.fee.mean()*24,"turnover/bar":A.turn.mean(),"mean|alloc|":A.a.abs().mean(),"long share":(A.a>0).mean(),"short share":(A.a<0).mean(),"trending share":(A.regime=="trending").mean(),"mean |dforecast|/bar":A.dfc.mean()})
    A["side"]=np.sign(A.a)
    out["by side"]=A.groupby("side").agg(n=("g","size"),gross=("g","mean"),fee=("fee","mean"),turn=("turn","mean"),alloc=("a","mean"),r=("r","mean"))
    A["fcb"]=pd.cut(A.fc,[-21,-10,-5,-1e-9,1e-9,5,10,21])
    out["by forecast bin"]=A.groupby("fcb").agg(n=("g","size"),gross=("g","mean"),fee=("fee","mean"),alloc=("a","mean"),r=("r","mean"),rsi=("rsi","mean"))
    A["rsib"]=pd.cut(A.rsi,[0,45,50,55,60,65,100])
    T=A[A.regime=="trending"]
    out["trending by rsi"]=T.groupby("rsib").agg(n=("g","size"),gross=("g","mean"),fee=("fee","mean"),alloc=("a","mean"),r=("r","mean"),fc=("fc","mean"))
    out["by coin"]=A.groupby("coin").agg(gross=("g","mean"),fee=("fee","mean"),turn=("turn","mean"))
    out["daily"]=pd.Series({"book mean":D.br.mean(),"book sd":D.br.std(),"coin mean":D.cr.mean(),"n days":len(D)})
    Gt=G[G.tr].copy(); Gt["rb"]=pd.cut(Gt.rsi,[0,45,50,55,60,65,100])
    mu=G.groupby("coin").f240.mean(); Gt["ex"]=Gt.f240-Gt.coin.map(mu)
    out["grid trending by rsi"]=Gt.groupby("rb").ex.agg(["count","mean"])
    out["corr fc rsi trending"]=float(T[["fc","rsi"]].corr().iloc[0,1])
    out["trade stats"]=pd.Series({"n trades":sum(len(data["trades"][c][w]) for c in data["trades"] for w in data["trades"][c]),
        "mean dur h":pd.concat([data["trades"][c][w] for c in data["trades"] for w in data["trades"][c]]).duration_minutes.mean()/60})
    return out
