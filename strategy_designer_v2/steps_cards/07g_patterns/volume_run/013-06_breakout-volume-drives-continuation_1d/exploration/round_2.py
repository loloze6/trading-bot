def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = cl.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            vr = v / v.rolling(30, min_periods=20).mean()
            z1 = r1 / vol20
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (1, 3):
                fwd = cl.shift(-h) / cl - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=c, w=w, h=h, fwd=fwd.iloc[i], vr=vr.iloc[i], z1=z1.iloc[i],
                                     yr=yr.iloc[i], r1=r1.iloc[i]))
    df = pd.DataFrame(rows).dropna()
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["lvr"] = np.log(df["vr"])
    def hl(d, var):
        q = d.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        hi = d.ex[q == 4]; lo = d.ex[q == 0]
        return pd.Series({"hi_minus_lo": hi.mean() - lo.mean(),
                          "t": stats.ttest_ind(hi, lo, equal_var=False).statistic,
                          "rho": stats.spearmanr(d[var], d.ex).correlation, "n": len(d)})
    for h in (1, 3):
        d = df[df.h == h]
        out[f"vr_by_coin_h{h}"] = d.groupby("coin").apply(lambda x: hl(x, "lvr")).round(4)
        out[f"z1_by_coin_h{h}"] = d.groupby("coin").apply(lambda x: hl(x, "z1")).round(4)
    d = df[df.h == 1]
    out["vr_by_year_h1"] = d.groupby("yr").apply(lambda x: hl(x, "lvr")).round(4)
    out["z1_by_year_h1"] = d.groupby("yr").apply(lambda x: hl(x, "z1")).round(4)
    # interaction: volume on up vs down days
    d = d.assign(up=d.r1 > 0)
    out["vr_split_by_day_sign_h1"] = d.groupby("up").apply(lambda x: hl(x, "lvr")).round(4)
    # z1 within high vs low volume
    d = d.assign(hv=d.groupby("coin")["lvr"].transform(lambda s: s > s.median()))
    out["z1_split_by_highvol_h1"] = d.groupby("hv").apply(lambda x: hl(x, "z1")).round(4)
    # joint regression
    X = np.column_stack([np.ones(len(d)), (d.lvr - d.lvr.mean()) / d.lvr.std(), (d.z1 - d.z1.mean()) / d.z1.std()])
    beta, *_ = np.linalg.lstsq(X, d.ex.values, rcond=None)
    res = d.ex.values - X @ beta
    s2 = res.var(ddof=3); cov = s2 * np.linalg.inv(X.T @ X)
    out["joint_reg_h1"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "lvr", "z1"]).round(5)
    return out
