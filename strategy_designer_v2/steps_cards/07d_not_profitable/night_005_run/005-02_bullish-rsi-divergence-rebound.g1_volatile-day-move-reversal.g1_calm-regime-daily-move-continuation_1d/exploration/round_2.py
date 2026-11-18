def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy().reset_index(drop=True)
            b["coin"]=c; b["w"]=w
            b["pos"]=b["postRebalance_current_allocation"]
            b["ret1"]=b["close"].shift(-1)/b["close"]-1
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            for k in range(1,8):
                b[f"r_d{k}"]=b["close"].shift(-k)/b["close"].shift(-(k-1))-1
                b[f"pos_d{k}"]=b["pos"].shift(-(k-1))
            b["r5"]=b["close"].shift(-5)/b["close"]-1
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    mu=B.groupby("coin")["ret1"].mean()
    B["thr"]=B.groupby("coin")["forecast"].transform(lambda x: x.abs().quantile(0.8))
    top=B[B["forecast"].abs()>=B["thr"]].copy()
    s=np.sign(top["forecast"])
    res={}
    for k in range(1,8):
        x=s*(top[f"r_d{k}"]-top["coin"].map(mu))
        p=np.sign(top[f"pos_d{k}"])==s
        res[f"d{k}"]={"signed_excess":x.mean(),"t":x.mean()/(x.std()/np.sqrt(x.count())),"share_pos_same_side":p.mean(),"mean_signed_pos":(s*top[f"pos_d{k}"]).mean()}
    out["decay_after_top"]=pd.DataFrame(res).T
    out["n_top"]=len(top)
    # by side in top
    top["side"]=s
    out["top_by_side"]=top.groupby("side").apply(lambda g: pd.Series({"n":len(g),"d1":(np.sign(g["forecast"])*g["r_d1"]).mean(),"sum5":(np.sign(g["forecast"])*g["r5"]).mean()}))
    # days: daily book stats
    D=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            d=d.copy(); d["coin"]=c; d["w"]=w; D.append(d)
    D=pd.concat(D,ignore_index=True)
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series({"mean":bk["book_return"].mean(),"sharpe":bk["book_return"].mean()/bk["book_return"].std()*np.sqrt(365),"hold_sharpe":bk["coin_return"].mean()/bk["coin_return"].std()*np.sqrt(365)})
    out["book_by_window"]=bk.groupby("w")["book_return"].agg(["mean","count"]).assign(hold=bk.groupby("w")["coin_return"].mean())
    # gain vs fee per quintile, position change in top
    B["dpos"]=(B["pos"]-B["previous_allocation"]).abs()
    B["q"]=(B["forecast"].abs()>=B["thr"]).map({True:"top",False:"rest"})
    out["gain_fee_turnover"]=B.groupby("q").agg(gain=("pos",lambda x:(x*B.loc[x.index,"ret1"]).mean()),fee=("fee","mean"),dpos=("dpos","mean"))
    return out
