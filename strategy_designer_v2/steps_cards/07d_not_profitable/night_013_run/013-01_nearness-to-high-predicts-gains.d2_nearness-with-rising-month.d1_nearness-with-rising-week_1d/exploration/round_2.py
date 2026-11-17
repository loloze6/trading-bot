def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    brs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            b["ret1"]=b["close"].shift(-1)/b["close"]-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["ret1"]
            b["coin"]=c; b["w"]=w
            b["dist"]=b["close"]/b["close"].rolling(364,min_periods=1).max()-1
            b["m30"]=b["close"]/b["close"].shift(30)-1
            b["m7"]=b["close"]/b["close"].shift(7)-1
            b["fwd7"]=b["close"].shift(-7)/b["close"]-1
            b["grid"]=(np.arange(len(b))%7==0)
            brs.append(b)
    B=pd.concat(brs)
    cm=B[B.grid].groupby("coin").fwd7.mean()
    B["ex7"]=B.fwd7-B.coin.map(cm)
    tot=B.gain.sum()
    out["gain_split"]=pd.Series({
        "share_gain_from_long":B.gain[B.pos>0].sum()/tot,
        "share_gain_from_short":B.gain[B.pos<0].sum()/tot,
        "share_bars_short":(B.pos<0).mean(),
        "share_bars_flat":(B.pos.abs()<1e-9).mean(),
        "mean_ret1_when_short":B.ret1[B.pos<0].mean(),
        "mean_ret1_when_flat":B.ret1[B.pos.abs()<1e-9].mean(),
        "mean_ret1_when_long":B.ret1[B.pos>0].mean(),
        "mean_pos_when_long":B.pos[B.pos>0].mean()})
    G=B[B.grid&(B.regime=="trending")].dropna(subset=["ex7","dist","m30","m7"])
    res={}
    for v in ["dist","m30","m7"]:
        z=(G[v]-G[v].mean())/G[v].std()
        s=stats.linregress(z,G.ex7); res[v]=(s.slope,s.slope/s.stderr,len(G))
    out["trend_grid_univ"]=pd.DataFrame(res,index=["slope","t","n"]).T
    N=B[B.grid&(B.regime!="trending")].dropna(subset=["ex7","dist","m30","m7"])
    res={}
    for v in ["dist","m30","m7"]:
        z=(N[v]-N[v].mean())/N[v].std()
        s=stats.linregress(z,N.ex7); res[v]=(s.slope,s.slope/s.stderr,len(N))
    out["nontrend_grid_univ"]=pd.DataFrame(res,index=["slope","t","n"]).T
    G=G.copy(); G["dq"]=pd.qcut(G.dist.rank(method="first"),5,labels=False)
    out["trend_grid_dist_q"]=G.groupby("dq").agg(dist=("dist","mean"),ex7=("ex7","mean"),fwd7=("fwd7","mean"),n=("ex7","size"))
    G["vq"]=pd.qcut(G.sizing_realised_vol.rank(method="first"),3,labels=False)
    out["trend_grid_by_vol_dist"]=G.groupby(["vq",G.dist>G.dist.median()]).agg(ex7=("ex7","mean"),n=("ex7","size"))
    out["trend_top_fc_pos_by_vol"]=B[(B.regime=="trending")&(B.forecast>6)].assign(vq=lambda x:pd.qcut(x.sizing_realised_vol,3,labels=False)).groupby("vq").agg(vol=("sizing_realised_vol","mean"),pos=("pos","mean"),ret1=("ret1","mean"),gain=("gain","mean"))
    return out
