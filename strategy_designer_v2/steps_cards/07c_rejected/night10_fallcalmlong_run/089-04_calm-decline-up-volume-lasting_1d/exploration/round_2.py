def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); v = df["volume"].astype(float)
            d = c.diff()
            up = (d > 0).astype(float); dn = (d < 0).astype(float)
            v60 = v.rolling(60).mean()
            share = (v*up).rolling(20).sum() / v.rolling(20).sum()
            upv = (v*up).rolling(20).sum() / (20*v60)      # up-day volume vs 60d norm
            dnv = (v*dn).rolling(20).sum() / (20*v60)      # down-day volume vs 60d norm
            volr = v.rolling(20).mean() / v60
            # relative up-day intensity: mean vol on up days / mean vol on down days
            upm = (v*up).rolling(20).sum() / up.rolling(20).sum()
            dnm = (v*dn).rolling(20).sum() / dn.rolling(20).sum()
            ratio = np.log(upm/dnm)
            fc = (df["regime"] == "unknown")
            n = len(df)
            for h in [5, 10]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fc=bool(fc.iloc[i]),
                                     share=share.iloc[i], upv=upv.iloc[i], dnv=dnv.iloc[i],
                                     volr=volr.iloc[i], ratio=ratio.iloc[i], fwd=fwd.iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows).dropna()
    R = R[np.isfinite(R["ratio"])]
    R["ex"] = R["fwd"] - R.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    res = []
    for (h, f), g in R.groupby(["h", "fc"]):
        for var in ["share", "upv", "dnv", "volr", "ratio"]:
            sl = stats.linregress(g[var], g["ex"])
            res.append(dict(h=h, fc=f, var=var, n=len(g), slope=sl.slope, t=sl.slope/sl.stderr,
                            rho=stats.spearmanr(g[var], g["ex"])[0]))
    out["univariate"] = pd.DataFrame(res)
    # multivariate in falling calm: share, volr, share*volr centred
    mv = []
    for h, g in R[R.fc].groupby("h"):
        X = pd.DataFrame({"const": 1.0, "share": g["share"]-0.5, "volr": g["volr"]-1,
                          "inter": (g["share"]-0.5)*(g["volr"]-1)})
        y = g["ex"].values
        b, *_ = np.linalg.lstsq(X.values, y, rcond=None)
        resid = y - X.values @ b
        s2 = resid @ resid / (len(y)-X.shape[1])
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.values.T @ X.values)))
        for k, nm in enumerate(X.columns):
            mv.append(dict(h=h, term=nm, coef=b[k], t=b[k]/se[k], n=len(y)))
    out["fc_multivar"] = pd.DataFrame(mv)
    # upv terciles in falling calm
    q = []
    for h, g in R[R.fc].groupby("h"):
        g = g.copy(); g["q"] = pd.qcut(g["upv"], 3, labels=False)
        for k, gg in g.groupby("q"):
            q.append(dict(h=h, q=k, n=len(gg), upv=gg["upv"].mean(), mean_ex=gg["ex"].mean(),
                          t=gg["ex"].mean()/(gg["ex"].std()/np.sqrt(len(gg)))))
    out["fc_upv_terciles"] = pd.DataFrame(q)
    # upv slope by coin, h=5
    cc = []
    for coin, g in R[(R.fc) & (R.h == 5)].groupby("coin"):
        sl = stats.linregress(g["upv"], g["ex"])
        sl2 = stats.linregress(g["volr"], g["ex"])
        cc.append(dict(coin=coin, n=len(g), upv_slope=sl.slope, upv_t=sl.slope/sl.stderr,
                       volr_slope=sl2.slope, volr_t=sl2.slope/sl2.stderr))
    out["fc_by_coin_h5"] = pd.DataFrame(cc)
    yy = []
    for yr, g in R[(R.fc) & (R.h == 5)].groupby("year"):
        if len(g) < 8: continue
        sl = stats.linregress(g["upv"], g["ex"])
        yy.append(dict(year=yr, n=len(g), upv_slope=sl.slope, upv_t=sl.slope/sl.stderr))
    out["fc_by_year_h5"] = pd.DataFrame(yy)
    out["corr_upv_volr_share_fc"] = R[R.fc & (R.h==5)][["share","upv","dnv","volr"]].corr()
    return out
