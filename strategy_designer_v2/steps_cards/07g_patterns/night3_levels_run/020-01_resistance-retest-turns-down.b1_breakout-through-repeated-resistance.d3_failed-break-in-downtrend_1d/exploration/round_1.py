def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    out = {}
    rows = []      # grid rows, all bars
    caserows = []  # recorded short cases
    brk = []       # recomputed resistance crosses
    for coin, wins in data["bars"].items():
        grid_rets = []
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:]/c[:n-H]-1
            p20 = np.full(n, np.nan); p20[20:] = c[20:]/c[:-20]-1
            p10 = np.full(n, np.nan); p10[10:] = c[10:]/c[:-10]-1
            vol20 = pd.Series(r1).rolling(20).std().values
            f = b["forecast"].fillna(0).values
            # recomputed breaks: swing high closes (2 each side) in past 90 bars, known 2 bars later
            sh = np.zeros(n, bool)
            for i in range(2, n-2):
                if c[i] > max(c[i-2], c[i-1], c[i+1], c[i+2]): sh[i] = True
            brkflag = np.zeros(n); touches = np.zeros(n)
            for t in range(3, n):
                lv = [c[i] for i in range(max(0, t-90), t-2) if sh[i]]
                if not lv: continue
                lv = np.array(lv)
                crossed = lv[(c[t-1] <= lv) & (c[t] > lv)]
                if len(crossed):
                    L = crossed.max()
                    touches[t] = np.sum(np.abs(lv/L-1) <= 0.02)
                    brkflag[t] = 1
            for t in range(0, n, H):
                per.append(dict(coin=coin, w=w, fwd=fwd[t], p20=p20[t], p10=p10[t], vol=vol20[t],
                                r1=r1[t], wd=ts[t].weekday()))
            # cases: first short signal per grid cell (forecast becomes more negative by >=2)
            df_ = np.r_[0, np.diff(f)]
            for g0 in range(0, n, H):
                for t in range(g0, min(g0+H, n)):
                    if f[t] < 0 and df_[t] <= -2:
                        caserows.append(dict(coin=coin, fwd=fwd[t], p20=p20[t], f=f[t], wd=ts[t].weekday()))
                        break
            for g0 in range(0, n, H):
                for t in range(g0, min(g0+H, n)):
                    if brkflag[t]:
                        brk.append(dict(coin=coin, fwd=fwd[t], p20=p20[t], tch=touches[t], vol=vol20[t]))
                        break
        rows += per
    G = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].mean()
    sd = G.groupby("coin")["fwd"].std()
    out["drift_sd"] = pd.DataFrame({"drift": drift, "sd": sd})
    G["u"] = G["fwd"] - G["coin"].map(drift)
    G["z"] = G["u"]/G["coin"].map(sd)
    def summ(df, key):
        g = df.dropna(subset=[key, "u"]).groupby(key)["u"]
        return pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    G["p20q"] = G.groupby("coin")["p20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["p10q"] = G.groupby("coin")["p10"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    G["volq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    G["r1q"] = G.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["all_by_p20q"] = summ(G, "p20q")
    out["all_by_p10q"] = summ(G, "p10q")
    out["all_by_volq"] = summ(G, "volq")
    out["all_by_r1q"] = summ(G, "r1q")
    out["all_by_wd"] = summ(G, "wd")
    C = pd.DataFrame(caserows).dropna(subset=["fwd"])
    C["u"] = C["fwd"] - C["coin"].map(drift)
    C["p20q"] = pd.qcut(C["p20"], 4, labels=False)
    out["cases_by_p20q"] = summ(C, "p20q")
    out["cases_by_coin"] = summ(C, "coin")
    B = pd.DataFrame(brk).dropna(subset=["fwd", "p20"])
    B["u"] = B["fwd"] - B["coin"].map(drift)
    B["down"] = (B["p20"] < 0).astype(int)
    out["brk_by_trend"] = summ(B, "down")
    B["tq"] = B["tch"].clip(upper=3)
    out["brk_by_touch"] = summ(B, "tq")
    B["p20q"] = pd.qcut(B["p20"], 5, labels=False)
    out["brk_by_p20q"] = summ(B, "p20q")
    return out
