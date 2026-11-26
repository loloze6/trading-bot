def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    d1 = []; w7 = []
    for coin, wins in bars.items():
        g7 = []; g1 = []; g3 = []
        for w, df in wins.items():
            c = df["close"].values
            g7 += [c[i+7]/c[i]-1 for i in range(0, len(c)-7, 7)]
            g3 += [c[i+3]/c[i]-1 for i in range(0, len(c)-3, 3)]
            g1 += list(c[1:]/c[:-1]-1)
        m7, m3, m1 = np.mean(g7), np.mean(g3), np.mean(g1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r = c.pct_change()
            sd30 = r.rolling(30).std()
            sd365 = r.rolling(90, min_periods=60).std()
            net = (c - c.shift(30)).abs(); path = c.diff().abs().rolling(30).sum()
            er = net/path
            r7 = c/c.shift(7)-1; z7 = r7/(sd30*np.sqrt(7))
            f1 = c.shift(-1)/c-1; f3 = c.shift(-3)/c-1; f7 = c.shift(-7)/c-1
            ts = df["timestamp"].astype(str).str[:10]
            yr = df["timestamp"].astype(str).str[:4]
            for i in range(30, len(c)-1):
                if not sd30[i] > 0: continue
                d1.append(dict(coin=coin, w=w, day=ts[i], yr=yr[i], z1=r[i]/sd30[i], f1=f1[i]-m1,
                               er=er[i], vr=sd30[i]/sd365[i] if sd365[i]>0 else np.nan,
                               pos=df["postRebalance_current_allocation"][i]))
            for i in range(0, len(c)-7, 7):
                if np.isnan(z7[i]) or np.isnan(er[i]): continue
                w7.append(dict(coin=coin, w=w, day=ts[i], yr=yr[i], z7=z7[i], fx=f7[i]-m7,
                               vr=sd30[i]/sd365[i] if sd365[i]>0 else np.nan, er=er[i]))
            # 3-day after daily z1, on 3-day grid
            for i in range(30, len(c)-3, 3):
                if not sd30[i] > 0: continue
                d1[-1]  # noop
    D = pd.DataFrame(d1); W = pd.DataFrame(w7)
    out = {}
    def clus_t(df, y, x=None):
        # day-clustered t of mean (x None) or slope
        df = df.dropna(subset=[y] + ([x] if x else []))
        if x is None:
            s = (df[y]-df[y].mean()).groupby(df["day"]).sum()
            se = np.sqrt((s**2).sum())/len(df)
            return pd.Series(dict(n=len(df), days=df["day"].nunique(), mean=df[y].mean(), t=df[y].mean()/se))
        X = df[x]-df[x].mean(); b = (X*df[y]).sum()/(X**2).sum()
        e = df[y]-df[y].mean()-b*X
        s = (X*e).groupby(df["day"]).sum()
        se = np.sqrt((s**2).sum())/(X**2).sum()
        return pd.Series(dict(n=len(df), days=df["day"].nunique(), slope=b, t=b/se))
    D["zd"] = pd.qcut(D["z1"], 10, labels=False)
    out["f1x_by_z1decile_clustered"] = D.groupby("zd").apply(lambda g: clus_t(g, "f1"))
    Dn = D[D.z1 < 0]
    out["slope_f1_on_z1_falls_only"] = clus_t(Dn, "f1", "z1")
    out["slope_f1_on_z1_rises_only"] = clus_t(D[D.z1 > 0], "f1", "z1")
    Dn = Dn.assign(vq=pd.qcut(Dn["vr"], 3, labels=False), erq=pd.qcut(Dn["er"], 3, labels=False))
    out["falls_slope_by_volratio_tercile"] = Dn.groupby("vq").apply(lambda g: clus_t(g, "f1", "z1"))
    out["falls_slope_by_er_tercile"] = Dn.groupby("erq").apply(lambda g: clus_t(g, "f1", "z1"))
    out["falls_bottomdecile_by_year"] = D[D.zd == 0].groupby("yr").apply(lambda g: clus_t(g, "f1"))
    out["falls_bottomdecile_by_coin"] = D[D.zd == 0].groupby("coin").apply(lambda g: clus_t(g, "f1"))
    out["falls_bottomdecile_share_in_position"] = float((D[D.zd == 0]["pos"].abs() > 0).mean())
    out["weekday_note"] = "skip"
    # 7-day momentum
    out["slope_f7_on_z7_all"] = clus_t(W, "fx", "z7")
    W = W.assign(vq=pd.qcut(W["vr"], 3, labels=False))
    out["slope_f7_on_z7_by_volratio"] = W.groupby("vq").apply(lambda g: clus_t(g, "fx", "z7"))
    out["slope_f7_on_z7_by_year"] = W.groupby("yr").apply(lambda g: clus_t(g, "fx", "z7"))
    out["slope_f7_on_z7_by_coin"] = W.groupby("coin").apply(lambda g: clus_t(g, "fx", "z7"))
    return out
