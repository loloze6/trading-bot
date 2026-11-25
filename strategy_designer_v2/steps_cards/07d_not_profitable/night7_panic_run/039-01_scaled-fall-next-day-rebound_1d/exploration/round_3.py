def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cmean = {}
    for c, ws in data["bars"].items():
        rr = [(b["close"].shift(-1)/b["close"]-1).dropna() for w, b in ws.items()]
        cmean[c] = pd.concat(rr).mean()
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            nxt = cl.shift(-1)/cl - 1
            r5 = cl/cl.shift(5) - 1
            r3 = cl.shift(1)/cl.shift(4) - 1  # 3 days before the fall day
            vr = sd / r.rolling(90, min_periods=60).std()
            rows.append(pd.DataFrame({"coin": c, "w": w, "wi": int(w[1:]), "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"), "z": z, "nxt": nxt,
                "ex": nxt - cmean[c], "r5": r5, "r3": r3, "vr": vr,
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
        return pd.Series({"sharpe": B.mean()/B.std()*np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr/abs(dd), "inpos": (x["p"].abs()>0.01).mean()})
    a = d["alloc"]
    res = {"actual": book(a)}
    res["cap0.5"] = book(a.clip(upper=0.5))
    res["cap1.0"] = book(a.clip(upper=1.0))
    res["half_when_vr>1"] = book(a.where(~(d["vr"] > 1), a*0.5))
    res["out_when_vr>1.3"] = book(a.where(~(d["vr"] > 1.3), 0))
    res["only_r5<-0.05"] = book(a.where(d["r5"] < -0.05, 0))
    res["z<-0.5_only"] = book(a.where(d["z"] < -0.5, 0))
    res["z<-0.5_cap1"] = book(a.where(d["z"] < -0.5, 0).clip(upper=1.0))
    out["variants"] = pd.DataFrame(res).T
    dn = d[(d["z"] < 0)].dropna(subset=["z"]).copy()
    dn["zc"] = pd.cut(dn["z"], [-99,-1.5,-0.5,0], labels=["<-1.5","-1.5..-0.5","-0.5..0"])
    dn["vb"] = pd.cut(dn["vr"], [0,0.8,1.0,1.3,99], labels=["<0.8","0.8-1","1-1.3",">1.3"])
    out["ex_down_z_x_vr"] = dn.groupby(["vb","zc"], observed=True)["ex"].agg(["size","mean"]).unstack(1)
    up = d[d["z"] >= 0].copy()
    up["vb"] = pd.cut(up["vr"], [0,0.8,1.0,1.3,99], labels=["<0.8","0.8-1","1-1.3",">1.3"])
    out["ex_up_by_vr_condition_alone"] = up.groupby("vb", observed=True)["ex"].agg(["size","mean"])
    dn["r3b"] = pd.cut(dn["r3"], [-9,-0.1,-0.03,0.03,9], labels=["<-10%","-10..-3","-3..3",">3"])
    out["ex_down_z_x_prior3"] = dn.groupby(["r3b","zc"], observed=True)["ex"].agg(["size","mean"]).unstack(1)
    up["r3b"] = pd.cut(up["r3"], [-9,-0.1,-0.03,0.03,9], labels=["<-10%","-10..-3","-3..3",">3"])
    out["ex_up_by_prior3_alone"] = up.groupby("r3b", observed=True)["ex"].agg(["size","mean"])
    # big fall t per day-cluster, r5<-15%
    big = dn[dn["z"] < -1.5].copy()
    for nm, m in [("r5<-15%", big["r5"] < -0.15), ("r5>=-15%", big["r5"] >= -0.15)]:
        s = big[m].groupby("day")["ex"].sum(); n = m.sum()
        out[f"bigfall_{nm}"] = f"n={n}, days={len(s)}, mean={big[m]['ex'].mean():.4f}, t={s.mean()/(s.std()/np.sqrt(len(s))):.2f}"
    md = d[(d["r5"] < -0.15) & (d["z"] >= -0.5)]
    out["r5<-15%_without_bigfall"] = f"n={len(md)}, mean={md['ex'].mean():.4f}"
    return out
