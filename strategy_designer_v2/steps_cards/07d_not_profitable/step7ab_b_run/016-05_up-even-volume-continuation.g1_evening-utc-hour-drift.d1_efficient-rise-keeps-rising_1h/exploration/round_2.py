def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    coins = list(bars.keys())
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r1=cl.pct_change()
            r72=cl/cl.shift(72)-1
            eff=(cl-cl.shift(72)).abs()/(cl.diff().abs().rolling(72).sum())
            r720=cl/cl.shift(720)-1
            hi=cl/cl.rolling(720).max()-1
            f72=cl.shift(-72)/cl-1
            a=b["postRebalance_current_allocation"]
            pg=a*(cl.shift(-1)/cl-1)
            # forward 72-bar min drawdown of the coin
            fmin=cl[::-1].rolling(73,min_periods=1).min()[::-1]/cl-1
            d=pd.DataFrame({"coin":c,"win":w,"r72":r72,"eff":eff,"r720":r720,"hi":hi,"f72":f72,"fmin":fmin,
                            "a":a,"pg":pg,"fc":b["forecast"],"reg":b["regime"],"grid":(np.arange(len(b))%72==0)})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D[D.grid].groupby("coin")["f72"].mean()
    D["ex"]=D["f72"]-D["coin"].map(mu)
    out={}
    out["forecast_desc_trending"]=D.loc[D.reg=="trending","fc"].describe()
    out["share_long_by_regime"]=D.groupby("reg").agg(share_long=("a",lambda x:(x>0).mean()),mean_a=("a","mean"),n=("a","size"))
    G=D[D.grid&(D.fc>0)].dropna(subset=["f72","eff","r720"])
    G["efft"]=pd.qcut(G["eff"],3,labels=["eff_lo","eff_mid","eff_hi"])
    G["trend"]=np.where(G["r720"]>0,"r720_up","r720_down")
    def agg(x):
        return pd.Series({"n":len(x),"mean_f72":x["f72"].mean(),"mean_ex":x["ex"].mean(),
                          "t_ex":x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))),
                          "mean_fmin":x["fmin"].mean(),"share_fmin_lt_-10pct":(x["fmin"]<-0.10).mean()})
    out["grid_eff_x_trend"]=G.groupby(["efft","trend"]).apply(agg)
    G["hit"]=pd.qcut(G["hi"],3,labels=["far","mid","near"])
    out["grid_eff_x_high"]=G.groupby(["efft","hit"]).apply(agg)
    # hourly book gain by state, and loss share
    H=D[D.a>0].dropna(subset=["eff","r720"])
    H["efft"]=pd.qcut(H["eff"],3,labels=["eff_lo","eff_mid","eff_hi"])
    H["trend"]=np.where(H["r720"]>0,"r720_up","r720_down")
    H["r72s"]=np.where(H["r72"]>0,"r72_up","r72_down")
    out["hourly_gain_state"]=H.groupby(["r72s","trend","efft"])["pg"].agg(["sum","mean","size"])
    # std of position gain per state (risk)
    out["hourly_gain_risk"]=H.groupby(["r72s","trend"])["pg"].agg(["mean","std","size"])
    return out
