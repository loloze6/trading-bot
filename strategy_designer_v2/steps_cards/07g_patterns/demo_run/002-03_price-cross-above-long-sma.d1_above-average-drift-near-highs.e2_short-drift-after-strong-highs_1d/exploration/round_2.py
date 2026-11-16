def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    for h in [5,10]:
        rows=[]
        for c,ws in data["bars"].items():
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                cl=pd.Series(b["close"].values)
                n=len(cl)
                hi20=cl.rolling(20).max(); lo20=cl.rolling(20).min()
                pos=(cl-lo20)/(hi20-lo20)
                r20=cl/cl.shift(20)-1
                ma200=cl.rolling(200,min_periods=1).mean()
                ts=pd.to_datetime(b["timestamp"])
                for i in range(0,n-h,h):
                    rows.append(dict(coin=c,win=w,fwd=cl[i+h]/cl[i]-1,reg=b["regime"].iloc[i],
                        pos=pos.iloc[i],r20=r20.iloc[i],yr=ts.iloc[i].year,fc=b["forecast"].iloc[i]))
        g=pd.DataFrame(rows)
        g["dm"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
        t=g[(g.reg=="trending")].dropna(subset=["pos","r20"])
        lo=t[t.pos<0.5]
        lr=stats.linregress(lo["pos"],lo["dm"])
        out[f"h{h}_trend_lowerhalf_slope_pos"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(lo)}"
        lr=stats.linregress(t["pos"],t["dm"])
        out[f"h{h}_trend_all_slope_pos"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(t)}"
        hi=t[t.pos>=0.5]
        lr=stats.linregress(hi["pos"],hi["dm"])
        out[f"h{h}_trend_upperhalf_slope_pos"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(hi)}"
        lo=t[t.r20<0]
        lr=stats.linregress(lo["r20"],lo["dm"])
        out[f"h{h}_trend_negr20_slope"]=f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(lo)}"
        if h==5:
            t=t.copy()
            t["pb"]=pd.cut(t["pos"],[-0.01,0.1,0.25,0.5,0.75,0.9,1.01])
            a=t.groupby("pb")["dm"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
            out["h5_trend_pos_bins"]=a
            q=t[t.pos<0.25]
            a=q.groupby("coin")["dm"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
            out["h5_lowpos_by_coin"]=a
            a=q.groupby("yr")["dm"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
            out["h5_lowpos_by_year"]=a
    # book largest days
    d=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy().reset_index(drop=True); x["coin"]=c
            x["prev_coin"]=x["coin_return"].shift(1); x["next_coin"]=x["coin_return"].shift(-1)
            d.append(x)
    d=pd.concat(d).dropna(subset=["book_return"])
    q1,q9=d["book_return"].quantile([0.01,0.99])
    out["book_tails"]=pd.DataFrame({"worst1pct":d[d.book_return<=q1][["book_return","coin_return","prev_coin","next_coin"]].mean(),
                                    "best1pct":d[d.book_return>=q9][["book_return","coin_return","prev_coin","next_coin"]].mean()})
    return out
