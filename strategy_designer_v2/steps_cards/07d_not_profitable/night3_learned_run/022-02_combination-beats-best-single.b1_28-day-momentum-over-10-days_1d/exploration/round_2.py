def explore(data):
    import numpy as np, pandas as pd
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    windows = sorted(days[coins[0]].keys(), key=lambda w:int(w[1:]))
    out = {}
    recs=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            r=b.close.pct_change().shift(-1)
            a=b.postRebalance_current_allocation
            ret28=b.close/b.close.shift(28)-1
            ret7=b.close/b.close.shift(7)-1
            vol=b.close.pct_change().rolling(20).std()
            dd60=b.close/b.close.rolling(60,min_periods=20).max()-1
            up60=b.close/b.close.rolling(60,min_periods=20).min()-1
            recs.append(pd.DataFrame({"coin":c,"w":w,"wn":int(w[1:]),"pnl":a*r,"a":a,"f":b.forecast,"ret28":ret28,"ret7":ret7,
                "vol":vol,"dd60":dd60,"up60":up60,"r":r,"year":pd.to_datetime(b.timestamp).dt.year}))
    R=pd.concat(recs).dropna(subset=["pnl"])
    R["side"]=np.sign(R.a)
    R["fall_ep"]=R.wn.between(2,8)
    t=lambda s:s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan
    out["episode_by_side"]=R.groupby(["fall_ep","side"]).agg(pnl_bps=("pnl",lambda s:s.mean()*1e4),t=("pnl",t),absA=("a",lambda s:s.abs().mean()),coin_r_bps=("r",lambda s:s.mean()*1e4),n=("pnl","size"))
    out["episode_by_coin"]=R[R.fall_ep].groupby("coin").agg(pnl_bps=("pnl",lambda s:s.mean()*1e4),long_share=("a",lambda s:(s>0).mean()),coin_r_bps=("r",lambda s:s.mean()*1e4))
    S=R[R.side!=0].dropna(subset=["dd60","up60","ret28","ret7"]).copy()
    for col in ["dd60","up60","ret7","vol"]:
        S["q"]=S.groupby("side")[col].transform(lambda x:pd.qcut(x,5,labels=False,duplicates="drop"))
        out["side_x_"+col]=S.groupby(["side","q"]).agg(lo=(col,"min"),hi=(col,"max"),pnl_bps=("pnl",lambda s:s.mean()*1e4),t=("pnl",t),absA=("a",lambda s:s.abs().mean()),n=("pnl","size"))
    # short side: graded by ret28 magnitude
    S["q"]=S.groupby("side")["ret28"].transform(lambda x:pd.qcut(x,5,labels=False,duplicates="drop"))
    out["side_x_ret28"]=S.groupby(["side","q"]).agg(lo=("ret28","min"),hi=("ret28","max"),pnl_bps=("pnl",lambda s:s.mean()*1e4),t=("pnl",t),n=("pnl","size"))
    # daily book contribution split long/short per window group
    R["grp"]=pd.cut(R.wn,[0,1,8,18,21,24],labels=["w1","w2-8","w9-18","w19-21","w22-24"])
    out["contrib_by_grp_side"]=R.groupby(["grp","side"]).pnl.sum().unstack()
    return out
