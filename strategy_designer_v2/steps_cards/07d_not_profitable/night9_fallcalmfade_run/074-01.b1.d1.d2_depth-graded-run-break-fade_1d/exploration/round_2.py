def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            sdmed = sd30.rolling(365, min_periods=120).median()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            down = (r < 0).astype(int).values
            run = np.zeros(len(b)); cnt = 0
            for i in range(len(b)):
                run[i] = cnt
                cnt = cnt + 1 if down[i] == 1 else 0
            ret60 = c / c.shift(60) - 1
            ret5z = (c / c.shift(5) - 1) / sd30
            a = b["postRebalance_current_allocation"]
            sig = (r > 0) & (run >= 2)
            df = pd.DataFrame(dict(coin=coin, wn=int(w[1:]), day=b["timestamp"].astype(str).str[:10],
                                   nxt=nxt, nxt2=nxt2, ret60=ret60, ret5z=ret5z, upz=r / sd30,
                                   agit=(sd30 > sdmed).where(sdmed.notna()), sig=sig,
                                   held=(a < 0) & (b["forecast"] < 0), alloc=a))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A = A[A.nxt.notna() & A.ret5z.notna()]
    F = A[A.ret60 < -0.10].copy()
    F["s"] = -F.nxt
    F["z5"] = pd.cut(F.ret5z, [-99, -2.1, -0.85, 0.07, 99])
    def agg(x):
        return pd.Series({"n": len(x), "mean": x.s.mean(), "t": x.s.mean() / (x.s.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["falling: signal vs not, by 5d z"] = F.groupby(["sig", "z5"], observed=True).apply(agg).unstack(0)
    out["falling: by agitation, signal only"] = F[F.sig].groupby("agit").apply(agg)
    out["falling: by agitation x deep 5d, signal"] = F[F.sig].groupby(["agit", F.ret5z < -0.85]).apply(agg)
    out["falling: all bars short next day"] = agg(F)
    # 2-day hold, signal, by z5 (non-overlap ignored for rough look)
    S = F[F.sig]
    out["signal 2d short by z5"] = S.groupby("z5", observed=True).agg(n=("nxt2", "size"), m2=("nxt2", lambda x: -x.mean()))
    # book loss days: held cases with losing next day > 4%
    H = A[A.held].copy(); H["s"] = -H.nxt
    big = H[H.s < -0.04]
    out["big-loss held cases profile"] = pd.Series({"n": len(big), "ret5z_mean": big.ret5z.mean(), "ret5z_all": H.ret5z.mean(),
        "upz_big": big.upz.mean(), "upz_all": H.upz.mean(), "share_z5_pos_big": (big.ret5z > 0.07).mean(),
        "share_z5_pos_all": (H.ret5z > 0.07).mean(), "agit_big": big.agit.mean(), "agit_all": H.agit.mean()})
    # simulated filtered book: daily mean over coins of |alloc|*short ret, per filter
    def book(mask, scale=None):
        X = A.copy()
        g = np.where(mask, X.alloc.abs() * (-X.nxt) if scale is None else scale * (-X.nxt), 0.0)
        X["g"] = g
        d = X.groupby(["wn", "day"]).g.mean().reset_index().sort_values(["wn", "day"])
        v = (1 + d.g).cumprod().values; pk = np.maximum.accumulate(v)
        mdd = (v / pk - 1).min(); yrs = len(d) / 365
        yr = v[-1] ** (1 / yrs) - 1
        return pd.Series({"yearly": yr, "maxdd": mdd, "calmar": yr / -mdd, "sharpe": d.g.mean() / d.g.std() * np.sqrt(365), "ncase": int(mask.sum())})
    held = A.held.values
    out["sim books"] = pd.DataFrame({
        "as held": book(held),
        "held, 5d z<0.07": book(held & (A.ret5z < 0.07).values),
        "held, 5d z<-0.85": book(held & (A.ret5z < -0.85).values),
        "held, agitated": book(held & (A.agit == True).values),
        "held, size by -5dz": book(held & (A.ret5z < 0).values, scale=np.clip(-A.ret5z.values, 0, 3) / 3 * 1.6),
    }).T
    return out
