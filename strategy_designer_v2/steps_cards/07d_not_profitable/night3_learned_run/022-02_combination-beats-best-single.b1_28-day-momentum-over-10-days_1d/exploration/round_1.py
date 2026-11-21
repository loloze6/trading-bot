def explore(data):
    import numpy as np, pandas as pd
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    windows = sorted(days[coins[0]].keys(), key=lambda w:int(w[1:]))
    out = {}
    # book daily returns
    chain = []
    for w in windows:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna().reset_index()
        g["w"]=w; chain.append(g)
    ch = pd.concat(chain, ignore_index=True)
    v = (1+ch["book"]).cumprod(); peak=v.cummax(); dd=v/peak-1
    ch["dd"]=dd
    # drawdown episodes
    eps=[]; i=0; n=len(ch)
    inep=False
    for k in range(n):
        if dd.iloc[k]<0 and not inep: inep=True; start=k-1 if k>0 else k
        if inep and dd.iloc[k]==0:
            seg=dd.iloc[start:k]; eps.append((start, seg.idxmin(), k, seg.min())); inep=False
    if inep: seg=dd.iloc[start:]; eps.append((start, seg.idxmin(), n, seg.min()))
    eps=sorted(eps,key=lambda e:e[3])[:6]
    rows=[]
    for s,t,e,m in eps:
        seg=ch.iloc[s+1:t+1]
        rows.append({"depth":m,"days_to_trough":t-s,"days_to_recover":e-t,"windows":",".join(sorted(set(seg.w),key=lambda x:int(x[1:]))),
                     "book_sum":seg.book.sum(),"hold_sum":seg.hold.sum()})
    out["deepest_falls"]=pd.DataFrame(rows)
    yrs = len(ch)/365; out["calmar_parts"]=pd.Series({"yearly":v.iloc[-1]**(1/yrs)-1,"maxdd":dd.min(),"days":len(ch)})
    # bar-level pnl
    recs=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            r=b.close.pct_change().shift(-1)
            a=b.postRebalance_current_allocation
            ret28=b.close/b.close.shift(28)-1
            ret5=b.close/b.close.shift(5)-1
            vol=b.close.pct_change().rolling(20).std()
            volrel=vol/b.close.pct_change().rolling(120,min_periods=60).std()
            dd60=b.close/b.close.rolling(60,min_periods=20).max()-1
            recs.append(pd.DataFrame({"coin":c,"w":w,"pnl":a*r,"a":a,"f":b.forecast,"ret28":ret28,
                "rev5":np.sign(b.forecast)*ret5,"vol":vol,"volrel":volrel,"dd60":dd60,"r":r,"year":pd.to_datetime(b.timestamp).dt.year}))
    R=pd.concat(recs).dropna(subset=["pnl"])
    def grp(col,q=5):
        x=R.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("q").agg(lo=(col,"min"),hi=(col,"max"),pnl_bps=("pnl",lambda s:s.mean()*1e4),
            t=("pnl",lambda s:s.mean()/s.std()*np.sqrt(len(s))),absA=("a",lambda s:s.abs().mean()),n=("pnl","size"))
    out["by_side"]=R.assign(side=np.sign(R.a)).groupby("side").agg(pnl_bps=("pnl",lambda s:s.mean()*1e4),sd=("pnl","std"),n=("pnl","size"),share_days=("pnl","size"))
    out["by_absf"]=R.assign(af=R.f.abs()).pipe(lambda x:x).groupby(pd.qcut(R.f.abs(),5,duplicates="drop")).agg(pnl_bps=("pnl",lambda s:s.mean()*1e4),sd_bps=("pnl",lambda s:s.std()*1e4),n=("pnl","size"))
    out["by_rev5_in_dir"]=grp("rev5")
    out["by_volrel"]=grp("volrel")
    out["by_dd60"]=grp("dd60")
    out["by_year"]=R.groupby("year").agg(pnl_bps=("pnl",lambda s:s.mean()*1e4),n=("pnl","size"),long_share=("a",lambda s:(s>0).mean()))
    out["by_coin"]=R.groupby("coin").agg(pnl_bps=("pnl",lambda s:s.mean()*1e4),sd_bps=("pnl",lambda s:s.std()*1e4),absA=("a",lambda s:s.abs().mean()))
    return out
