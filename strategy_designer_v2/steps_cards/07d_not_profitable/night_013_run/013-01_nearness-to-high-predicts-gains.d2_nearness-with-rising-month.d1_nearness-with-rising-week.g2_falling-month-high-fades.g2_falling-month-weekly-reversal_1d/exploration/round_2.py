def explore(data):
    import pandas as pd, numpy as np
    rows=[]
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
    d=pd.concat(rows,ignore_index=True)
    out={}
    d["side"]=np.sign(d["pos"].fillna(0)).map({1.0:"long",-1.0:"short",0.0:"flat"})
    cm=d.groupby("coin")["fwd1"].mean()
    d["mkt"]=d["pos"]*d["coin"].map(cm)
    out["gain_by_side"]=d.groupby("side").agg(n=("gain","size"),mean_gain=("gain","mean"),mkt=("mkt","mean"),fee=("fee","mean"),mean_fwd1=("fwd1","mean"),abs_pos=("pos",lambda x:x.abs().mean()))
    out["gain_by_coin"]=d.groupby("coin").agg(gain=("gain","mean"),mkt=("mkt","mean"),fee=("fee","mean"),fwd=("fwd1","mean"),pos=("pos","mean"),share_active=("pos",lambda x:(x.abs()>0).mean()))
    g=d[(d.i%7==0)].dropna(subset=["r7","f7","r30"]).copy()
    g["fall30"]=g["r30"]<0
    g["q7"]=g.groupby("fall30")["r7"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["f7_by_r7q"]=g.groupby(["fall30","q7"]).agg(n=("f7","size"),r7=("r7","mean"),f7=("f7","mean"),pos=("pos","mean")).reset_index()
    m=g[g.fall30].copy()
    m["q30"]=pd.qcut(m["r30"],3,labels=False)
    res=[]
    for q,x in m.groupby("q30"):
        res.append({"q30":q,"n":len(x),"r30":x.r30.mean(),"f7":x.f7.mean(),"corr_r7_f7":np.corrcoef(x.r7,x.f7)[0,1],"pos":x.pos.mean()})
    out["fall30_by_r30_tercile"]=pd.DataFrame(res)
    # daily book
    dd=[]
    for coin, ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    dd=pd.concat(dd,ignore_index=True)
    day=dd.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna().reset_index()
    day["wn"]=day["w"].str[1:].astype(int)
    out["by_window"]=day.groupby("wn").agg(n=("br","size"),book=("br","mean"),coin=("cr","mean"),sh=("br",lambda x:x.mean()/x.std()*np.sqrt(365)))
    day=day.sort_values(["wn","day"])
    eq=(1+day.br).cumprod(); dt=eq/eq.cummax()-1
    out["maxdd"]=float(dt.min())
    out["fee_mean"]=float(d["fee"].mean())
    out["gain_mean"]=float(d["gain"].mean())
    out["year_gain"]=d.assign(yr=d.w).groupby("regime").agg(gain=("gain","mean"),n=("gain","size"))
    return out
