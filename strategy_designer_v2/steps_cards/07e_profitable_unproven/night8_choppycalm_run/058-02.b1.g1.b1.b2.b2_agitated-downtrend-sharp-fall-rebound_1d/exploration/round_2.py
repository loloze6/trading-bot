def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    B = []
    for c, wd in data["bars"].items():
        for w, b in wd.items():
            t = b[["timestamp", "close", "high", "low", "regime", "forecast", "postRebalance_current_allocation"]].copy()
            t["coin"] = c; t["window"] = w
            t["ret"] = t.close.pct_change()
            t["std20"] = t.ret.rolling(20).std()
            t["std60"] = t.ret.rolling(60).std()
            t["z"] = t.ret / t.std20
            t["z60"] = t.ret / t.std60
            t["r60"] = t.close / t.close.shift(60) - 1
            t["r5"] = t.close / t.close.shift(5) - 1
            t["nxt"] = t.close.shift(-1) / t.close - 1
            t["f2"] = t.close.shift(-2) / t.close - 1
            t["pos"] = np.arange(len(t))
            B.append(t)
    B = pd.concat(B, ignore_index=True)
    mu = B.groupby("coin")["ret"].mean()
    B["mu"] = B.coin.map(mu)
    B["ex"] = B.nxt - B.mu
    B["day"] = pd.to_datetime(B.timestamp).dt.floor("D")

    def clslope(df, xcol, ycol="ex"):
        df = df.dropna(subset=[xcol, ycol])
        if len(df) < 20:
            return pd.Series({"n": len(df), "slope": np.nan, "t_cl": np.nan})
        x = df[xcol].values; y = df[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = np.zeros((2, 2))
        for _, idx in df.groupby("day").indices.items():
            s = (X[idx] * e[idx][:, None]).sum(0); S += np.outer(s, s)
        V = XtXi @ S @ XtXi
        return pd.Series({"n": len(df), "slope": beta[1], "t_cl": beta[1] / np.sqrt(V[1, 1])})

    fa = B[(B.regime == "unknown")].copy()
    pf = fa[fa.forecast > 0].copy()
    pf["absz"] = -pf.z
    pf["absz60"] = -pf.z60
    pf["fall"] = -pf.ret
    r = {}
    r["on_forecast"] = clslope(pf, "forecast")
    r["on_absz20"] = clslope(pf, "absz")
    r["on_absz60"] = clslope(pf, "absz60")
    r["on_rawfall"] = clslope(pf, "fall")
    r["on_absz20_no_z<-3"] = clslope(pf[pf.z > -3], "absz")
    r["on_forecast_no_z<-3"] = clslope(pf[pf.z > -3], "forecast")
    out["slopes_pos_forecast"] = pd.DataFrame(r).T
    # all fa days (both sides): slope of ex on -z
    fa["negz"] = -fa.z
    out["fa_allside_slope"] = clslope(fa, "negz")
    # by window, down days in fa
    d = fa[fa.z < 0].dropna(subset=["ex"])
    out["fa_down_by_window"] = d.groupby("window")["ex"].agg(["count", "mean"])
    out["fa_down_by_coin"] = d.groupby("coin")["ex"].agg(["count", "mean"])
    # winsorized mean and median
    out["fa_down_robust"] = pd.Series({"mean": d.ex.mean(), "median": d.ex.median(), "trim5": stats.trim_mean(d.ex, 0.05), "share_pos": (d.ex > 0).mean()})
    # outside profile, by own 60d trend (where computable)
    o = B[(B.regime != "unknown") & (B.z < 0)].dropna(subset=["ex", "r60"]).copy()
    o["trend"] = np.where(o.r60 > 0.1, "rising", np.where(o.r60 < -0.1, "falling", "choppy"))
    o["negz"] = -o.z
    out["other_down_by_trend"] = o.groupby("trend").apply(lambda s: pd.concat([clslope(s, "negz"), pd.Series({"mean_ex": s.ex.mean()})]))
    # in fa: does the prior 5-day fall add (fall after a run down)?
    d = d.dropna(subset=["r5"]).copy()
    d["r5b"] = pd.qcut(d.r5, 3, labels=["deep5", "mid5", "up5"])
    d["zb"] = pd.cut(d.z, [-np.inf, -1, -0.5, 0], labels=["big", "mid", "small"])
    out["fa_down_z_x_r5"] = d.groupby(["zb", "r5b"], observed=True)["ex"].agg(["count", "mean"]).unstack()
    # book gain by weekday of entry
    B["gain"] = B.postRebalance_current_allocation * B.nxt
    h = B[B.postRebalance_current_allocation.abs() > 1e-9].copy()
    h["wd"] = pd.to_datetime(h.timestamp).dt.weekday
    out["gain_by_weekday"] = h.groupby("wd")["gain"].agg(["count", "sum"])
    return out
