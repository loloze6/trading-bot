def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; dayrows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            vol720 = r1.rolling(720, min_periods=240).std()
            z = r1 / vol24
            vr = vol24 / vol720
            ts = pd.to_datetime(b["timestamp"], utc=True)
            alloc = b["postRebalance_current_allocation"].astype(float)
            nxt = c.shift(-1)/c - 1
            pv = b["postRebalance_total_value"].astype(float)
            gain = pv.pct_change()
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "year": ts.dt.year,
                               "fc": b["forecast"].astype(float), "alloc": alloc,
                               "pg": alloc*nxt, "gain": gain, "r24p": c/c.shift(24)-1,
                               "r168p": c/c.shift(168)-1})
            fr = c.shift(-24)/c - 1
            df["f24"] = fr
            g = np.zeros(len(c), bool); g[::24] = True
            df["g24"] = g
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # book: position gain before cost by side and year
    D["side"] = np.where(D.alloc > 0, "long", np.where(D.alloc < 0, "short", "flat"))
    out["pos gain before cost by side (sum %, mean bp/bar, bars)"] = D.groupby("side").agg(
        sum_pct=("pg", lambda x: 100*x.sum()), bp=("pg", lambda x: 1e4*x.mean()), n=("pg", "size"))
    out["pos gain by year x side (sum %)"] = D.pivot_table(index="year", columns="side", values="pg", aggfunc=lambda x: 100*x.sum())
    out["mean |alloc| by side"] = D[D.side!="flat"].groupby("side")["alloc"].apply(lambda x: x.abs().mean())
    # turnover cost proxy
    D["turn"] = D.groupby(["coin","w"])["alloc"].diff().abs()
    out["total turnover (sum |dalloc|) and mean bar gain"] = pd.Series({"turnover": D["turn"].sum(), "sum_gain_pct": 100*D["pg"].sum(),
        "cost_at_0.095pct_per_side_pct": 100*D["turn"].sum()*0.00095})
    # grid: condition alone vs condition + signal, long side
    G = D[D.g24].dropna(subset=["f24","z","vr"]).copy()
    G["dr"] = G.groupby("coin")["f24"].transform("mean")
    G["exl"] = G["f24"] - G["dr"]
    def st(s):
        return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    grp = {}
    grp["all bars long"] = G["exl"]
    grp["vr>1 long, any z"] = G.loc[G.vr>1, "exl"]
    grp["vr>1, z>-0.5 long (cond w/o signal)"] = G.loc[(G.vr>1)&(G.z>-0.5), "exl"]
    grp["vr<=1, z<-1 long (signal w/o cond)"] = G.loc[(G.vr<=1)&(G.z<-1), "exl"]
    for lo, hi in [(-0.5,0),(-1,-0.5),(-1.5,-1),(-2,-1.5),(-3,-2),(-100,-3)]:
        grp[f"vr>1, z in ({lo},{hi}] long"] = G.loc[(G.vr>1)&(G.z>lo)&(G.z<=hi), "exl"]
    for lo, hi in [(0,0.5),(0.5,1),(1,1.5),(1.5,2),(2,100)]:
        grp[f"vr>1, z in ({lo},{hi}] short"] = -G.loc[(G.vr>1)&(G.z>lo)&(G.z<=hi), "exl"]
    out["grid h24 long/short excess"] = pd.DataFrame({k: st(v) for k, v in grp.items()}).T
    # long after down-hour, split by prior 7-day trend (in vr>1)
    L = G[(G.vr>1)&(G.z<-0.5)].copy()
    L["t7"] = pd.qcut(L["r168p"], 3, labels=["down7d","mid7d","up7d"])
    out["vr>1 z<-0.5 long by 7d trend"] = L.groupby("t7", observed=True)["exl"].apply(st).unstack()
    Sh = G[(G.vr>1)&(G.z>0.5)].copy()
    Sh["t7"] = pd.qcut(Sh["r168p"], 3, labels=["down7d","mid7d","up7d"])
    out["vr>1 z>0.5 short by 7d trend"] = Sh.groupby("t7", observed=True)["exl"].apply(lambda s: st(-s)).unstack()
    # forecast vs raw z relation
    A = D[D.fc!=0].dropna(subset=["z"])
    A["zb"] = pd.cut(A.z.abs(), [0,0.5,1,2,100])
    out["share capped |fc|>=19.9 by |z|"] = A.groupby("zb", observed=True)["fc"].apply(lambda x: (x.abs()>=19.9).mean())
    out["share active bars capped"] = (A.fc.abs()>=19.9).mean()
    # grid long by year
    Ly = G[(G.vr>1)&(G.z<-0.5)]
    out["vr>1 z<-0.5 long by year"] = Ly.groupby("year")["exl"].apply(st).unstack()
    return out
