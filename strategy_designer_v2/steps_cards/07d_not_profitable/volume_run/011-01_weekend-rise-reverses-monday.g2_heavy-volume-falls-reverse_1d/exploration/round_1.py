def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]; drows=[]
    coin_mean={}
    for c in bars:
        rs=[]
        for w,b in bars[c].items():
            rs.append(b["close"].pct_change().dropna())
        coin_mean[c]=pd.concat(rs).mean()
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy()
            cl=b["close"]; v=b["volume"]
            r=cl.pct_change()
            vr=v/v.rolling(60,min_periods=20).mean()
            vs=r/r.rolling(20,min_periods=10).std()
            for h in [1,2,3,5]:
                b[f"f{h}"]=cl.shift(-h)/cl-1-h*coin_mean[c]
            b["vr"]=vr; b["vs"]=vs; b["coin"]=c; b["w"]=w
            b["alloc"]=b["postRebalance_current_allocation"]
            b["gain"]=b["alloc"]*(cl.shift(-1)/cl-1)
            b["fee"]=b["total_portfolio_value"]-b["postRebalance_total_value"]
            b["feer"]=b["fee"]/b["total_portfolio_value"]
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            rows.append(b)
        for w,d in days[c].items():
            d=d.copy(); d["coin"]=c; d["w"]=w; drows.append(d)
    B=pd.concat(rows); D=pd.concat(drows)
    act=B[B.forecast>0]
    out={}
    out["book daily"]=pd.Series({"mean":D.book_return.mean(),"coin mean":D.coin_return.mean(),"n":D.book_return.notna().sum(),
        "share bars active":(B.forecast>0).mean(),"share bars alloc>0":(B.alloc>0.001).mean(),
        "mean alloc active":act.alloc.mean(),"mean gain per bar":B.gain.mean(),"mean fee per bar":B.feer.mean(),
        "gain active bars mean":act.gain.mean(),"n active":len(act)})
    out["active fwd excess"]=act[["f1","f2","f3","f5"]].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(x.count())])
    # down days by vr bins (all down days)
    dn=B[(B.vs<0)&B.vr.notna()].copy()
    dn["vrb"]=pd.cut(dn.vr,[0,0.7,1,1.25,1.5,2,3,100])
    out["down days by vr"]=dn.groupby("vrb")[["f1","f2","f3","f5"]].mean().join(dn.groupby("vrb").size().rename("n"))
    dn["vsb"]=pd.cut(dn.vs,[-100,-3,-2,-1.5,-1,-0.5,0])
    out["down days by fall size"]=dn.groupby("vsb")[["f1","f2","f3","f5"]].mean().join(dn.groupby("vsb").size().rename("n"))
    hv=dn[dn.vr>=1.5]
    out["heavy-vol down by fall size"]=hv.groupby("vsb")[["f1","f3"]].mean().join(hv.groupby("vsb").size().rename("n")).join(hv.groupby("vsb").forecast.apply(lambda x:(x>0).mean()).rename("share active"))
    out["active by coin"]=act.groupby("coin").agg(n=("f1","size"),f1=("f1","mean"),gain=("gain","mean"),alloc=("alloc","mean"))
    out["book by coin"]=D.groupby("coin").book_return.mean()
    return out
