def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 7
    def build(off):
        rows = []
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values.astype(float); n = len(cl)
                s_ = pd.Series(cl)
                r1 = s_.pct_change(1).values; r14 = s_.pct_change(14).values; r60 = s_.pct_change(60).values
                r7 = s_.pct_change(7).values
                for i in range(off, n - H, H):
                    rows.append(dict(coin=c, wn=int(w[1:]), fwd=cl[i+H]/cl[i]-1, r1=r1[i], r7=r7[i], r14=r14[i],
                                     r60=r60[i], reg=df["regime"].iloc[i]))
        s = pd.DataFrame(rows)
        s["dm"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
        return s
    def ols_t(g, xs):
        g = g.dropna(subset=xs + ["dm"])
        X = np.column_stack([np.ones(len(g))] + [g[x].values for x in xs])
        y = g["dm"].values
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b; s2 = e @ e / (len(e) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return (b / se)[1:], len(g)
    out = {}
    res = {}
    for off in range(7):
        s = build(off)
        tr = s[s.reg == "trending"]; un = s[s.reg != "trending"]
        t1, n1 = ols_t(tr, ["r14", "r1"])
        t2, n2 = ols_t(un, ["r60"])
        t3, n3 = ols_t(un, ["r1"])
        t4, n4 = ols_t(tr, ["r14", "r7", "r1"])
        res[off] = dict(tr_r1_given_r14=t1[1], tr_r14=t1[0], n_tr=n1, un_r60=t2[0], n_un60=n2,
                        un_r1=t3[0], tr_r1_given_r14_r7=t4[2])
        if off == 0:
            halves = {}
            for nm, g in [("early w1-12", s[s.wn <= 12]), ("late w13-24", s[s.wn > 12])]:
                a, na = ols_t(g[g.reg == "trending"], ["r14", "r1"])
                b_, nb = ols_t(g[g.reg != "trending"], ["r60"])
                halves[nm] = dict(tr_r1_t=a[1], n_tr=na, un_r60_t=b_[0], n_un=nb)
            out["halves"] = pd.DataFrame(halves).T
            pc = {}
            for c, g in un.groupby("coin"):
                pc[c] = ols_t(g, ["r60"])[0][0]
            out["untrend r60 t per coin"] = pd.Series(pc)
    out["grid offsets t"] = pd.DataFrame(res).T
    return out
