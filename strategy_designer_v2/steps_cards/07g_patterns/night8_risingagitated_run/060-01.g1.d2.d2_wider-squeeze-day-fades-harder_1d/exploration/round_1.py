import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 25: continue
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            cl = (c - l) / rng.replace(0, np.nan)
            rr = rng / rng.rolling(20, min_periods=20).mean()
            r1 = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            t20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            fa = b["regime"].isin(["mean_reversion", "unknown"])
            df = pd.DataFrame({"coin": coin, "win": w, "cl": cl, "rr": rr, "r1": r1, "z1": r1 / vol20,
                               "nxt": nxt, "nxt2": nxt2, "fa": fa, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "t20": t20, "pos": b["postRebalance_current_allocation"], "day": ts.dt.floor("D"),
                               "oc": (c - o) / rng.replace(0, np.nan)})
            rows.append(df)
    P = pd.concat(rows, ignore_index=True)
    drift = P.groupby("coin")["nxt"].mean()
    P["u"] = P["nxt"] - P["coin"].map(drift)

    def tstat(s, d):
        g = pd.DataFrame({"s": s, "d": d}).dropna().groupby("d")["s"].sum()
        x = pd.DataFrame({"s": s, "d": d}).dropna()
        n = len(x)
        if n < 10: return np.nan
        m = x["s"].mean()
        G = len(g)
        se = np.sqrt((((g - g.index.map(lambda _: 0)) - x.groupby("d").size() * m) ** 2).sum() * G / (G - 1)) / n
        return m / se

    def tab(mask, col, bins, labels=None):
        Q = P[mask].dropna(subset=[col, "u"]).copy()
        Q["b"] = pd.cut(Q[col], bins, labels=labels) if not isinstance(bins, str) else Q[col]
        out = []
        for k, g in Q.groupby("b", observed=True):
            out.append({"bin": str(k), "n": len(g), "mean_u%": 100 * g["u"].mean(), "t_day": tstat(g["u"], g["day"])})
        return pd.DataFrame(out)

    res = {}
    res["profile_share"] = P["fa"].mean()
    clb = [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01]
    res["FA_by_close_loc"] = tab(P["fa"], "cl", clb)
    res["notFA_by_close_loc"] = tab(~P["fa"], "cl", clb)
    rrb = [0, 0.6, 0.9, 1.2, 1.6, 10]
    res["FA_highclose_by_rr"] = tab(P["fa"] & (P["cl"] > 0.5), "rr", rrb)
    res["FA_lowclose_by_rr"] = tab(P["fa"] & (P["cl"] <= 0.5), "rr", rrb)
    res["notFA_highclose_by_rr"] = tab(~P["fa"] & (P["cl"] > 0.5), "rr", rrb)
    zb = [-50, -2, -1, 0, 1, 2, 50]
    res["FA_by_z1"] = tab(P["fa"], "z1", zb)
    res["notFA_by_z1"] = tab(~P["fa"], "z1", zb)
    res["FA_by_weekday"] = tab(P["fa"], "wd", "wd")
    res["all_by_weekday"] = tab(P["fa"] | ~P["fa"], "wd", "wd")
    res["FA_by_year"] = tab(P["fa"] & (P["cl"] > 0.5), "yr", "yr")
    res["notFA_by_20d_trend"] = tab(~P["fa"], "t20", [-5, -0.2, -0.1, 0, 0.1, 0.2, 50])
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby("day")["book_return"].mean().dropna()
    res["book_mean_std"] = pd.Series({"mean%": 100 * bk.mean(), "std%": 100 * bk.std(), "n": len(bk)})
    q = bk.quantile([0.02, 0.98])
    big = P.groupby("day")["r1"].mean()
    res["coin_ret_on_book_extremes"] = pd.Series({
        "coin_r_on_top2%": 100 * big.reindex(bk[bk >= q.iloc[1]].index).mean(),
        "coin_r_on_bot2%": 100 * big.reindex(bk[bk <= q.iloc[0]].index).mean()})
    return res
