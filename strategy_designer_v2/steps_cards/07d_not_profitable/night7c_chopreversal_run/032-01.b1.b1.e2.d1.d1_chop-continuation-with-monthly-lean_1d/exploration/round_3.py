def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            vol90 = r1.rolling(90, min_periods=60).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            fee = (pos - pos.shift(1).fillna(0)).abs() * 0.0019 / 2
            gain = pos * (c.shift(-1) / c - 1)
            fwd7 = c.shift(-7) / c - 1
            mv7 = ret7 / (vol30 * np.sqrt(7))
            sig = ((er < 0.3) & (((ret30 > 0) & (mv7 > 0)) | ((ret30 < 0) & (mv7 < 0))))
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "pos": pos,
                               "gain": gain, "fee": fee, "er": er, "ret30": ret30, "mv7": mv7,
                               "vol30": vol30, "vr": vol30 / vol90, "fwd7": fwd7, "sig": sig,
                               "regime": b["regime"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["wn"] = A["w"].str[1:].astype(int)
    A["net_all"] = (A["gain"] - A["fee"].shift(-1).fillna(0)).fillna(0)
    def book(mask):
        A["net"] = np.where(mask, A["net_all"], 0)
        P = A.groupby(["wn", "i"])["net"].mean().reset_index().sort_values(["wn", "i"])
        eq = (1 + P["net"]).cumprod()
        dd = (eq / eq.cummax() - 1)
        yr = eq.iloc[-1] ** (365 / len(P)) - 1
        sh = P["net"].mean() / P["net"].std() * np.sqrt(365)
        return pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(), "sharpe": sh,
                          "worst_window_ret": P.groupby("wn")["net"].apply(lambda x: (1+x).prod()-1).min()})
    reg = A["regime"] == "mean_reversion"
    res = {"all": book(np.ones(len(A), bool)), "regime_only": book(reg),
           "unknown_only": book(~reg)}
    out["variants"] = pd.DataFrame(res).T
    # in unknown bars held: what state? er recovered (trend) vs alignment broken
    H = A[(A["pos"].abs() > 1e-6) & ~reg].copy()
    H["er_hi"] = H["er"] >= 0.3
    out["unknown_held_by_er"] = H.groupby("er_hi")["gain"].agg(["mean", "count"])
    # grid check: holding beyond regime. forward 7d from bars that left regime vs bars in regime
    G = A[A["i"] % 7 == 0].dropna(subset=["fwd7", "er", "mv7"]).copy()
    drift = G.groupby("coin")["fwd7"].mean()
    G["ex"] = (G["fwd7"] - G["coin"].map(drift)) * np.sign(G["mv7"])
    G["agit"] = pd.qcut(G["vr"], 3, labels=False)
    def s(x):
        return pd.Series({"mean": x.mean(), "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan, "n": len(x)})
    out["sig_by_volratio_tercile"] = G[G["sig"]].groupby("agit")["ex"].apply(s).unstack()
    out["nosig_by_volratio_tercile"] = G[~G["sig"]].groupby("agit")["ex"].apply(s).unstack()
    # er grading inside signal
    G["erq"] = pd.qcut(G["er"], 3, labels=False)
    out["sig_by_er_tercile"] = G[G["sig"]].groupby("erq")["ex"].apply(s).unstack()
    out["mv7_abs_by_tercile_sig"] = G[G["sig"]].assign(q=pd.qcut(G.loc[G["sig"], "mv7"].abs(), 3, labels=False)).groupby("q")["ex"].apply(s).unstack()
    return out
