def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    # book daily returns: mean over coins per day
    rows=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D=pd.concat(rows)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean()
    out["book_overall"]=pd.Series({"book_mean":bk.book_return.mean(),"hold_mean":bk.coin_return.mean(),"n_days":len(bk)})
    out["per_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    # per bar: allocation, regime, gain
    br=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy()
            b["r1"]=b.close.shift(-1)/b.close-1
            b["r5"]=b.close.shift(-5)/b.close-1
            b["coin"]=c;b["w"]=w;b["pos"]=np.arange(len(b))
            br.append(b[["coin","w","pos","close","forecast","regime","postRebalance_current_allocation","r1","r5"]])
    B=pd.concat(br)
    B["alloc"]=B.postRebalance_current_allocation
    mu=B.groupby("coin").r1.mean()
    B["mu"]=B.coin.map(mu)
    B["gain"]=B.alloc*B.r1
    B["mkt"]=B.alloc*B.mu
    B["inpos"]=B.alloc.abs()>1e-6
    out["exposure"]=pd.Series({"share_bars_in":B.inpos.mean(),"mean_alloc_when_in":B.loc[B.inpos,"alloc"].mean(),
        "mean_alloc_all":B.alloc.mean(),"gain_per_bar":B.gain.mean(),"mkt_part":B.mkt.mean(),"timing":(B.gain-B.mkt).mean(),
        "share_regime_trending":(B.regime=="trending").mean(),"share_fc_pos":(B.forecast>0).mean()})
    # coin's 1-day excess return by state
    B["ex1"]=B.r1-B.mu
    B["state"]=np.where(B.inpos,"in",np.where(B.regime=="trending","trend_flat","out"))
    out["state_ex1"]=B.groupby("state").agg(n=("ex1","size"),ex1_mean=("ex1","mean"),r1=("r1","mean"))
    # 5-day grid: excess return by forecast bucket in regime
    G=B[(B.pos%5==0)].dropna(subset=["r5"]).copy()
    mu5=G.groupby("coin").r5.mean(); G["ex5"]=G.r5-G.coin.map(mu5)
    G["fb"]=pd.cut(G.forecast,[-21,-0.001,0.001,5,10,15,21])
    out["grid_fc"]=G.groupby("fb").agg(n=("ex5","size"),ex5=("ex5","mean"),r5=("r5","mean"),alloc=("alloc","mean"))
    out["grid_state"]=G.groupby("state").agg(n=("ex5","size"),ex5=("ex5","mean"),r5=("r5","mean"))
    # outside regime: does coin rise when merely above cloud? compute cloud position recomputed
    res=[]
    for c in bars:
        for w,b in bars[c].items():
            h,l,cl=b.high,b.low,b.close
            t=(h.rolling(9).max()+l.rolling(9).min())/2; k=(h.rolling(26).max()+l.rolling(26).min())/2
            sa=((t+k)/2).shift(26); sb=((h.rolling(52).max()+l.rolling(52).min())/2).shift(26)
            top=np.maximum(sa,sb); bot=np.minimum(sa,sb); mid=(sa+sb)/2
            sl=mid.pct_change(26)
            r5=cl.shift(-5)/cl-1
            df=pd.DataFrame({"coin":c,"above":cl>top,"below":cl<bot,"slope_up":sl>0,"r5":r5,"pos":np.arange(len(b)),
                             "width":(sa-sb).abs()/cl*100, "dist":(cl-top)/cl*100,"alloc":b.postRebalance_current_allocation.values})
            res.append(df)
    R=pd.concat(res); R=R[R.pos%5==0].dropna(subset=["r5","width"])
    R["ex5"]=R.r5-R.coin.map(mu5)
    R["cs"]=np.select([R.above&R.slope_up,R.above&~R.slope_up,R.below&~R.slope_up,R.below&R.slope_up],["above_up","above_down","below_down","below_up"],"inside")
    out["cloud_states"]=R.groupby("cs").agg(n=("ex5","size"),ex5=("ex5","mean"),r5=("r5","mean"),alloc=("alloc","mean"))
    A=R[R.cs=="above_up"].copy()
    A["wq"]=pd.qcut(A.width,4,labels=False); A["dq"]=pd.qcut(A.dist,4,labels=False)
    out["above_up_by_width_q"]=A.groupby("wq").agg(n=("ex5","size"),ex5=("ex5","mean"),w=("width","mean"),alloc=("alloc","mean"))
    out["above_up_by_dist_q"]=A.groupby("dq").agg(n=("ex5","size"),ex5=("ex5","mean"),d=("dist","mean"),alloc=("alloc","mean"))
    return out
