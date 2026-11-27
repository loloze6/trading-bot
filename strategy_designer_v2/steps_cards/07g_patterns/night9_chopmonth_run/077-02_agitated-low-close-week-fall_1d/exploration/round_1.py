def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].values
            n=len(b)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            loc=(b["close"]-b["low"])/rng  # 1 = at high
            r1=b["close"].pct_change()
            vol20=r1.rolling(20).std()
            for h in (1,3,7):
                fr=np.full(n,np.nan)
                fr[:n-h]=c[h:]/c[:n-h]-1
                b[f"f{h}"]=fr
            b["loc"]=loc; b["r1"]=r1; b["z1"]=r1/vol20
            b["rngz"]=(rng/b["close"])/( (rng/b["close"]).rolling(20).mean())
            b["agit"]=(b["regime"]!="chop").astype(int)
            b["pos"]=np.arange(n)
            b["coin"]=coin; b["win"]=w
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["tr30"]=b["close"]/b["close"].shift(30)-1
            rows.append(b[["coin","win","pos","loc","r1","z1","rngz","agit","wd","year","tr30","f1","f3","f7","forecast","postRebalance_current_allocation","high","low","close","open"]])
    d=pd.concat(rows,ignore_index=True)
    # drift per coin by horizon, non-overlapping
    drift={}
    for h in (1,3,7):
        g=d[d.pos%h==0]
        drift[h]=g.groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"]=d[f"f{h}"]-d["coin"].map(drift[h])
    d["locq"]=pd.cut(d["loc"],[-0.01,0.2,0.4,0.6,0.8,1.01],labels=["q1low","q2","q3","q4","q5high"])
    out={}
    def tab(sub,h,by):
        g=sub[sub.pos%h==0].dropna(subset=[f"u{h}"])
        r=g.groupby(by)[f"u{h}"].agg(["mean","count","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r[["mean","count","t"]]
    for h in (1,3,7):
        out[f"loc_q_u{h}_by_agit"]=tab(d,h,["agit","locq"])
    # regression slope of u7 on loc in agitated and calm
    res=[]
    for a in (0,1):
        for h in (1,3,7):
            g=d[(d.agit==a)&(d.pos%h==0)].dropna(subset=[f"u{h}","loc"])
            s=stats.linregress(g["loc"],g[f"u{h}"])
            res.append([a,h,s.slope,s.slope/s.stderr,len(g)])
    out["slope_u_on_loc"]=pd.DataFrame(res,columns=["agit","h","slope","t","n"])
    # large moves: z1 bins
    d["zq"]=pd.cut(d["z1"],[-99,-2,-1,0,1,2,99])
    for h in (1,3,7):
        out[f"z1_u{h}_by_agit"]=tab(d,h,["agit","zq"])
    d["rq"]=pd.cut(d["rngz"],[0,0.7,1,1.4,2,99])
    out["range_u7"]=tab(d,7,["agit","rq"])
    out["wd_u1"]=tab(d,1,["wd"])
    d["trq"]=pd.cut(d["tr30"],[-9,-0.2,-0.05,0.05,0.2,9])
    out["tr30_u7_agit"]=tab(d,7,["agit","trq"])
    # book by year
    bk=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["win"]=w; x["coin"]=coin; bk.append(x)
    k=pd.concat(bk)
    k["year"]=pd.to_datetime(k["day"]).dt.year
    out["book_by_win"]=k.groupby("win")[["book_return","coin_return"]].mean()
    out["share_agit"]=d["agit"].mean()
    return out
