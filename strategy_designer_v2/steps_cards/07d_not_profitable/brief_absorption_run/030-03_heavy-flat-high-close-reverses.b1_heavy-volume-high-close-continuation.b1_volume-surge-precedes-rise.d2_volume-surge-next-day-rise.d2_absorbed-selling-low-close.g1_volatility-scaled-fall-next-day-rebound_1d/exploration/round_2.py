def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s:int(s[1:]))
    recs=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            r=b.close.pct_change()
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["n3"]=b.close.shift(-3)/b.close-1
            b["vol20"]=r.rolling(20).std(); b["vol60"]=r.rolling(60,min_periods=20).std()
            b["vr"]=b.vol20/b.vol60
            b["r20"]=b.close/b.close.shift(20)-1
            a=b.postRebalance_current_allocation.fillna(0)
            b["a"]=a
            b["fee"]=(a-a.shift(1).fillna(b.previous_allocation.iloc[0] if "previous_allocation" in b else 0)).abs()*0.00095
            b["g"]=a*b.nxt
            b["coin"]=c; b["w"]=w; b["pos"]=np.arange(len(b))
            recs.append(b[["coin","w","pos","forecast","nxt","n3","vr","r20","a","fee","g"]])
    B=pd.concat(recs)
    B=B[B.nxt.notna()]
    edges=B.vr.quantile([.2,.4,.6,.8]).values
    B["vq"]=np.digitize(B.vr,edges); B.loc[B.vr.isna(),"vq"]=-1
    out["vr_edges"]=pd.Series(edges)
    mu=B.groupby("coin").nxt.mean(); B["ex"]=B.nxt-B.coin.map(mu)
    sig=B.forecast>0
    # gain and fee by vq among signal bars
    g=B[sig].groupby("vq").agg(n=("g","size"),gain=("g","mean"),fee=("fee","mean"),ex=("ex","mean"),sd=("ex","std"))
    g["t"]=g.ex/(g.sd/np.sqrt(g.n)); out["sig_by_vq"]=g.drop(columns="sd")
    # 3-day horizon non-overlapping on signal bars by vq
    B3=B[(B.pos%3==0)&B.n3.notna()].copy()
    mu3=B3.groupby("coin").n3.mean(); B3["ex3"]=B3.n3-B3.coin.map(mu3)
    s3=B3[B3.forecast>0].groupby("vq").agg(n=("ex3","size"),ex3=("ex3","mean"),sd=("ex3","std"))
    s3["t"]=s3.ex3/(s3.sd/np.sqrt(s3.n)); out["sig3d_by_vq"]=s3.drop(columns="sd")
    # variants: simulate book from bar gains minus fees
    def book(mask_keep, scale=None):
        x=B.copy()
        keep=mask_keep(x)
        x["net"]=np.where(keep,x.g-x.fee,0.0)
        rows=[]
        for w in wins:
            d=x[x.w==w].groupby("pos").net.mean()
            rows.append(d.values)
        s=np.concatenate(rows)
        v=np.cumprod(1+s); dd=(v/np.maximum.accumulate(v)-1).min()
        yr=v[-1]**(365/len(s))-1
        return pd.Series({"sharpe":s.mean()/s.std(ddof=1)*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"share_in":keep.mean()})
    res={}
    res["base"]=book(lambda x: np.ones(len(x),bool))
    res["drop_vq0"]=book(lambda x: ~(x.vq==0))
    res["drop_vq0_1"]=book(lambda x: ~x.vq.isin([0,1]))
    res["only_vq34"]=book(lambda x: x.vq.isin([3,4]))
    res["fc_gt10"]=book(lambda x: (x.forecast>10).values)
    res["fc_gt10_drop_vq0"]=book(lambda x: ((x.forecast>10)&(x.vq!=0)).values)
    out["variants"]=pd.DataFrame(res).T
    # deepest-fall windows w8-w9: gain by vq
    f=B[B.w.isin(["w8","w9"])&sig]
    out["fall_w8w9_by_vq"]=f.groupby("vq").agg(n=("g","size"),gain_sum=("g","sum"),a=("a","mean"))
    # condition alone (no signal) by vq: next day ex
    ns=B[~sig].groupby("vq").agg(n=("ex","size"),ex=("ex","mean"))
    out["nosig_by_vq"]=ns
    return out
