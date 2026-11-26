def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            r1=pd.Series(c).pct_change().values
            sd30=pd.Series(r1).rolling(30).std().values
            raw=r1/sd30
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            h=5
            for i in range(0,len(b)-h,h):
                rows.append(dict(coin=coin,win=w,year=yr[i],fwd=c[i+h]/c[i]-1,
                    fc=b["forecast"].iloc[i],reg=b["regime"].iloc[i],raw=raw[i]))
    df=pd.DataFrame(rows)
    df["mu"]=df.groupby("coin")["fwd"].transform("mean")
    df["ex"]=df["fwd"]-df["mu"]
    out={}
    def slope(g,x):
        g=g.dropna(subset=["ex",x])
        if len(g)<5: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[x],g["ex"])
        return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    pos=df[df.fc>0]
    out["share_fc_at_cap"]=float((pos.fc>=19.99).mean())
    out["slope_ex_on_raw_pos_fc"]=slope(pos,"raw")
    inp=df[(df.reg=="unknown")&(df.raw>0)]
    out["slope_ex_on_raw_inprof_up"]=slope(inp,"raw")
    out["slope_by_window_pos"]=pos.groupby("win").apply(lambda g: slope(g,"fc"))
    out["slope_by_year_pos"]=pos.groupby("year").apply(lambda g: slope(g,"fc"))
    out["slope_pos_excl_2018"]=slope(pos[pos.year!=2018],"fc")
    out["ex_std_pos"]=float(pos.ex.std())
    return out
