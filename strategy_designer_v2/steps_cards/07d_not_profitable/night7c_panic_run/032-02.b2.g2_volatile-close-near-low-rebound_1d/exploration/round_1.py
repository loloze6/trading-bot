def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            nxt = c.shift(-1)/c - 1
            rng = (h-l)
            loc = ((h-c)/rng).where(rng>0)
            r30 = c/c.shift(30)-1
            r5 = c/c.shift(5)-1
            r1 = c/c.shift(1)-1
            br = (rng/c)
            rr = br.rolling(30).mean()/br.rolling(90).mean()
            alloc = b["postRebalance_current_allocation"].fillna(0)
            df = pd.DataFrame({"coin":coin,"w":w,"nxt":nxt,"loc":loc,"r30":r30,"r5":r5,"r1":r1,
                               "rr":rr,"alloc":alloc,"fc":b["forecast"],"reg":b["regime"],
                               "gain":alloc*nxt,"brange":br})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["ex"] = D["nxt"] - D["coin"].map(drift)
    R = D[D.reg=="mean_reversion"].dropna(subset=["nxt","loc"])
    out = {}
    # book daily, per window drawdown
    bk = []
    for coin, wd in days.items():
        for w, d in wd.items():
            bk.append(pd.DataFrame({"w":w,"day":d["day"].values,"br":d["book_return"].values,"cr":d["coin_return"].values}))
    B = pd.concat(bk).groupby(["w","day"]).mean().reset_index().dropna()
    B["wn"] = B.w.str[1:].astype(int)
    B = B.sort_values(["wn","day"])
    v = (1+B.br).cumprod(); dd = v/v.cummax()-1
    B["dd"]=dd.values
    vc=(1+B.cr).cumprod(); B["cdd"]=(vc/vc.cummax()-1).values
    out["by_window"] = B.groupby("w").agg(book_sum=("br","sum"),coin_sum=("cr","sum"),min_dd=("dd","min"),n=("br","size"),coin_min_dd=("cdd","min"))
    # window stats of the regime bars
    # gain by trend state
    def summ(g):
        return pd.Series({"n":len(g),"mean_gain":g.gain.mean(),"mean_ex":g.ex.mean(),"t_ex":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,"mean_alloc":g.alloc.mean()})
    R["r30q"]=pd.qcut(R.r30,4,labels=["q1low","q2","q3","q4high"])
    R["locq"]=pd.qcut(R["loc"],3,labels=["nearhigh","mid","nearlow"])
    out["r30q_x_loc"] = R.groupby(["r30q","locq"]).apply(summ)
    R["r1q"]=pd.qcut(R.r1,4,labels=["q1low","q2","q3","q4high"])
    out["r1q_x_loc"] = R.groupby(["r1q","locq"]).apply(summ)
    R["rrq"]=pd.qcut(R.rr,3,labels=["mildwide","wide","verywide"])
    out["rrq_x_loc"] = R.groupby(["rrq","locq"]).apply(summ)
    # gain on all held bars by r30 sign
    H = D[D.alloc>0].dropna(subset=["nxt"])
    H["r30s"]=np.where(H.r30<0,"r30neg","r30pos")
    out["held_by_r30sign_coin"] = H.groupby(["coin","r30s"]).apply(summ)
    out["held_by_year"]=H.assign(y=0).groupby("w").apply(summ)
    return out
