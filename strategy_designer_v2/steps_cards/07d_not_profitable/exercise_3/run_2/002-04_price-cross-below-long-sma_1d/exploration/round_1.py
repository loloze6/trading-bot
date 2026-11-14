def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].astype(float)
            al=b["postRebalance_current_allocation"].astype(float)
            raw=b.get("debug_info.components.below_ma.last_history_value")
            fc=b["forecast"].astype(float)
            r1=cl.shift(-1)/cl-1
            r10=cl.shift(-10)/cl-1
            mom20=cl/cl.shift(20)-1
            mom60=cl/cl.shift(60)-1
            vol=np.log(cl).diff().rolling(20).std()
            fees=(b["postRebalance_total_value"].astype(float)/b["total_portfolio_value"].astype(float)-1)
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(len(b)),"al":al,"fc":fc,"raw":raw.astype(float) if raw is not None else np.nan,
                            "r1":r1,"r10":r10,"m20":mom20,"m60":mom60,"vol":vol,"fee":fees,"year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows)
    # coin mean daily return pooled
    mu=D.groupby("coin")["r1"].mean()
    D["mu"]=D["coin"].map(mu)
    D["g1"]=D["al"]*D["r1"]
    D["ex10"]=D["r10"]-10*D["mu"]
    blk=D[(D["pos"]%10==0)&D["ex10"].notna()].copy()
    blk["prod"]=blk["al"]*blk["ex10"]
    act=blk[blk["al"]<0].copy()
    def summ(g):
        x=g["prod"]; 
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"meanex10":g["ex10"].mean(),"alloc":g["al"].mean()})
    act["fcb"]=pd.cut(act["fc"],[-21,-15,-10,-5,-2,0])
    act["m20b"]=pd.qcut(act["m20"],4)
    act["m60b"]=pd.qcut(act["m60"],4)
    act["rawb"]=pd.qcut(act["raw"],4)
    act["volb"]=pd.qcut(act["vol"],3)
    out={}
    out["by_fc"]=act.groupby("fcb").apply(summ)
    out["by_raw"]=act.groupby("rawb").apply(summ)
    out["by_m20"]=act.groupby("m20b").apply(summ)
    out["by_m60"]=act.groupby("m60b").apply(summ)
    out["by_vol"]=act.groupby("volb").apply(summ)
    out["by_coin"]=act.groupby("coin").apply(summ)
    out["by_year"]=act.groupby("year").apply(summ)
    # daily gains
    dd=D[D["r1"].notna()]
    out["daily"]=pd.Series({"gross_mean_g1":dd["g1"].mean(),"fee_mean":dd["fee"].mean(),"share_short":(dd["al"]<0).mean(),
                            "mean_g1_short":dd.loc[dd.al<0,"g1"].mean(),"mean_r1_short":dd.loc[dd.al<0,"r1"].mean(),"mean_r1_flat":dd.loc[dd.al==0,"r1"].mean(),"mean_mu":mu.mean()})
    # book daily
    bk=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            bk.append(d.assign(coin=c,win=w))
    B=pd.concat(bk)
    out["book_by_win"]=B.groupby("win")[["book_return","coin_return"]].sum()
    return out
