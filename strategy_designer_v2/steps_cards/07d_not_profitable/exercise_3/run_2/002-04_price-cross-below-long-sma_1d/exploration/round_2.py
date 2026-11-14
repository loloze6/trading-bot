def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float)
            al=b["postRebalance_current_allocation"].astype(float)
            fc=b["forecast"].astype(float)
            r10=cl.shift(-10)/cl-1
            m20=cl/cl.shift(20)-1
            lo60=cl/cl.rolling(60).min()-1
            dd60=cl/cl.rolling(60).max()-1
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(len(b)),"al":al,"fc":fc,"r10":r10,"r1":cl.shift(-1)/cl-1,
                            "m20":m20,"lo60":lo60,"dd60":dd60,"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows)
    mu=D.groupby("coin")["r1"].mean(); D["mu"]=D["coin"].map(mu)
    D["ex10"]=D["r10"]-10*D["mu"]
    blk=D[(D["pos"]%10==0)&D["ex10"].notna()].copy()
    act=blk[blk["al"]<0].copy()
    act["prod"]=act["al"]*act["ex10"]
    def summ(g):
        x=g["prod"]
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"meanex10":g["ex10"].mean()})
    out={}
    act["deep"]=act["fc"]<=-10
    act["m20neg"]=act["m20"]<-0.15
    out["deep_x_m20"]=act.groupby(["deep","m20neg"]).apply(summ)
    act["lo60b"]=pd.qcut(act["lo60"],4)
    out["by_lo60"]=act.groupby("lo60b").apply(summ)
    act["dd60b"]=pd.qcut(act["dd60"],4)
    out["by_dd60"]=act.groupby("dd60b").apply(summ)
    a=act.dropna(subset=["m20"])
    out["corr_m20_ex10"]=pd.Series(stats.spearmanr(a["m20"],a["ex10"]),index=["rho","p"])
    a=act.dropna(subset=["dd60"])
    out["corr_dd60_ex10"]=pd.Series(stats.spearmanr(a["dd60"],a["ex10"]),index=["rho","p"])
    # book falls: worst 20-day book return segments within windows, state at start
    seg=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            d=d.reset_index(drop=True)
            br=d["book_return"].fillna(0); cr=d["coin_return"].fillna(0)
            for s in range(0,len(d)-20,20):
                seg.append({"coin":c,"win":w,"book20":(1+br[s:s+20]).prod()-1,"coin20":(1+cr[s:s+20]).prod()-1})
    S=pd.DataFrame(seg)
    S["q"]=pd.qcut(S["book20"],[0,0.05,0.2,0.8,1])
    out["book_segments"]=S.groupby("q")[["book20","coin20"]].agg(["mean","count"])
    out["worst5pct_coin_up_share"]=float((S.loc[S.book20<=S.book20.quantile(0.05),"coin20"]>0).mean())
    return out
