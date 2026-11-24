def explore(data):
    import numpy as np, pandas as pd
    H=10
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b))})
            d["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            d["r5"]=c/c.shift(5)-1
            d["r20"]=c/c.shift(20)-1
            d["sbody"]=(c-o)/rng.replace(0,np.nan)
            d["rm"]=rng/rng.rolling(20).mean()
            d["lrm"]=np.log(d.rm)
            d["fwd"]=c.shift(-H)/c-1
            d["fwd5"]=c.shift(-5)/c-1
            d["year"]=d.day.dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%H==0)&D.fwd.notna()]
    drift=G.groupby("coin").fwd.mean(); usual=G.groupby("coin").fwd.std()
    D["un"]=D.fwd-D.coin.map(drift)
    D["str"]=D.un/D.coin.map(usual)
    D["cell"]=D.pos//H
    def clus_slope(x,col,y="str"):
        x=x[[col,y,"day"]].dropna()
        X=np.c_[np.ones(len(x)),x[col].values]; Y=x[y].values
        bta=np.linalg.lstsq(X,Y,rcond=None)[0]; e=Y-X@bta
        XtXi=np.linalg.inv(X.T@X)
        S=pd.DataFrame(X*e[:,None]).groupby(x.day.values).sum().values
        nd=len(S); V=XtXi@(S.T@S)@XtXi*nd/(nd-1)
        return pd.Series({"n":len(x),"days":nd,"slope":bta[1],"t":bta[1]/np.sqrt(V[1,1])})
    def cases(mask):
        x=D[mask & D.fwd.notna()].groupby(["coin","win","cell"]).head(1)
        u=x.un; dev=(u-u.mean()).groupby(x.day).sum(); nd=len(dev)
        se=np.sqrt((dev**2).sum()*nd/(nd-1))/len(u)
        return pd.Series({"n":len(x),"days":nd,"unusual":u.mean(),"t":u.mean()/se,"strength":x.str.mean()})
    g=D[(D.pos%H==0)&D.un.notna()&D.rm.notna()].copy()
    out={}
    out["slope_str_on_logrm"]=pd.DataFrame({
        "all":clus_slope(g,"lrm"),
        "r5>0":clus_slope(g[g.r5>0],"lrm"),
        "r5<0":clus_slope(g[g.r5<0],"lrm"),
        "r20>0":clus_slope(g[g.r20>0],"lrm"),
        "r20<0":clus_slope(g[g.r20<0],"lrm"),
        "up_close":clus_slope(g[g.sbody>0],"lrm"),
        "down_close":clus_slope(g[g.sbody<0],"lrm"),
        "|sbody|<=.3":clus_slope(g[g.sbody.abs()<=0.3],"lrm"),
    }).T
    g["r5rm"]=g.r5.clip(lower=0)*g.lrm
    out["slope_str_on_r5_given_wide"]=pd.DataFrame({
        "rm>=1":clus_slope(g[g.rm>=1],"r5"),
        "rm<1":clus_slope(g[g.rm<1],"r5"),
        "all":clus_slope(g,"r5"),"r20_all":clus_slope(g,"r20")}).T
    w=(D.rm>=1.5)&(D.r5>0)
    x=D[w&D.fwd.notna()].groupby(["coin","win","cell"]).head(1)
    out["wide15_up5_by_coin"]=x.groupby("coin").agg(n=("un","size"),un=("un","mean"))
    out["wide15_up5_by_year"]=x.groupby("year").agg(n=("un","size"),un=("un","mean"))
    out["wide15_up5_by_sbody_sign"]=x.groupby(np.sign(x.sbody)).agg(n=("un","size"),un=("un","mean"))
    out["rm_bins_up5"]=pd.DataFrame({k:cases((D.r5>0)&m) for k,m in {
        "rm<0.7":D.rm<0.7,"0.7-1":(D.rm>=0.7)&(D.rm<1),"1-1.5":(D.rm>=1)&(D.rm<1.5),
        "1.5-2":(D.rm>=1.5)&(D.rm<2),">=2":D.rm>=2}.items()}).T
    out["rm_bins_dn5"]=pd.DataFrame({k:cases((D.r5<0)&m) for k,m in {
        "rm<0.7":D.rm<0.7,"0.7-1":(D.rm>=0.7)&(D.rm<1),"1-1.5":(D.rm>=1)&(D.rm<1.5),
        "1.5-2":(D.rm>=1.5)&(D.rm<2),">=2":D.rm>=2}.items()}).T
    # book: days
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; t["win"]=w; dd.append(t)
    DD=pd.concat(dd)
    bk=DD.groupby("day").book_return.mean().dropna()
    out["book_top_days_share"]=pd.Series({"n_days":len(bk),"sum":bk.sum(),"top10_sum":bk.nlargest(10).sum(),"bottom10_sum":bk.nsmallest(10).sum(),"top1pct_sum":bk.nlargest(int(len(bk)*0.01)).sum()})
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    T["dur_d"]=T.duration_minutes/1440
    out["trades_by_coin"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda s:(s>0).mean()),dur=("dur_d","mean"))
    T["fq"]=pd.qcut(T.entry_forecast.rank(method="first"),4,labels=False)
    out["trades_by_entry_fc_q"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),fc=("entry_forecast","mean"))
    return out
