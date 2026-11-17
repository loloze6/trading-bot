def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            b["ret"]=r; b["nxt"]=c.shift(-1)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["sd20"]=r.rolling(20).std()
            b["volratio"]=b["sd20"]/(r.abs().rolling(120,min_periods=60).mean())
            b["ret20"]=c/c.shift(20)-1
            b["coin"]=coin; b["w"]=w
            # drawdown of book within window
            v=b["postRebalance_total_value"]; b["dd"]=v/v.cummax()-1
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    cm=B.groupby("coin")["ret"].mean(); B["cm"]=B["coin"].map(cm)
    B["timing"]=B["pos"]*(B["nxt"]-B["cm"]); B["gross"]=B["pos"]*B["nxt"]; B["net"]=B["gross"]-B["fee"]
    def t(x):
        x=x.dropna(); return x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan
    out={}
    B["vd"]=pd.qcut(B["volratio"],6,labels=False)
    out["by_volratio_sextile"]=B.groupby("vd").agg(n=("net","size"),vr=("volratio","mean"),gross=("gross","mean"),fee=("fee","mean"),net=("net","mean"),t_net=("net",t),abspos=("pos",lambda x:x.abs().mean()))
    B["side"]=np.sign(B["pos"])
    out["side_x_vol3"]=B[B["pos"]!=0].groupby([pd.qcut(B["volratio"],3,labels=False),"side"]).agg(n=("net","size"),gross=("gross","mean"),timing=("timing","mean"),net=("net","mean"),t=("timing",t))
    B["tr"]=np.sign(B["ret20"])
    out["side_x_trend20"]=B[B["pos"]!=0].groupby(["tr","side"]).agg(n=("net","size"),gross=("gross","mean"),net=("net","mean"),t=("net",t))
    # bars inside deep drawdowns: worst 10% net-loss bars context
    q=B["net"].quantile(0.05)
    W=B[B["net"]<=q]
    out["worst5pct_bars"]=pd.Series({"n":len(W),"mean_net":W["net"].mean(),"share_short":(W["pos"]<0).mean(),"mean_volratio":W["volratio"].mean(),"all_volratio":B["volratio"].mean(),"share_against_trend20":(np.sign(W["pos"])!=np.sign(W["ret20"])).mean(),"mean_abs_nxt":W["nxt"].abs().mean()})
    # net by window, high-vol sextiles only vs rest
    B["hv"]=B["vd"]>=4
    out["net_by_window_hv"]=B.groupby(["w","hv"])["net"].mean().unstack()
    return out
