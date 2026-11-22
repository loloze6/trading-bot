def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            r1=b.close.pct_change()
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["alloc"]=b.postRebalance_current_allocation
            b["ret168"]=b.close/b.close.shift(168)-1
            b["ret720"]=b.close/b.close.shift(720)-1
            sd=r1.rolling(720,min_periods=200).std()
            b["z"]=r1/sd
            b["vr"]=b.volume/b.volume.rolling(720,min_periods=200).mean()
            b["prod"]=b.z*b.vr
            b["fwd24"]=b.close.shift(-24)/b.close-1
            b["pos"]=np.arange(len(b)); b["coin"]=c; b["w"]=w
            b["peak720"]=b.close/b.close.rolling(720,min_periods=200).max()-1
            recs.append(b[["coin","w","pos","forecast","alloc","nxt","ret168","ret720","z","vr","prod","fwd24","peak720"]])
    B=pd.concat(recs)
    drift1=B.nxt.mean()
    out["alloc_quantiles_when_in"]=B.loc[B.alloc.abs()>1e-6,"alloc"].quantile([.1,.25,.5,.75,.9])
    out["share_forecast_pos"]=(B.forecast>0).mean()
    out["corr_alloc_forecast"]=B[["alloc","forecast"]].corr().iloc[0,1]
    B["gain"]=B.alloc*B.nxt
    out["gain_split"]=pd.Series({"mean_gain_bar":B.gain.mean(),"market_part":(B.alloc*drift1).mean(),"timing":B.gain.mean()-(B.alloc*drift1).mean()})
    # bar-level gain by position state vs drawdown from 30d high
    B["ddq"]=pd.qcut(B.peak720.rank(method="first"),5,labels=False)
    out["nxt_by_dd_from_30d_high_q"]=B.dropna(subset=["peak720"]).groupby("ddq").agg(n=("nxt","size"),mean_nxt=("nxt","mean"),share_in=("alloc",lambda a:(a.abs()>1e-6).mean()),mean_gain=("gain","mean"))
    # cases (grid) on prod top: interaction vr quintile x prior 7d sign
    G=B[(B.pos%24==0)].dropna(subset=["fwd24","ret168","prod"]).copy()
    drift=G.fwd24.mean()
    G["u"]=G.fwd24-drift
    def tt(x): return pd.Series({"n":len(x),"mean_u":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    up=G[G.z>0].copy()
    up["pq"]=pd.qcut(up["prod"].rank(method="first"),5,labels=False)
    up["t7"]=np.where(up.ret168>0,"7d_up","7d_down")
    out["uphour_grid_by_prod_q_and_7d"]=up.groupby(["t7","pq"]).u.apply(tt).unstack()
    dn=G[G.z<0].copy()
    dn["pq"]=pd.qcut((-dn["prod"]).rank(method="first"),5,labels=False)
    dn["t7"]=np.where(dn.ret168>0,"7d_up","7d_down")
    out["downhour_grid_by_absprod_q_and_7d"]=dn.groupby(["t7","pq"]).u.apply(tt).unstack()
    # all grid bars: 24h forward by prior 7d return quintile (trend itself)
    G["t7q"]=pd.qcut(G.ret168,5,labels=False)
    out["allgrid_by_7d_q"]=G.groupby("t7q").u.apply(tt).unstack()
    # book daily in falls: days with pooled book drawdown
    rows=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; rows.append(dd)
    D=pd.concat(rows); P=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"]=P.w.str[1:].astype(int); P=P.sort_values(["wn","day"]).dropna()
    eq=(1+P.book_return).cumprod(); P["dd"]=(eq/eq.cummax()-1).values
    P["indd"]=P.dd< -0.3
    out["book_vs_coin_in_deep_fall_days"]=P.groupby("indd").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    return out
