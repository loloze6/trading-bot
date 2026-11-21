def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    dayrows = []
    for coin, wins in data["bars"].items():
        grid_all = []
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            df = pd.DataFrame({
                "fwd": fwd,
                "past10": c / c.shift(10) - 1,
                "past30": c / c.shift(30) - 1,
                "vol20": r1.rolling(20).std(),
                "rng": (b["high"] - b["low"]) / c,
                "lastday": r1,
                "fc": b["forecast"].astype(float),
                "raw": b.get("debug_info.components.support_above.last_history_value", pd.Series(np.nan, index=b.index)).astype(float),
                "dist_hi30": c / c.rolling(30).max() - 1,
                "dist_lo30": c / c.rolling(30).min() - 1,
                "vchg": b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean(),
            })
            g = df.iloc[::H].copy()
            g = g[g["fwd"].notna()]
            g["coin"] = coin
            per.append(g)
            ts = pd.to_datetime(b["timestamp"])
            dayrows.append(pd.DataFrame({"wd": ts.dt.weekday, "r": r1, "coin": coin}))
        if not per:
            continue
        G = pd.concat(per)
        mu, sd = G["fwd"].mean(), G["fwd"].std()
        G["z"] = (G["fwd"] - mu) / sd
        G["unus"] = G["fwd"] - mu
        # rank features within coin
        for f in ["past10", "past30", "vol20", "rng", "lastday", "dist_hi30", "dist_lo30", "vchg"]:
            G["q_" + f] = pd.qcut(G[f].rank(method="first"), 5, labels=False) if G[f].notna().sum() > 20 else np.nan
        rows.append(G)
    A = pd.concat(rows)
    out = {}
    def tab(col):
        r = A.groupby(col)["z"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["unus_mean"] = A.groupby(col)["unus"].mean()
        r["raw_mean"] = A.groupby(col)["fwd"].mean()
        return r.drop(columns="std").round(4)
    for f in ["past10", "past30", "vol20", "rng", "lastday", "dist_hi30", "dist_lo30", "vchg"]:
        out["q_" + f] = tab("q_" + f)
    A["fside"] = np.where(A["fc"] < 0, "short", np.where(A["fc"] > 0, "long", "flat"))
    out["by_forecast_side"] = tab("fside")
    s = A[A["fc"] < 0].copy()
    s["fq"] = pd.qcut(s["fc"].rank(method="first"), 5, labels=False)
    out["short_by_fc_quintile(0=most short)"] = tab_s = s.groupby("fq").agg(z=("z", "mean"), n=("z", "count"), raw=("fwd", "mean"))
    D = pd.concat(dayrows).dropna()
    wd = D.groupby("wd")["r"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_daily"] = wd.drop(columns="std")
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d[["book_return", "coin_return"]].assign(coin=coin, w=w))
    B = pd.concat(bk).dropna()
    out["book_mean_daily"] = B["book_return"].mean()
    out["coin_mean_daily"] = B["coin_return"].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
