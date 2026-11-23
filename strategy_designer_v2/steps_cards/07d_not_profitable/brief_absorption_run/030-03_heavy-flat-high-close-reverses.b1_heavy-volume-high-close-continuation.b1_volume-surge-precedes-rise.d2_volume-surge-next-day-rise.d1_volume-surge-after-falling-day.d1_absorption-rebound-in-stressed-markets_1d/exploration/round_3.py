def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["coin"] = coin; b["wn"] = int(w[1:])
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            lr = np.log(b["close"]).diff()
            b["vr"] = lr.rolling(20).std() / lr.rolling(120, min_periods=40).std()
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            b["clv"] = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["prevsig"] = (b["forecast"].shift(1) > 0)
            b["al"] = b["postRebalance_current_allocation"].fillna(0)
            b["turn"] = (b["al"] - b["al"].shift(1).fillna(0)).abs()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(mu)
    B["fpos"] = B["forecast"] > 0
    cost = 0.0019 / 2
    def book(mask, scale=None):
        a = B["al"].where(mask, 0.0)
        if scale is not None:
            a = a * scale
        g = (a * B["r1"]).fillna(0)
        # approximate fee on turnover of the modified allocation
        prev = a.groupby([B["coin"], B["wn"]]).shift(1).fillna(0)
        g = g - (a - prev).abs() * cost
        P = pd.DataFrame({"wn": B["wn"], "day": B["day"], "g": g}).groupby(["wn", "day"])["g"].mean().sort_index()
        v = (1 + P).cumprod(); dd = float((v / v.cummax() - 1).min())
        yr = float(v.iloc[-1] ** (365 / len(P)) - 1)
        sh = float(P.mean() / P.std() * np.sqrt(365))
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd if dd < 0 else np.nan, "sharpe": sh, "held_share": float((a.abs() > 1e-6).mean())})
    allm = pd.Series(True, index=B.index)
    res = {}
    res["as tested"] = book(allm)
    res["vr>=0.75"] = book(B["vr"].fillna(0) >= 0.75)
    res["clv<=0.4 (low close)"] = book(B["clv"].fillna(1) <= 0.4)
    res["clv scaled 1-clv"] = book(allm, (1 - B["clv"].fillna(0.5)) * 1.5)
    res["not first signal"] = book(B["prevsig"])
    res["low close & vr>=0.75"] = book((B["clv"].fillna(1) <= 0.4) & (B["vr"].fillna(0) >= 0.75))
    out["proxy books"] = pd.DataFrame(res).T
    # condition alone: close location on non-signal (up/flat) days
    S = B[B["fpos"]].dropna(subset=["clv", "ex"])
    cuts = list(S["clv"].quantile([1/3, 2/3]))
    NS = B[~B["fpos"]].dropna(subset=["clv", "ex"]).copy()
    NS["q"] = pd.cut(NS["clv"], [-np.inf] + cuts + [np.inf], labels=False)
    out["nonsignal days by signal clv bins"] = NS.groupby("q").agg(n=("ex", "size"), clv=("clv", "mean"), ex=("ex", "mean"))
    # low-close signals: t, and by window halves
    Sc = S.copy(); Sc["low"] = Sc["clv"] <= cuts[0]
    from scipy import stats
    a = Sc.loc[Sc["low"], "ex"]; b_ = Sc.loc[~Sc["low"], "ex"]
    out["low close minus rest"] = pd.Series({"low_mean": a.mean(), "rest_mean": b_.mean(), "n_low": len(a), "n_rest": len(b_), "welch_t": stats.ttest_ind(a, b_, equal_var=False).statistic})
    Sc["half"] = np.where(Sc["wn"] <= 12, "w1-w12", "w13-w24")
    out["low close by half"] = Sc.groupby(["half", "low"])["ex"].agg(["size", "mean"])
    # episode w16: clv of signals
    E = B[(B["wn"] == 16) & B["fpos"]]
    out["w16 signals by clv"] = E.dropna(subset=["clv"]).assign(low=lambda x: x["clv"] <= cuts[0]).groupby("low").agg(n=("r1", "size"), r1=("r1", "mean"), alloc=("al", "mean"))
    return out
