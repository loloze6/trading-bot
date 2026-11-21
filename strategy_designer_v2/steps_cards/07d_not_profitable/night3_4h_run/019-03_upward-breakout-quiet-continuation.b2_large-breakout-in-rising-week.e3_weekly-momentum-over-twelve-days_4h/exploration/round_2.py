def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    B = []
    for c in bars:
        for w, b in bars[c].items():
            x = b[["timestamp", "close", "postRebalance_current_allocation", "forecast"]].copy().reset_index(drop=True)
            x["nxt"] = x.close.pct_change().shift(-1)
            a = x.postRebalance_current_allocation
            x["g_all"] = a * x.nxt
            x["g_long"] = a.clip(lower=0) * x.nxt
            x["g_short"] = a.clip(upper=0) * x.nxt
            x["ret180"] = x.close / x.close.shift(180) - 1
            x["g_trend"] = np.where(np.sign(a) == np.sign(x.ret180), a, 0) * x.nxt
            lr = np.log(x.close).diff()
            x["vr"] = lr.rolling(20).std() / lr.rolling(180).std()
            x["day"] = pd.to_datetime(x.timestamp).dt.floor("D")
            x["coin"] = c; x["window"] = w
            B.append(x)
    B = pd.concat(B, ignore_index=True).dropna(subset=["nxt"])
    # daily approx: sum of bar gains per coin-day (log-ish), then mean over coins
    cols = ["g_all", "g_long", "g_short", "g_trend"]
    Dc = B.groupby(["coin", "window", "day"])[cols].sum().reset_index()
    P = Dc.groupby(["window", "day"])[cols].mean().reset_index()
    P["wn"] = P.window.str[1:].astype(int)
    P = P.sort_values(["wn", "day"])
    def summ(s):
        eq = (1 + s).cumprod().values
        dd = (eq / np.maximum.accumulate(eq) - 1).min()
        yr = eq[-1] ** (365 / len(s)) - 1
        return pd.Series({"mean": s.mean(), "sharpe": s.mean() / s.std() * np.sqrt(365), "maxdd": dd, "calmar": yr / -dd})
    out["variants"] = pd.DataFrame({k: summ(P[k]) for k in cols}).T
    pw = P.groupby("wn")[["g_all", "g_long", "g_short"]].sum()
    out["window_by_side"] = pw.loc[10:18].round(3)
    # long side graded by vol ratio and trend
    L = B[B.postRebalance_current_allocation > 0].dropna(subset=["vr", "ret180"]).copy()
    L["vq"] = pd.qcut(L.vr, 3, labels=["quiet", "mid", "loud"])
    L["tr"] = np.where(L.ret180 > 0, "up30d", "down30d")
    out["long_gain_by_state"] = L.groupby(["tr", "vq"]).g_all.agg(["size", "mean"])
    S = B[B.postRebalance_current_allocation < 0].dropna(subset=["vr", "ret180"]).copy()
    S["tq"] = pd.qcut(S.ret180, 4, labels=False)
    out["short_gain_by_ret30_q"] = S.groupby("tq").agg(n=("g_all", "size"), mean=("g_all", "mean"), r30=("ret180", "mean"))
    return out
