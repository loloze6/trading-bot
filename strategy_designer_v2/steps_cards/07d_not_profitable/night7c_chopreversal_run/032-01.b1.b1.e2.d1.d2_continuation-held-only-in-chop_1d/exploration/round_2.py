def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 7
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            net = (c - c.shift(30)).abs()
            path = c.diff().abs().rolling(30).sum()
            er = net / path
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            z = r7 / (sd30 * np.sqrt(7))
            fc = b["forecast"].astype(float)
            pos = b["postRebalance_current_allocation"].astype(float)
            fwd = c.shift(-H) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, fc=fc[i], fwd=fwd[i], er=er[i], z=z[i], r30=r30[i], pos=pos[i]))
            ts = pd.to_datetime(b["timestamp"])
            agree = (np.sign(pos.shift(1)) == np.sign(r30.shift(1))).astype(float)
            daily.append(pd.DataFrame(dict(coin=coin, w=w, day=ts.dt.floor("D"), g=pos.shift(1) * r1,
                                           pos=pos.shift(1), r1=r1, er=er.shift(1), agree=agree,
                                           chop=(er.shift(1) <= 0.3).astype(float),
                                           inpos=(pos.shift(1).abs() > 0).astype(float))))
    G = pd.DataFrame(rows).dropna(subset=["fwd", "z", "er", "r30"])
    mu = G.groupby("coin")["fwd"].mean()
    G["dm"] = G["fwd"] - G["coin"].map(mu)
    G["chop"] = np.where(G.er <= 0.3, "chop", "nonchop")
    G["agree"] = np.where(np.sign(G.z) == np.sign(G.r30), "z_with_r30", "z_against_r30")
    G["sz"] = np.sign(G.z) * G.dm
    G["s30"] = np.sign(G.r30) * G.dm
    def st(x):
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x)))))
    out["z-direction unusual by chop x agree"] = G.groupby(["chop", "agree"]).sz.apply(st).unstack().round(4)
    out["r30-direction unusual by chop (condition alone)"] = G.groupby("chop").s30.apply(st).unstack().round(4)
    C = G[(G.chop == "chop") & (G.agree == "z_with_r30")].copy()
    C["zq"] = pd.qcut(C.z.abs(), 3, labels=False)
    out["chop & agree: by |z| tercile"] = C.groupby("zq").sz.apply(st).unstack().round(4)
    C2 = G[G.chop == "chop"].copy()
    C2["r30q"] = pd.qcut(C2.r30.abs() , 3, labels=False)
    out["chop: z-direction by |r30| tercile"] = C2.groupby("r30q").sz.apply(st).unstack().round(4)
    # fc sign vs z sign on chop
    A = G[G.fc != 0].copy()
    A["fz"] = np.where(np.sign(A.fc) == np.sign(A.z), "fc=z", "fc!=z")
    A["sf"] = np.sign(A.fc) * A.dm
    out["fc-direction unusual by fc/z sign agreement"] = A.groupby("fz").sf.apply(st).unstack().round(4)
    out["held after chop ends: share of grid bars nonchop with pos!=0"] = float(((G.chop == "nonchop") & (G.pos.abs() > 0)).mean())
    # book days
    D = pd.concat(daily).dropna(subset=["g"])
    D["gi"] = D.g * D.agree
    D["go"] = D.g * (1 - D.agree)
    D["gc"] = D.g * D.chop
    D["gn"] = D.g * (1 - D.chop)
    bd = D.groupby(["w", "day"]).agg(g=("g", "mean"), gi=("gi", "mean"), go=("go", "mean"),
                                    gc=("gc", "mean"), gn=("gn", "mean"), r=("r1", "mean")).reset_index()
    bd["wn"] = bd.w.str[1:].astype(int)
    bd = bd.sort_values(["wn", "day"]).reset_index(drop=True)
    out["book daily mean: all / pos with r30 / pos against r30 / held in chop / held outside chop"] = bd[["g", "gi", "go", "gc", "gn"]].mean().round(6)
    out["book daily sd of each part"] = bd[["g", "gi", "go"]].std().round(5)
    for k in ["g", "gi", "go"]:
        eq = (1 + bd[k]).cumprod()
        out[f"deepest fall chained {k}"] = float((eq / eq.cummax() - 1).min())
    # falls: days in deepest 3 drawdown episodes
    eq = (1 + bd.g).cumprod(); dd = eq / eq.cummax() - 1
    bd["dd"] = dd
    fall = bd.dd < -0.15
    out["fall days (dd<-15%) count, mean g, gi, go, r"] = bd[fall][["g", "gi", "go", "r"]].mean().round(5).to_string() + f" n={int(fall.sum())}"
    out["share of book days in position held outside chop"] = float((D.chop == 0).where(D.inpos == 1).mean())
    return out
