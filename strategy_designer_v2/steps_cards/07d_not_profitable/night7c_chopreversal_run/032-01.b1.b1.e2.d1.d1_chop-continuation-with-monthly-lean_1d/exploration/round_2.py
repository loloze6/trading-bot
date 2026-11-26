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
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            ret90 = c / c.shift(90) - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            v = b["postRebalance_total_value"]
            br = v / v.shift(1) - 1
            fee = (pos - pos.shift(1).fillna(0)).abs() * 0.0019 / 2
            gain = pos * (c.shift(-1) / c - 1)
            fwd7 = c.shift(-7) / c - 1
            mv7 = ret7 / (vol30 * np.sqrt(7))
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "pos": pos,
                               "br": br, "gain": gain, "fee": fee, "er": er, "ret30": ret30,
                               "ret7": ret7, "ret90": ret90, "vol30": vol30, "mv7": mv7,
                               "fwd7": fwd7, "fc": b["forecast"], "regime": b["regime"]})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["wn"] = A["w"].str[1:].astype(int)
    A["side"] = np.sign(A["pos"])

    def book(g):
        P = g.groupby(["wn", "i"])["net"].mean().reset_index().sort_values(["wn", "i"])
        eq = (1 + P["net"]).cumprod()
        dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(P)) - 1
        sh = P["net"].mean() / P["net"].std() * np.sqrt(365)
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": sh})

    A["net_all"] = (A["gain"] - A["fee"].shift(-1).fillna(0)).fillna(0)
    res = {}
    A["net"] = A["net_all"]; res["as_is_approx"] = book(A)
    A["net"] = np.where(A["pos"] > 0, A["net_all"], 0); res["long_only"] = book(A)
    A["net"] = np.where(A["pos"] < 0, A["net_all"], 0); res["short_only"] = book(A)
    A["net"] = np.where((A["pos"] > 0) | ((A["pos"] < 0) & (A["ret90"] < 0)), A["net_all"], 0); res["short_only_if_ret90neg"] = book(A)
    A["net"] = np.where(A["regime"] == "mean_reversion", A["net_all"], 0); res["regime_bars_only"] = book(A)
    out["book_variants"] = pd.DataFrame(res).T

    # deepest falls of actual book: what was held
    P = A.groupby(["wn", "i"])["br"].mean().reset_index().sort_values(["wn", "i"])
    eq = (1 + P["br"].fillna(0)).cumprod()
    P["dd"] = (eq / eq.cummax() - 1).values
    P["indd"] = P["dd"] < -0.10
    M = A.merge(P[["wn", "i", "indd"]], on=["wn", "i"])
    H = M[M["pos"].abs() > 1e-6]
    out["gain_in_deep_dd_by_side"] = H.groupby(["indd", "side"])["gain"].agg(["mean", "count"])
    out["gain_by_side_regime"] = H.groupby(["side", "regime"])["gain"].agg(["mean", "count"])

    # non-overlapping 7-day grid: cases and condition checks
    G = A[A["i"] % 7 == 0].dropna(subset=["fwd7", "er", "ret30", "mv7"]).copy()
    drift = G.groupby("coin")["fwd7"].mean()
    G["ex"] = G["fwd7"] - G["coin"].map(drift)
    sig_long = (G["er"] < 0.3) & (G["ret30"] > 0) & (G["mv7"] > 0)
    sig_short = (G["er"] < 0.3) & (G["ret30"] < 0) & (G["mv7"] < 0)
    def s(x):
        return pd.Series({"mean": x.mean(), "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan, "n": len(x)})
    tab = {}
    tab["long_signal_ex"] = s(G.loc[sig_long, "ex"])
    tab["short_signal_ex_short_dir"] = s(-G.loc[sig_short, "ex"])
    up90 = G["ret90"] > 0
    tab["short_signal_ret90neg"] = s(-G.loc[sig_short & ~up90, "ex"])
    tab["short_signal_ret90pos"] = s(-G.loc[sig_short & up90, "ex"])
    tab["long_signal_ret90pos"] = s(G.loc[sig_long & up90, "ex"])
    tab["long_signal_ret90neg"] = s(G.loc[sig_long & ~up90, "ex"])
    tab["ret90neg_nosignal_short_dir"] = s(-G.loc[~sig_short & ~sig_long & ~up90, "ex"])
    tab["ret90pos_nosignal_long_dir"] = s(G.loc[~sig_short & ~sig_long & up90, "ex"])
    out["grid_cases"] = pd.DataFrame(tab).T
    # graded check within long signal
    L = G[sig_long].copy()
    L["q"] = pd.qcut(L["mv7"], 3, labels=False)
    out["long_by_mv7_tercile"] = L.groupby("q")["ex"].agg(["mean", "count"])
    S = G[sig_short].copy()
    S["q"] = pd.qcut(-S["mv7"], 3, labels=False)
    out["short_by_mv7_tercile_shortdir"] = (-S["ex"]).groupby(S["q"]).agg(["mean", "count"])
    return out
