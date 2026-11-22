def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    allrows = {}
    for H in [2, 4, 8, 12]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float).values
                n = len(c)
                ts = pd.to_datetime(b["timestamp"])
                s = pd.Series(c)
                r1 = s.pct_change().values
                r3 = s.pct_change(3).values
                vol20 = pd.Series(r1).shift(1).rolling(20).std().values
                hi20 = s.shift(1).rolling(20).max().values
                bo = c > hi20
                for i in range(0, n - H, H):
                    fwd = c[i + H] / c[i] - 1
                    fb = np.nan
                    for k in range(max(0, i - 5), i):
                        if bo[k] and not np.isnan(hi20[k]) and c[i] < hi20[k]:
                            fb = c[i] / hi20[k] - 1
                    rows.append(dict(coin=coin, w=w, year=ts[i].year, fwd=fwd, r1=r1[i], r3=r3[i],
                                     z1=r1[i] / vol20[i] if vol20[i] else np.nan, vol20=vol20[i], fb=fb))
        d = pd.DataFrame(rows)
        d["u"] = d["fwd"] - d["coin"].map(d.groupby("coin")["fwd"].mean())
        allrows[H] = d
    def quint(x, col, q=5, by_coin=True):
        x = x.dropna(subset=[col, "u"]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("b")["u"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        return g.drop(columns="std").round(4)
    def slope(x, col):
        x = x.dropna(subset=[col, "u"])
        r = stats.linregress(x[col], x["u"])
        return r.slope, r.slope / r.stderr, len(x)
    sl = {}
    for H, d in allrows.items():
        for col in ["r1", "z1", "r3"]:
            s_, t_, n_ = slope(d, col)
            sl[f"H{H}_{col}"] = [s_, t_, n_]
    out["slope_u_on_past_by_horizon"] = pd.DataFrame(sl, index=["slope", "t", "n"]).T.round(4)
    d8 = allrows[8]
    out["H8_quint_z1"] = quint(d8, "z1")
    out["H4_quint_z1"] = quint(allrows[4], "z1")
    # by coin and by year: slope of u on z1, H=8
    pc = {}
    for coin, x in d8.groupby("coin"):
        s_, t_, n_ = slope(x, "z1"); pc[coin] = [s_, t_, n_]
    out["H8_z1_slope_by_coin"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T.round(4)
    py = {}
    for y, x in d8.groupby("year"):
        s_, t_, n_ = slope(x, "z1"); py[y] = [s_, t_, n_]
    out["H8_z1_slope_by_year"] = pd.DataFrame(py, index=["slope", "t", "n"]).T.round(4)
    # by vol regime (tercile of vol20 within coin)
    x = d8.dropna(subset=["vol20", "z1"]).copy()
    x["vb"] = x.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    pv = {}
    for v, y in x.groupby("vb"):
        s_, t_, n_ = slope(y, "z1"); pv[v] = [s_, t_, n_]
    out["H8_z1_slope_by_vol_tercile"] = pd.DataFrame(pv, index=["slope", "t", "n"]).T.round(4)
    # sign split: down days vs up days
    ps = {}
    for nm, y in [("down_day", d8[d8.r1 < 0]), ("up_day", d8[d8.r1 > 0])]:
        s_, t_, n_ = slope(y, "z1"); ps[nm] = [s_, t_, n_, y["u"].mean()]
    out["H8_z1_slope_by_sign"] = pd.DataFrame(ps, index=["slope", "t", "n", "mean_u"]).T.round(4)
    # failed breakout: depth gradient and by horizon
    fbr = {}
    for H, d in allrows.items():
        y = d.dropna(subset=["fb"])
        rest = d[d["fb"].isna()]["u"]
        s_ = stats.linregress(y["fb"], y["u"]) if len(y) > 5 else None
        fbr[H] = [y["u"].mean(), len(y), stats.ttest_ind(y["u"], rest, equal_var=False).statistic,
                  s_.slope if s_ else np.nan, s_.slope / s_.stderr if s_ else np.nan]
    out["failed_breakout_by_horizon"] = pd.DataFrame(fbr, index=["mean_u", "n", "t_vs_rest", "slope_on_depth", "t_slope"]).T.round(4)
    # does the fb effect survive controlling for z1? H8 regression u ~ z1 + fbflag
    y = d8.dropna(subset=["z1"]).copy(); y["f"] = y["fb"].notna().astype(float)
    X = np.column_stack([np.ones(len(y)), y["z1"], y["f"]])
    beta, *_ = np.linalg.lstsq(X, y["u"].values, rcond=None)
    res = y["u"].values - X @ beta
    s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["H8_u_on_z1_and_fb"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z1", "fb"]).round(4)
    return out
