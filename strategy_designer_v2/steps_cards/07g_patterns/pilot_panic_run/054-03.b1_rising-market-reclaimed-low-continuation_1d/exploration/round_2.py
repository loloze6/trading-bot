def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    frames = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df[["timestamp","open","high","low","close","regime"]].copy().reset_index(drop=True)
            d["coin"]=coin; d["w"]=w; d["pos"]=np.arange(len(d))
            d["low30"]=d["low"].rolling(30).min().shift(1)
            d["high30"]=d["high"].rolling(30).max().shift(1)
            d["ret1"]=d["close"].pct_change()
            d["r60"]=d["close"]/d["close"].shift(60)-1
            d["rising"]=(d["regime"]!="chop")
            d["vol30"]=d["ret1"].rolling(30).std()
            d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["year"]=pd.to_datetime(d["timestamp"]).dt.year
            for h in [3,10]:
                d[f"f{h}"]=d["close"].shift(-h)/d["close"]-1
            frames.append(d)
    A = pd.concat(frames, ignore_index=True)
    rng = (A["high"]-A["low"]).replace(0,np.nan)
    A["clv"]=(A["close"]-A["low"])/rng
    A["up_depth"]=(A["high"]-A["high30"])/A["high30"]*100
    A["dn_depth"]=(A["low30"]-A["low"])/A["low30"]*100
    A["up_depth_vol"]=A["up_depth"]/(A["vol30"]*100)
    A["dn_depth_vol"]=A["dn_depth"]/(A["vol30"]*100)
    drift={}
    for h in [3,10]:
        g=A[A["pos"]%h==0]; drift[h]=g.groupby("coin")[f"f{h}"].mean()
    def cases(mask,h):
        sub=A[mask & A[f"f{h}"].notna()].copy()
        sub["cell"]=sub["pos"]//h
        sub=sub.groupby(["coin","w","cell"]).head(1)
        sub["u"]=sub[f"f{h}"]-sub["coin"].map(drift[h])
        return sub
    def tday(sub):
        per=sub.groupby("day")["u"].sum(); G=len(per); n=len(sub)
        if G<2: return np.nan
        se=np.sqrt((per**2).sum()*G/(G-1))/n
        return sub["u"].mean()/se
    out={}
    phf=(A["high"]>A["high30"])&(A["close"]<=A["high30"])
    pr=(A["low"]<A["low30"])&(A["close"]>=A["low30"])
    rows=[]
    for name,m,dep in [("phf_rising",phf&A["rising"],"up_depth_vol"),("phf_all",phf,"up_depth_vol"),
                       ("pr_rising",pr&A["rising"],"dn_depth_vol"),("pr_all",pr,"dn_depth_vol")]:
        for h in [3,10]:
            s=cases(m,h)
            sl=stats.linregress(s[dep],s["u"]) if len(s)>5 else None
            rows.append(dict(ev=name,h=h,n=len(s),days=s["day"].nunique(),mean=s["u"].mean(),t=tday(s),
                             slope_depth=sl.slope if sl else np.nan, slope_p=sl.pvalue if sl else np.nan,
                             share_pos=(s["u"]>0).mean()))
    out["grading"]=pd.DataFrame(rows)
    # by window and year for phf rising 10
    s=cases(phf&A["rising"],10)
    out["phf_rising_by_w"]=s.groupby("w")["u"].agg(["count","mean"])
    out["phf_rising_by_coin"]=s.groupby("coin")["u"].agg(["count","mean"])
    # phf rising by clv tercile
    s["clvq"]=pd.qcut(s["clv"],3,labels=False,duplicates="drop")
    out["phf_rising_by_clv"]=s.groupby("clvq")["u"].agg(["count","mean"])
    # baseline: rising grid days 10 unusual and rising days with close within 5% of high30 (not piercing)
    near=A["rising"]&(~phf)&(A["high"]<=A["high30"])&(A["close"]>A["high30"]*0.95)
    s2=cases(near,10); s3=cases(A["rising"]&~phf&~(A["close"]>A["high30"]),10)
    out["baselines"]=pd.DataFrame([dict(g="rising_near_high_nopierce",n=len(s2),mean=s2["u"].mean(),t=tday(s2)),
                                   dict(g="rising_other",n=len(s3),mean=s3["u"].mean(),t=tday(s3))])
    # pierce reclaim rising by window, coin
    s4=cases(pr&A["rising"],10)
    out["pr_rising_by_coin"]=s4.groupby("coin")["u"].agg(["count","mean"])
    out["pr_rising_by_w"]=s4.groupby("w")["u"].agg(["count","mean"])
    return out
