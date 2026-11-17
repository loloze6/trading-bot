def explore(data):
    import pandas as pd, numpy as np
    rows=[]; trades=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]
            b["fwd1"]=c.shift(-1)/c-1
            b["r7"]=c/c.shift(7)-1
            b["r30"]=c/c.shift(30)-1
            b["f7"]=c.shift(-7)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["fwd1"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=coin; b["w"]=w; b["i"]=np.arange(len(b))
            rows.append(b[["coin","w","i","regime","forecast","pos","fwd1","gain","fee","r7","r30","f7"]])
        for w,t in data["trades"][coin].items():
            t=t.copy(); t["coin"]=coin; trades.append(t)
    d=pd.concat(rows); t=pd.concat(trades)
    out={}
    d["side"]=np.sign(d["pos"]).map({1:"long",-1:"short",0:"flat"})
    out["gain_by_side"]=d.groupby("side").agg(n=("gain","size"),mean_gain=("gain","mean"),fee=("fee","mean"),mean_fwd1=("fwd1","mean"),mean_abs_pos=("pos",lambda x:x.abs().mean()))
    out["gain_by_coin"]=d.groupby("coin").agg(gain=("gain","mean"),fee=("fee","mean"),fwd=("fwd1","mean"),pos=("pos","mean"))
    mr=d[d.regime=="mean_reversion"].dropna(subset=["r7","f7"])
    g=mr[mr.i%7==0].copy()
    g["q7"]=pd.qcut(g["r7"],5,labels=False)
    out["f7_by_r7_quintile"]=g.groupby("q7").agg(n=("f7","size"),r7=("r7","mean"),f7=("f7","mean"),pos=("pos","mean"))
    g["q30"]=pd.qcut(g["r30"],3,labels=False)
    out["f7_by_r30_tercile"]=g.groupby("q30").agg(n=("f7","size"),r30=("r30","mean"),f7=("f7","mean"),corr_r7_f7=("f7",lambda x: np.corrcoef(x,g.loc[x.index,"r7"])[0,1] if len(x)>3 else np.nan))
    allg=d[d.i%7==0].dropna(subset=["r7","f7"]).copy()
    allg["up30"]=allg["r30"]>0
    allg["q7"]=allg.groupby("up30")["r7"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["f7_by_r7_all_regimes"]=allg.groupby(["up30","q7"]).agg(n=("f7","size"),r7=("r7","mean"),f7=("f7","mean")).reset_index()
    out["trades"]=t.groupby("side").agg(n=("side","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_days=("duration_minutes",lambda x:x.mean()/1440))
    out["fee_total_mean_daily"]=d["fee"].mean()
    out["gain_by_year_window"]=d.groupby("w").agg(gain=("gain","mean"),fwd=("fwd1","mean"))
    return out
