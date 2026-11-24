def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b.timestamp)})
            d["flat"]=1-(c-o).abs()/rng.replace(0,np.nan)
            d["rise5"]=c/c.shift(5)-1
            d["width"]=rng/rng.rolling(20).mean()
            d["clv"]=(c-l)/rng.replace(0,np.nan)
            d["fwd3"]=c.shift(-3)/c-1
            d["pos"]=np.arange(len(b))
            d["fc"]=b.forecast.values
            d["alloc"]=b.postRebalance_current_allocation.values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%3==0)&D.fwd3.notna()].copy()
    G["norm"]=G.groupby("coin").fwd3.transform("mean")
    G["unu"]=G.fwd3-G.norm
    G["day"]=G.ts.dt.floor("D")
    G["year"]=G.ts.dt.year
    def stat(df):
        n=len(df)
        if n<5: return pd.Series({"n":n})
        m=df.unu.mean(); dev=df.unu-m; sd=dev.groupby(df.day).sum()
        se=np.sqrt((sd**2).sum())/n
        return pd.Series({"n":n,"days":df.day.nunique(),"mean_unu":m,"t":m/se,"hit":(df.fwd3>0).mean()})
    out={}
    dn=G[(G.rise5<0)&(G.width>1.4)].copy()
    dn["hiclose"]=dn.clv>0.8
    out["down-run wide, clv>0.8 by year"]=dn[dn.hiclose].groupby("year").apply(stat)
    dn["wq"]=pd.cut(dn.width,[1.4,2,3,99])
    out["down-run wide clv>0.8 by width"]=dn[dn.hiclose].groupby("wq").apply(stat)
    # graded: wide down-run days, correlation of clv with unu
    wd=G[(G.rise5<0)&(G.width>1)]
    out["corr clv vs unu, down-run width>1 (spearman, n)"]=pd.Series({"rho":wd[["clv","unu"]].corr("spearman").iloc[0,1],"n":len(wd)})
    up=G[(G.rise5>0)&(G.width>1)].copy()
    up["flq"]=pd.cut(up.flat,[-.01,.3,.6,.9,1.01])
    out["up-run width>1 by flatness"]=up.groupby("flq").apply(stat)
    up["clvq"]=pd.cut(up.clv,[-.01,.33,.66,1.01])
    out["up-run width>1 by clv"]=up.groupby("clvq").apply(stat)
    # tested signal by year
    act=G[(G.flat>=0.9)&(G.rise5>0)&(G.width>1)]
    out["tested situation by year"]=act.groupby("year").apply(stat)
    # book: days, largest gains/losses
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
    DD=pd.concat(dd)
    B=DD.groupby("day").agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    B=B.sort_values("br")
    out["book worst/best 20 days: mean book, mean coins"]=pd.DataFrame({"worst20":[B.br.head(20).mean(),B.cr.head(20).mean()],"best20":[B.br.tail(20).mean(),B.cr.tail(20).mean()]},index=["book","coins"])
    out["share of book total from best 20 days"]=float(B.br.tail(20).sum()/B.br.sum())
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    T["dur_d"]=T.duration_minutes/1440
    T["dq"]=pd.cut(T.dur_d,[0,2.5,3.5,6,999])
    out["trades by duration"]=T.groupby("dq").net_profit_loss_percent.agg(["count","mean","median"])
    out["trades by coin"]=T.groupby("coin").net_profit_loss_percent.agg(["count","mean"])
    return out
