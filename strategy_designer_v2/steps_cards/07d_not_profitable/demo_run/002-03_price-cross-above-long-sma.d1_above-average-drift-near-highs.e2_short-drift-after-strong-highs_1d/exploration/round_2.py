def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            wn = int(w[1:])
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            b["gain"] = a*b["ret1"]
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["r60"] = b["close"]/b["close"].shift(60)-1
            b["c5"] = b["close"].shift(-5)/b["close"]-1
            on = (b["forecast"]>0).astype(int)
            grp = (on.diff()!=0).cumsum()
            b["days_on"] = on.groupby(grp).cumsum()
            b["bir"] = pd.to_numeric(b["debug_info.bars_in_regime"], errors="coerce")
            b["pos"] = np.arange(len(b))
            b["coin"]=c; b["wn"]=wn
            b["dd_win"] = (wn>=4)&(wn<=10)
            br.append(b[["coin","wn","pos","forecast","postRebalance_current_allocation","ret1","gain","r5","r20","r60","c5","days_on","bir","dd_win"]])
    B = pd.concat(br)
    act = B[B["forecast"]>0].copy()
    out["dd_vs_rest_active"] = act.groupby("dd_win").agg(gain=("gain","mean"), ret1=("ret1","mean"), alloc=("postRebalance_current_allocation","mean"), f=("forecast","mean"), n=("gain","count"))
    act["fq"] = pd.qcut(act["forecast"],3,labels=False)
    out["dd_by_fq"] = act.groupby(["dd_win","fq"]).agg(gain=("gain","mean"), ret1=("ret1","mean"), n=("gain","count"))
    # days since forecast on
    act["don"] = pd.cut(act["days_on"],[0,2,5,10,20,1000])
    out["by_days_on"] = act.groupby("don").agg(gain=("gain","mean"), ret1=("ret1","mean"), alloc=("postRebalance_current_allocation","mean"), n=("gain","count"))
    # bars in regime (time above 200d)
    a2 = act.dropna(subset=["bir"]).copy()
    if len(a2)>50:
        a2["bq"] = pd.qcut(a2["bir"],5,labels=False,duplicates="drop")
        out["by_bars_in_regime"] = a2.groupby("bq").agg(bir=("bir","mean"), gain=("gain","mean"), ret1=("ret1","mean"), n=("gain","count"))
    # r60 quintiles (where available)
    a3 = act.dropna(subset=["r60"]).copy()
    a3["q"] = pd.qcut(a3["r60"],5,labels=False)
    out["by_r60_q"] = a3.groupby("q").agg(r60=("r60","mean"), gain=("gain","mean"), ret1=("ret1","mean"), n=("gain","count"))
    # r5 quintiles
    a4 = act.dropna(subset=["r5"]).copy()
    a4["q"] = pd.qcut(a4["r5"],5,labels=False)
    out["by_r5_q"] = a4.groupby("q").agg(r5=("r5","mean"), gain=("gain","mean"), ret1=("ret1","mean"), n=("gain","count"))
    # grid 5-day: c5 by forecast tercile x r20 tercile, non-overlap
    g = act[(act["pos"]%5==0)].dropna(subset=["c5","r20"]).copy()
    g["rq"] = pd.qcut(g["r20"],3,labels=False)
    out["grid_c5_fq_rq"] = g.groupby(["fq","rq"])["c5"].agg(["mean","count"])
    # worst book days: state
    act["loss_day"] = act["gain"] < act["gain"].quantile(0.05)
    out["worst5pct_state"] = act.groupby("loss_day")[["forecast","r5","r20","days_on","postRebalance_current_allocation"]].mean()
    return out
