def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["coin"] = c; dd["window"] = w
            rows.append(dd[["coin","window","day","book_return","coin_return"]])
    D = pd.concat(rows)
    wnum = lambda w: int(w[1:])
    B = D.groupby(["window","day"])[["book_return","coin_return"]].mean().reset_index()
    B["wn"] = B["window"].map(wnum)
    B = B.sort_values(["wn","day"]).dropna(subset=["book_return"])
    v = (1+B["book_return"]).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    yrs = len(B)/365
    out["chain"] = pd.Series({"yearly": v.iloc[-1]**(1/yrs)-1, "maxdd": dd.min(), "days": len(B)})
    # drawdown by window: book and holding sum
    g = B.groupby("window")
    def wdd(x):
        vv=(1+x).cumprod(); return (vv/vv.cummax()-1).min()
    out["by_window"] = pd.DataFrame({"book_sum": g["book_return"].sum(), "coin_sum": g["coin_return"].sum(),
                                     "book_dd": g["book_return"].apply(wdd), "coin_dd": g["coin_return"].apply(wdd)}).loc[sorted(B.window.unique(), key=wnum)]
    # bar-level analysis
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]; r1 = cl.shift(-1)/cl-1
            ret = cl.pct_change()
            sd30 = ret.rolling(30).std()
            fallz = -ret/sd30
            cloc = (b["high"]-cl)/(b["high"]-b["low"])
            tr60 = cl/cl.shift(60)-1
            r3 = cl.pct_change(3)
            pos = b["postRebalance_current_allocation"]
            recs.append(pd.DataFrame({"coin":c,"window":w,"r1":r1,"ret":ret,"fallz":fallz,"cloc":cloc,
                       "tr60":tr60,"r3prev":r3,"pos":pos,"fc":b["forecast"],"regime":b["regime"],
                       "gain":pos*r1,"sd30":sd30}))
    X = pd.concat(recs).dropna(subset=["r1"])
    mu = X.groupby("coin")["r1"].mean()
    X["ex"] = X["r1"]-X["coin"].map(mu)
    held = X[X.pos>0]
    out["held_share_and_gain"] = pd.Series({"held_bars":len(held),"mean_gain":held.gain.mean(),
        "mean_pos":held.pos.mean(),"share_fc0_but_held":(held.fc<=0).mean()})
    # gain by trend profile
    held = held.assign(trend=pd.cut(held.tr60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"]))
    out["held_by_trend"] = held.groupby("trend").agg(n=("gain","size"),gain=("gain","mean"),r1=("r1","mean"),ex=("ex","mean"),
        sd=("r1","std"),worst=("gain","min"))
    # by forecast strength quartile
    held["fq"] = pd.qcut(held.fc.rank(method="first"),4,labels=False)
    out["held_by_fc_q"] = held.groupby("fq").agg(n=("gain","size"),fc=("fc","mean"),pos=("pos","mean"),gain=("gain","mean"),r1=("r1","mean"),sdr=("r1","std"))
    # by previous 3-day return (falls in a row)
    held["p3"] = pd.qcut(held.r3prev,4,labels=False)
    out["held_by_prev3"] = held.groupby("p3").agg(n=("gain","size"),r3=("r3prev","mean"),gain=("gain","mean"),r1=("r1","mean"))
    # worst 20 drawdown days: mean conditions
    worst = B.nsmallest(30,"book_return")
    out["worst30_days"] = pd.Series({"mean_book":worst.book_return.mean(),"mean_coin":worst.coin_return.mean()})
    # deepest fall episode: locate
    i_tr = int(np.argmin(dd.values)); peak = int(np.argmax(v.values[:i_tr+1]))
    ep = B.iloc[peak:i_tr+1]
    out["deepest_episode"] = pd.Series({"window_start":ep.window.iloc[0],"window_end":ep.window.iloc[-1],"days":len(ep),
        "book_sum":ep.book_return.sum(),"coin_sum":ep.coin_return.sum()})
    return out
