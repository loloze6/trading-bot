def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]
            r=cl.pct_change()
            b["nxt"]=cl.shift(-1)/cl-1
            b["ret20"]=cl/cl.shift(20)-1
            b["dist_hi60"]=cl/cl.rolling(60,min_periods=20).max()-1
            b["ret5"]=cl/cl.shift(5)-1
            b["vol20"]=r.rolling(20).std()
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["nxt"]
            b["coin"]=c; b["w"]=w; b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["wn"]=int(w[1:])
            rows.append(b)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["mkt"]=d["pos"]*d["coin"].map(mu)
    act=d[d["forecast"]>0].dropna(subset=["nxt"])
    out={}
    # book per day
    pb=d.groupby(["wn","timestamp"])[["gain"]].mean().reset_index().sort_values(["wn","timestamp"])
    out["book_mean_gain_per_day"]=pb["gain"].mean()
    out["share_market_vs_timing"]=pd.Series({"mkt":d.groupby(["wn","timestamp"])["mkt"].mean().mean(),"total":pb["gain"].mean()})
    eq=(1+pb["gain"].fillna(0)).cumprod(); dd=eq/eq.cummax()-1
    out["maxdd"]=dd.min()
    # by window book return
    out["by_window"]=pb.groupby("wn")["gain"].agg(["mean","sum","count"]).round(4)
    # forecast bins x trend state
    act=act.copy()
    act["fbin"]=pd.qcut(act["forecast"],4,labels=False,duplicates="drop")
    act["trend"]=np.where(act["ret20"]>0,"up20","down20")
    g=act.groupby(["trend","fbin"]).agg(n=("ex","size"),ex=("ex","mean"),gain=("gain","mean"),pos=("pos","mean"))
    out["ex_by_trend_fbin"]=g.round(5)
    act["hibin"]=pd.qcut(act["dist_hi60"],5,labels=False,duplicates="drop")
    out["ex_by_dist_hi60"]=act.groupby("hibin").agg(n=("ex","size"),dist=("dist_hi60","mean"),ex=("ex","mean"),gain=("gain","mean"),t=("ex",lambda x: x.mean()/x.std()*np.sqrt(len(x)))).round(5)
    act["r5bin"]=pd.qcut(act["ret5"],5,labels=False,duplicates="drop")
    out["ex_by_ret5"]=act.groupby("r5bin").agg(n=("ex","size"),r5=("ret5","mean"),ex=("ex","mean"),gain=("gain","mean")).round(5)
    # held bars: gain by days since entry (position held while forecast 0?)
    held=d[d["pos"].abs()>1e-6].dropna(subset=["nxt"])
    out["held_by_forecast_pos"]=held.groupby(held["forecast"]>0).agg(n=("gain","size"),gain=("gain","mean"),ex=("ex","mean"),pos=("pos","mean")).round(5)
    out["by_coin"]=d.groupby("coin").agg(gain=("gain","mean"),pos=("pos","mean")).round(5)
    out["by_year"]=d.groupby("year").agg(gain=("gain","mean"),hold=("nxt","mean")).round(5)
    # fees
    tr=pd.concat([t for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"]=pd.Series({"n":len(tr),"pl":tr["profit_loss_percent"].mean(),"net":tr["net_profit_loss_percent"].mean(),"dur_days":tr["duration_minutes"].mean()/1440})
    return out
