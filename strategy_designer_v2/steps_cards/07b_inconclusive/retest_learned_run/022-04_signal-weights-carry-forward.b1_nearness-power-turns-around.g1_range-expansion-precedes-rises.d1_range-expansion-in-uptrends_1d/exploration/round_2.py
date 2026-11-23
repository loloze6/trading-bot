def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        drift = {}
        for h in [3, 5, 10]:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[h] = np.mean(rs)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            hl = df["high"] - df["low"]
            ratio = hl / hl.rolling(30, min_periods=30).mean()
            r20 = c / c.shift(20) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in [3, 5, 10]:
                for off in range(h):
                    for i in range(off, n - h, h):
                        rows.append(dict(coin=coin, h=h, off=off, year=yr.iloc[i], fc=df["forecast"].iloc[i],
                                         reg=df["regime"].iloc[i], ratio=ratio.iloc[i], r20=r20.iloc[i],
                                         ex=c.iloc[i + h] / c.iloc[i] - 1 - drift[h]))
    R = pd.DataFrame(rows)

    def slope(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 20 or d[x].std() == 0:
            return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        res = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(n=len(d), slope=res.slope, t=res.slope / res.stderr))

    T = R[R.reg == "trending"]
    out = {}
    out["h5_fc_by_grid_offset"] = T[T.h == 5].groupby("off").apply(slope)
    out["h5_ratio_by_grid_offset"] = T[T.h == 5].groupby("off").apply(lambda d: slope(d, "ratio"))
    T10 = T[(T.h == 10) & (T.off == 0)]
    out["h10_ratio_by_coin"] = T10.groupby("coin").apply(lambda d: slope(d, "ratio"))
    out["h10_ratio_by_year"] = T10.groupby("year").apply(lambda d: slope(d, "ratio"))
    T3 = T[(T.h == 3) & (T.off == 0)]
    out["h3_ratio_by_coin"] = T3.groupby("coin").apply(lambda d: slope(d, "ratio"))
    A = R[(R.h == 5) & (R.off == 0)].dropna(subset=["ratio", "r20", "ex"]).copy()
    A["up"] = (A.r20 > 0).astype(float)
    A["rxu"] = A.ratio * A.up
    X = np.column_stack([np.ones(len(A)), A.ratio, A.up, A.rxu])
    b, *_ = np.linalg.lstsq(X, A.ex.values, rcond=None)
    res = A.ex.values - X @ b
    s2 = res @ res / (len(A) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["h5_interaction"] = pd.DataFrame(dict(coef=b, t=b / se), index=["const", "ratio", "up", "ratio_x_up"])
    return out
