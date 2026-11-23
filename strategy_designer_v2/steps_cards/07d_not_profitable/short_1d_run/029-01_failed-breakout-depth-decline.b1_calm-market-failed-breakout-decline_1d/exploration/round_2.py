def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; allrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            vol120 = r.rolling(120, min_periods=40).std()
            vrel = vol / vol120
            hi = c.shift(1).rolling(20).max()
            bo = c > hi
            bosize = (c - hi) / hi / vol
            fail = pd.Series(False, index=c.index); lagk = pd.Series(np.nan, index=c.index); bsz = pd.Series(np.nan, index=c.index)
            for k in (1, 2, 3):
                oh = hi.shift(k)
                m = bo.shift(k).fillna(False).astype(bool) & (c < oh)
                new = m & lagk.isna()
                lagk = lagk.where(~new, k); bsz = bsz.where(~new, bosize.shift(k))
                fail |= m
            alloc = b["postRebalance_current_allocation"].astype(float)
            g = alloc * (c.shift(-1) / c - 1)
            g5 = sum(g.shift(-i) for i in range(5))
            n = len(c)
            for H in (5, 10):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n - H, H):
                    cell = range(i, min(i + H, n - H))
                    j = next((t for t in cell if fail.iloc[t]), None)
                    allrows.append(dict(H=H, coin=coin, fwd=fwd.iloc[i], vrel=vrel.iloc[i]))
                    if j is not None:
                        rows.append(dict(H=H, coin=coin, fwd=fwd.iloc[j], vol=vol.iloc[j], vrel=vrel.iloc[j],
                                         lagk=lagk.iloc[j], bsz=bsz.iloc[j], g5=g5.iloc[j], alloc=alloc.iloc[j]))
    A = pd.DataFrame(allrows); D = pd.DataFrame(rows)
    drift = A.groupby(["H", "coin"])["fwd"].mean()
    D["unus"] = -(D["fwd"] - [drift[(a, b)] for a, b in zip(D["H"], D["coin"])])
    D["tot"] = -D["fwd"]
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series(dict(n=len(x), mean_unus=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))), mean_tot=g["tot"].mean(),
                              book5=g["g5"].mean() if "g5" in g else np.nan))
    D5 = D[D.H == 5]; D10 = D[D.H == 10]
    out["H10_all"] = summ(D10)
    out["H10_by_q_vol"] = D10.groupby(pd.qcut(D10["vol"], 4, labels=False)).apply(summ)
    out["H5_by_q_vrel"] = D5.groupby(pd.qcut(D5["vrel"], 4, labels=False)).apply(summ)
    out["H5_by_lagk"] = D5.groupby("lagk").apply(summ)
    out["H5_by_q_bosize"] = D5.groupby(pd.qcut(D5["bsz"], 4, labels=False)).apply(summ)
    out["H5_by_q_vol_book_gain"] = D5.groupby(pd.qcut(D5["vol"], 4, labels=False))[["g5", "alloc"]].mean()
    lo = D5[D5["vol"] <= D5["vol"].quantile(0.25)]
    out["H5_lowvol_by_coin"] = lo.groupby("coin").apply(summ)
    out["H5_vol_q_edges"] = D5["vol"].quantile([0.25, 0.5, 0.75])
    out["H5_lowvol_by_lagk"] = lo.groupby("lagk").apply(summ)
    return out
