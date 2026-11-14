def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins=list(data["bars"].keys())
    wins = sorted(data["days"]["BTCUSD"].keys(), key=lambda w:int(w[1:]))
    rows=[]
    for c in coins:
        for w in wins:
            b=data["bars"][c][w].copy()
            cl=b.close; r1=cl.pct_change(); nxt=cl.shift(-1)/cl-1
            a=b.postRebalance_current_allocation.astype(float)
            mad=r1.abs().rolling(60,min_periods=20).mean()
            vol20=r1.rolling(20).std(); vol60=r1.rolling(60).std()
            r60=cl/cl.shift(60)-1; r20=cl/cl.shift(20)-1
            r1n=r1.shift(-1)
            rows.append(pd.DataFrame({"c":c,"w":w,"a":a,"nxt":nxt,"z":r1/mad,"vr":vol20/vol60,
               "r20":r20,"r60":r60,"vol20":vol20,"pnl":a*nxt,"prevz":(r1/mad).shift(1),
               "day":pd.to_datetime(b.timestamp).dt.floor("D")}))
    D=pd.concat(rows,ignore_index=True).dropna(subset=["nxt"])
    H=D[D.a>0].copy()
    # book daily
    bk=[]
    for w in wins:
        cols=[data["days"][c][w].set_index("day")["book_return"].rename(c) for c in coins]
        df=pd.concat(cols,axis=1)
        s=df.mean(axis=1).dropna()
        bk.append(pd.DataFrame({"w":w,"r":s.values,"nheld":(df.loc[s.index]!=0).sum(axis=1).values}))
    B=pd.concat(bk,ignore_index=True)
    eq=(1+B.r).cumprod(); B["dd"]=(eq/eq.cummax()-1).values
    # loss contribution: worst 5% book days share of total loss
    neg=B[B.r<0]; q=B.r.quantile(0.02)
    out["book_worst2pct"]=pd.Series({"n":int((B.r<=q).sum()),"sum_worst":B.r[B.r<=q].sum(),"sum_all":B.r.sum(),
        "mean_nheld_worst":B.nheld[B.r<=q].mean(),"mean_nheld_negdays":neg.nheld.mean()}).round(4)
    # held bars: excess vs coin mean
    cm=D.groupby("c").nxt.mean()
    H["ex"]=H.nxt-H.c.map(cm)
    H["big"]=H.a>=1.0
    def tab(g):
        r=H.groupby(g,observed=True).agg(n=("pnl","size"),ex=("ex","mean"),pnl=("pnl","mean"),
            pnl_sd=("pnl","std"),loss_sum=("pnl",lambda s:s[s<0].sum()))
        r["t_ex"]=H.groupby(g,observed=True).ex.apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))
        return r.round(5)
    H["vrb"]=pd.cut(H.vr,[0,0.9,1.1,1.3,9]); H["r60b"]=pd.cut(H.r60,[-1,0,0.3,0.7,1,50])
    H["vol20b"]=pd.qcut(H.vol20,4); H["yr"]=pd.to_datetime(H.day).dt.year
    out["by_big_alloc"]=tab("big")
    out["by_vr"]=tab("vrb"); out["by_r60"]=tab("r60b"); out["by_vol20"]=tab("vol20b")
    out["by_year"]=tab("yr")
    Hb=H[H.big]
    out["big_by_vr"]=Hb.groupby("vrb",observed=True).agg(n=("pnl","size"),pnl=("pnl","mean"),ex=("ex","mean"),sd=("pnl","std")).round(5)
    out["big_by_r60"]=Hb.groupby("r60b",observed=True).agg(n=("pnl","size"),pnl=("pnl","mean"),ex=("ex","mean"),sd=("pnl","std")).round(5)
    # drawdown period w11-w17 vs rest
    H["ddzone"]=H.w.isin(["w11","w12","w13","w14","w15","w16","w17","w20","w21","w22","w23"])
    out["by_ddzone"]=tab("ddzone")
    # held after prior big down day (2 dips in row)
    H["prev_dn"]=pd.cut(H.prevz,[-99,-1,0,99])
    out["by_prevz"]=tab("prev_dn")
    # co-holding: days where many coins held at once
    dayheld=H.groupby("day").agg(k=("c","size"),pnl=("pnl","sum"))
    out["by_simult"]=dayheld.groupby(pd.cut(dayheld.k,[0,1,2,3,6]),observed=True).agg(n=("pnl","size"),mean=("pnl","mean"),sd=("pnl","std"),worst=("pnl","min")).round(4)
    return out
