def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    h = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ret1 = c.pct_change()
            rng = ((b["high"] - b["low"]) / c).astype(float)
            df = pd.DataFrame({"coin": coin, "win": w,
                "fwd3": c.shift(-3)/c-1, "fwd7": c.shift(-7)/c-1,
                "ret5": c/c.shift(5)-1, "ret10": c/c.shift(10)-1,
                "vr": np.log(v.rolling(5).mean()/v.rolling(30).mean()),
                "rngr": np.log(rng.rolling(5).mean()/rng.rolling(30).mean()),
                "rngf3": rng[::-1].rolling(3).mean()[::-1].shift(-1) / rng.rolling(30).mean(),
                "volf3": v[::-1].rolling(3).mean()[::-1].shift(-1) / v.rolling(30).mean(),
                "pos": b["postRebalance_current_allocation"].astype(float),
                "nxt": c.shift(-1)/c-1})
            df["g3"] = (np.arange(len(b)) % 3 == 0)
            df["g7"] = (np.arange(len(b)) % 7 == 0)
            rows.append(df)
    A = pd.concat(rows)
    D = A[A["g3"]].dropna(subset=["fwd3"]).copy()
    D["ex"] = D["fwd3"] - D.groupby("coin")["fwd3"].transform("mean")
    def slope(S, x, y):
        S = S.dropna(subset=[x, y]); r = stats.linregress(S[x], S[y]); return (round(r.slope,4), round(r.slope/r.stderr,2), len(S))
    res = {}
    res["vr all"] = slope(D, "vr", "ex")
    res["vr down"] = slope(D[D.ret5<0], "vr", "ex")
    res["vr up"] = slope(D[D.ret5>=0], "vr", "ex")
    D["vr_x_sign"] = D["vr"]*np.sign(D["ret5"])
    res["vr*sign(ret5) all"] = slope(D, "vr_x_sign", "ex")
    res["ret5 all"] = slope(D, "ret5", "ex")
    res["ret5 high vol (vr>0)"] = slope(D[D.vr>0], "ret5", "ex")
    res["ret5 low vol (vr<=0)"] = slope(D[D.vr<=0], "ret5", "ex")
    D["absex"] = D["fwd3"].abs() - D.groupby("coin")["fwd3"].transform(lambda x: x.abs().mean())
    res["absret vs rngr"] = slope(D, "rngr", "absex")
    res["absret vs vr"] = slope(D, "vr", "absex")
    res["fwd range vs rngr"] = slope(D, "rngr", "rngf3")
    res["fwd vol vs vr"] = slope(D, "vr", "volf3")
    out["slopes (slope,t,n)"] = pd.DataFrame(res, index=["slope","t","n"]).T
    # vr slope per window-third (stability): windows grouped
    D["wn"] = D["win"].str[1:].astype(int)
    D["wgrp"] = pd.cut(D["wn"], [0,6,12,18,24], labels=["w1-6","w7-12","w13-18","w19-24"])
    st = {}
    for gname, s in D.groupby("wgrp"):
        st[str(gname)+" vr"] = slope(s, "vr", "ex")
        st[str(gname)+" vr*sign"] = slope(s, "vr_x_sign", "ex")
    out["by window group"] = pd.DataFrame(st, index=["slope","t","n"]).T
    pcs = {}
    for coin, s in D.groupby("coin"):
        pcs[coin] = slope(s, "vr_x_sign", "ex") + slope(s, "vr", "ex")
    out["per coin vr*sign (s,t,n) | vr (s,t,n)"] = pd.DataFrame(pcs, index=["s1","t1","n1","s2","t2","n2"]).T
    # 7-day horizon on g7
    E = A[A["g7"]].dropna(subset=["fwd7"]).copy()
    E["ex"] = E["fwd7"] - E.groupby("coin")["fwd7"].transform("mean")
    E["vr_x_sign"] = E["vr"]*np.sign(E["ret5"])
    out["7d slopes"] = pd.DataFrame({"vr": slope(E,"vr","ex"), "vr*sign": slope(E,"vr_x_sign","ex"), "ret5": slope(E,"ret5","ex")}, index=["slope","t","n"]).T
    # book: daily pnl from short vs long positions
    A2 = A.dropna(subset=["nxt","pos"])
    A2["pnl"] = A2["pos"]*A2["nxt"]
    side = np.where(A2["pos"]>0,"long",np.where(A2["pos"]<0,"short","flat"))
    out["bar pnl by side"] = A2.groupby(side)["pnl"].agg(["mean","sum","count"]).round(6)
    return out
