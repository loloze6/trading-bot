def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # coin mean daily return across windows
        allr=[]
        for w,b in ws.items():
            r=b["close"].pct_change().shift(-1)
            allr.append(r.dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.copy()
            pos=b["postRebalance_current_allocation"]
            nr=b["close"].shift(-1)/b["close"]-1
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            ret1=b["close"].pct_change()
            vol20=ret1.rolling(20).std()
            vol500=ret1.abs().rolling(500,min_periods=120).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":pos,"nr":nr,"mu":mu,"fee":fee,
                            "turn":(pos-b["previous_allocation"]).abs(),
                            "fc":b["forecast"],"ret1":ret1,"vol20":vol20,
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    d=pd.concat(rows).dropna(subset=["nr"])
    d["gain"]=d.pos*d.nr
    d["mkt"]=d.pos*d.mu
    d["timing"]=d.pos*(d.nr-d.mu)
    out={}
    out["decomp"]=pd.Series({"gain":d.gain.mean(),"mkt":d.mkt.mean(),"timing":d.timing.mean(),
        "fee":d.fee.mean(),"net":d.gain.mean()-d.fee.mean(),"mean_pos":d.pos.mean(),
        "mean_abs_pos":d.pos.abs().mean(),"mean_turn":d.turn.mean(),"share_long":(d.pos>0).mean(),
        "fee_per_turn":d.fee.sum()/d.turn.sum()})
    d["q"]=pd.qcut(d.fc.abs().rank(method="first"),5,labels=False)
    out["by_abs_fc_q"]=d.groupby("q").agg(gain=("gain","mean"),timing=("timing","mean"),fee=("fee","mean"),turn=("turn","mean"),abspos=("pos",lambda x:x.abs().mean()),n=("gain","size"))
    d["side"]=np.sign(d.pos)
    out["by_side"]=d.groupby("side").agg(gain=("gain","mean"),timing=("timing","mean"),mkt=("mkt","mean"),fee=("fee","mean"),n=("gain","size"))
    out["by_coin"]=d.groupby("coin").agg(gain=("gain","mean"),timing=("timing","mean"),fee=("fee","mean"),n=("gain","size"))
    out["by_year"]=d.groupby("yr").agg(gain=("gain","mean"),timing=("timing","mean"),fee=("fee","mean"),n=("gain","size"))
    out["by_weekday"]=d.groupby("wd").agg(gain=("gain","mean"),timing=("timing","mean"),fee=("fee","mean"),n=("gain","size"))
    # lag-1 autocorr of returns by vol tercile across coins
    d["vq"]=d.groupby("coin")["vol20"].transform(lambda x:pd.qcut(x.rank(method="first"),3,labels=False))
    def ac(g):
        x=g.ret1/g.vol20; y=g.nr/g.vol20
        m=x.notna()&y.notna()
        return pd.Series({"corr":np.corrcoef(x[m],y[m])[0,1],"n":m.sum(),"timing":g.timing.mean(),"fee":g.fee.mean()})
    out["by_volq"]=d.groupby("vq").apply(ac)
    # multi-day: does reversal persist? corr of ret1 with next 1 and next 2..5 days
    return out
