def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            b["ret1"] = c.shift(-1) / c - 1
            b["r0"] = c / c.shift(1) - 1
            b["r20"] = c / c.shift(20) - 1
            b["vol20"] = b["r0"].rolling(20).std()
            b["volrel"] = b["vol20"] / b["r0"].rolling(120, min_periods=60).std()
            b["pos"] = b["postRebalance_current_allocation"]
            b["chg"] = (b["pos"] - b["pos"].shift(1).fillna(b["previous_allocation"].iloc[0])).abs()
            b["coin"] = coin; b["win"] = w
            b["wn"] = int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["drift"] = B["coin"].map(B.groupby("coin")["r0"].mean())
    B["ex1"] = B["ret1"] - B["drift"]
    B["sig"] = B["forecast"] > 0
    Y = B[B.ret1.notna() & B.volrel.notna()].copy()
    Y["vq"] = pd.qcut(Y["volrel"], 3, labels=["calm", "mid", "wild"])
    g = Y.groupby(["vq", "sig"])["ex1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["ex1_by_volrel_sig"] = g
    S = Y[Y.sig].copy()
    S["fh"] = S.groupby("vq")["forecast"].transform(lambda x: x > x.median())
    out["ex1_sig_vq_forecasthalf"] = S.groupby(["vq", "fh"])["ex1"].agg(["mean", "count"])
    # wild-state signal vs wild nonsignal welch
    a = Y[(Y.vq == "wild") & Y.sig]["ex1"]; bb = Y[(Y.vq == "wild") & ~Y.sig]["ex1"]
    out["wild_sig_minus_nosig_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)
    a = Y[(Y.vq == "calm") & Y.sig]["ex1"]; bb = Y[(Y.vq == "calm") & ~Y.sig]["ex1"]
    out["calm_sig_minus_nosig_t"] = float(stats.ttest_ind(a, bb, equal_var=False).statistic)

    # approximate books: daily = mean over coins of pos*ret1 - cost*chg
    cost = 0.0019 / 2
    def book(mask):
        Z = B.copy()
        Z["p"] = np.where(mask, Z["pos"], 0.0)
        Z["pc"] = Z.groupby(["coin", "win"])["p"].diff().abs().fillna(Z["p"].abs())
        Z["g"] = Z["p"] * Z["ret1"].fillna(0) - cost * Z["pc"]
        P = Z.groupby(["wn", "day"])["g"].mean().reset_index().sort_values(["wn", "day"])
        r = P["g"].values
        v = np.cumprod(1 + r)
        dd = (v / np.maximum.accumulate(v) - 1).min()
        yr = v[-1] ** (365 / len(r)) - 1
        return pd.Series({"sharpe": r.mean() / r.std(ddof=1) * np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr / -dd, "share_in": float((Z["p"].abs() > 1e-9).mean())})
    vr = B["volrel"]
    q1, q2 = Y["volrel"].quantile([1/3, 2/3])
    res = {"as_is": book(np.ones(len(B), bool)),
           "out_calm": book(~(vr < q1)),
           "wild_only": book(vr >= q2),
           "out_r20_q2": book(~((B.r20 > Y.r20.quantile(0.25)) & (B.r20 <= Y.r20.quantile(0.5))))}
    out["books"] = pd.DataFrame(res).T
    # deepest fall window w9 / w8: state of held bars
    F = Y[Y.win.isin(["w8", "w9"]) & (Y.pos.abs() > 1e-9)]
    out["fall_wins_gain_by_vq"] = F.groupby("vq").apply(lambda x: pd.Series({"sum": (x.pos * x.ret1).sum(), "n": len(x)}))
    return out
