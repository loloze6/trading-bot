def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cmean = {}
    for c, ws in data["bars"].items():
        rr = [ (b["close"].shift(-1)/b["close"]-1).dropna() for w,b in ws.items()]
        cmean[c] = pd.concat(rr).mean()
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            nxt = cl.shift(-1)/cl - 1
            tr60 = cl/cl.shift(60) - 1
            tr30 = cl/cl.shift(30) - 1
            vr = sd / r.rolling(90, min_periods=60).std()
            rows.append(pd.DataFrame({"coin": c, "w": w, "wi": int(w[1:]), "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"), "z": z, "nxt": nxt,
                "ex": nxt - cmean[c], "tr60": tr60, "tr30": tr30, "vr": vr,
                "alloc": b["postRebalance_current_allocation"].fillna(0)}))
    d = pd.concat(rows, ignore_index=True)
    d["nxt"] = d["nxt"].fillna(0)
    cost = 0.0019/2
    def book(pos):
        x = d[["coin","w","wi","pos","day","nxt"]].copy(); x["p"] = pos.fillna(0).values
        x["chg"] = x.groupby(["coin","w"])["p"].diff().abs().fillna(x["p"].abs())
        x["g"] = x["p"]*x["nxt"] - x["chg"]*cost
        B = x.groupby(["wi","day"])["g"].mean().sort_index()
        v = (1+B).cumprod().values; dd = (v/np.maximum.accumulate(v)-1).min()
        yr = v[-1]**(365/len(v)) - 1
        inpos = (x["p"].abs()>0.01).mean()
        return pd.Series({"sharpe": B.mean()/B.std()*np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr/abs(dd), "mean_day": B.mean(), "inpos": inpos,
                          "turn": x["chg"].mean()})
    a = d["alloc"]
    res = {"actual_alloc_withcost": book(a)}
    for thr in [-0.5, -1.0, -1.5]:
        res[f"alloc_only_z<{thr}"] = book(a.where(d["z"] < thr, 0))
    res["alloc_not_falling60"] = book(a.where(~(d["tr60"] < -0.1), 0))
    res["alloc_z<-1_not_falling60"] = book(a.where((d["z"] < -1) & ~(d["tr60"] < -0.1), 0))
    res["alloc_not_falling30"] = book(a.where(~(d["tr30"] < -0.1), 0))
    res["alloc_z<-1_not_falling30"] = book(a.where((d["z"] < -1) & ~(d["tr30"] < -0.1), 0))
    out["variants"] = pd.DataFrame(res).T
    # condition check: falling-trend effect alone vs with signal (60-day)
    d["tb"] = pd.cut(d["tr60"], [-9,-0.1,0.1,9], labels=["falling","choppy","rising"])
    d["zc"] = pd.cut(d["z"], [-99,-1.5,-1,-0.5,0,99], labels=["<-1.5","-1.5..-1","-1..-0.5","-0.5..0","up"])
    g = d.dropna(subset=["tb","z"]).groupby(["tb","zc"], observed=True)["ex"]
    out["ex_trend60_x_z"] = g.agg(["size","mean"]).unstack(0)
    # w9 drawdown: what was held
    x = d.copy(); x["g"] = x["alloc"]*x["nxt"]
    B = x.groupby(["wi","day"])["g"].mean().sort_index()
    v = (1+B).cumprod(); dd = v/v.cummax()-1
    w9 = dd.loc[9]; trough = w9.idxmin(); peak = v.loc[9].loc[:trough].idxmax()
    seg = x[(x["wi"]==9)&(x["day"]>peak)&(x["day"]<=trough)]
    seg["zc2"] = seg["zc"].astype(str)
    out["w9_dd_by_z"] = seg.groupby("zc2").agg(n=("g","size"), alloc=("alloc","mean"), g_sum=("g","sum"))
    out["w9_dd_tr30_mean"] = float(seg["tr30"].mean())
    out["w9_dd_days"] = int(seg["day"].nunique())
    # deepest falls in every window: trend and held z
    allseg = []
    for wi in B.index.get_level_values(0).unique():
        vv = v.loc[wi]; ddw = vv/vv.cummax()-1; tro = ddw.idxmin(); pk = vv.loc[:tro].idxmax()
        s = x[(x["wi"]==wi)&(x["day"]>pk)&(x["day"]<=tro)&(x["alloc"]>0.01)]
        allseg.append(s)
    S = pd.concat(allseg)
    S["tb2"] = S["tb"].astype(str)
    out["falls_held_by_trend"] = S.groupby("tb2").agg(n=("g","size"), g_sum=("g","sum"), ex=("ex","mean"))
    H = x[x["alloc"]>0.01].copy(); H["tb2"] = H["tb"].astype(str)
    out["allheld_by_trend"] = H.groupby("tb2").agg(n=("g","size"), g_mean=("g","mean"), ex=("ex","mean"))
    return out
