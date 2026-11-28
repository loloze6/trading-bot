def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns: mean over coins each day, per window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().dropna()
    B = B.sort_values(["wn", "day"])
    v = (1 + B["br"]).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd.values
    out["overall"] = pd.Series({"days": len(B), "mean": B.br.mean(), "maxdd": dd.min(),
                                "total": v.iloc[-1] - 1})
    pw = B.groupby("wn").apply(lambda g: pd.Series({
        "sum_br": g.br.sum(), "sum_cr": g.cr.sum(),
        "dd_in_w": ((1 + g.br).cumprod() / (1 + g.br).cumprod().cummax() - 1).min(),
        "days": len(g)}))
    out["per_window"] = pw
    # locate deepest fall: window of trough and peak
    it = int(np.argmin(dd.values))
    ip = int(np.argmax(v.values[:it + 1]))
    out["deepest_fall"] = pd.Series({"peak_w": B.wn.iloc[ip], "trough_w": B.wn.iloc[it],
                                     "days_peak_to_trough": it - ip, "depth": dd.values[it]})
    # trade-level features
    tr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            r = cl.pct_change()
            b["r60"] = cl / cl.shift(60) - 1
            b["r1"] = r
            b["r7"] = cl / cl.shift(7) - 1
            b["sd30"] = r.rolling(30).std()
            b["z7"] = b["r7"] / (b["sd30"] * np.sqrt(7))
            b["r3f"] = cl.shift(-3) / cl - 1
            b["sd_ratio"] = r.rolling(10).std() / b["sd30"]
            b["dist_hi30"] = cl / cl.rolling(30).max() - 1
            b["inprof"] = b["regime"] == "unknown"
            b["sig"] = b["forecast"] > 0
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * (cl.shift(-1) / cl - 1)
            b["coin"] = c; b["w"] = w
            b["grid"] = (np.arange(len(b)) % 3) == 0
            tr.append(b)
    A = pd.concat(tr)
    G = A[A.grid & A.inprof].dropna(subset=["r3f"])
    drift = A[A.grid].groupby("coin")["r3f"].mean()
    G = G.assign(u=G["r3f"] - G["coin"].map(drift))
    out["grid_inprof_sig_vs_nosig"] = G.groupby("sig")["u"].agg(["mean", "count"])
    S = G[G.sig]
    def q(col, n=3):
        x = S.dropna(subset=[col])
        x = x.assign(b=pd.qcut(x[col], n, labels=False, duplicates="drop"))
        return x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), u=("u", "mean"),
                                  r3=("r3f", "mean"), n=("u", "count"))
    out["sig_by_z7"] = q("z7")
    out["sig_by_r60"] = q("r60")
    out["sig_by_r1"] = q("r1")
    out["sig_by_sdratio"] = q("sd_ratio")
    out["sig_by_disthi30"] = q("dist_hi30")
    # same splits on no-signal in-profile bars
    N = G[~G.sig]
    def qn(col):
        x = N.dropna(subset=[col]); x = x.assign(b=pd.qcut(x[col], 3, labels=False, duplicates="drop"))
        return x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), u=("u", "mean"), n=("u", "count"))
    out["nosig_by_r60"] = qn("r60")
    out["nosig_by_r1"] = qn("r1")
    # book gain by year and position days
    A["year"] = pd.to_datetime(A["timestamp"]).dt.year
    out["gain_by_year"] = A.groupby("year").agg(gain=("gain", "sum"), posdays=("pos", lambda s: (s != 0).sum()))
    # trades
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T)
    out["trades"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
                               "mean_gross": T.profit_loss_percent.mean(),
                               "win": (T.net_profit_loss_percent > 0).mean(),
                               "med_dur_days": T.duration_minutes.median() / 1440,
                               "worst": T.net_profit_loss_percent.min()})
    T["db"] = pd.cut(T.duration_minutes / 1440, [0, 3.5, 7, 14, 1000])
    out["trades_by_dur"] = T.groupby("db").net_profit_loss_percent.agg(["mean", "count", "sum"])
    out["alloc_held"] = A.loc[A.pos != 0, "pos"].describe()
    return out
