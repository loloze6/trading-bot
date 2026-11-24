def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    drift = {}
    out = {}
    # coin drift on 2-bar grid and daily mean
    dmean = {}
    for c, ws in bars.items():
        r2 = []; r1 = []
        for w, b in ws.items():
            cl = b["close"].values
            g = cl[::2]
            r2 += list(g[1:] / g[:-1] - 1)
            r1 += list(cl[1:] / cl[:-1] - 1)
        drift[c] = np.mean(r2); dmean[c] = np.mean(r1)
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]
            d = pd.DataFrame({
                "coin": c, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                "day": ts.dt.normalize(),
                "r14": cl / cl.shift(14) - 1,
                "r7": cl / cl.shift(7) - 1,
                "fwd2": cl.shift(-2) / cl - 1,
                "fwd1": cl.shift(-1) / cl - 1,
                "near": b.get("debug_info.components.near_high.last_history_value"),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
            })
            d["ex2"] = d["fwd2"] - drift[c]
            d["ex1"] = d["fwd1"] - drift[c] / 2
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)

    def ct(s, dcol):
        x = pd.DataFrame({"v": s, "d": dcol}).dropna()
        if len(x) < 5: return (np.nan, np.nan, len(x), 0)
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return (m, m / se, len(x), G)

    def tab(df, key, col="ex2"):
        res = {}
        for k, gdf in df.groupby(key):
            m, t, n, G = ct(gdf[col], gdf["day"])
            res[k] = {"mean_ex": m, "t_dayclust": t, "n": n, "days": G}
        return pd.DataFrame(res).T

    # weekend excess by weekday (every weekday, any r14), and by r14 sign
    A["up14"] = np.where(A["r14"] > 0, "up", "down")
    out["ex2_by_weekday_all"] = tab(A.dropna(subset=["fwd2"]), "wd")
    fri = A[(A["wd"] == 4)].dropna(subset=["fwd2", "r14"])
    out["fri_by_r14sign"] = tab(fri, "up14")
    nonfri_up = A[(A["wd"] != 4) & (A["r14"] > 0)].dropna(subset=["fwd2"])
    out["nonfri_up14_ex2"] = pd.DataFrame([ct(nonfri_up["ex2"], nonfri_up["day"])], columns=["m","t","n","days"])
    # graded by r14 quintile among Fridays (all)
    fri = fri.copy()
    fri["r14q"] = pd.qcut(fri["r14"], 5, labels=False)
    out["fri_by_r14_quintile"] = tab(fri, "r14q")
    fri["r7q"] = pd.qcut(fri["r7"], 5, labels=False)
    out["fri_by_r7_quintile"] = tab(fri, "r7q")
    # cases: Fridays up14 with near value
    cs = fri[(fri["r14"] > 0)].dropna(subset=["near"]).copy()
    cs["nq"] = pd.qcut(cs["near"].rank(method="first"), 5, labels=False)
    out["cases_by_nearness_quintile"] = tab(cs, "nq")
    out["cases_by_coin"] = tab(cs, "coin")
    out["cases_by_year"] = tab(cs, "year")
    # Saturday vs Sunday split
    out["cases_sat_only_ex1"] = pd.DataFrame([ct(cs["ex1"], cs["day"])], columns=["m","t","n","days"])
    sat = A[(A["wd"] == 5)].copy()
    # Saturday bars following a case Friday: their fwd1 = Sunday
    # market share of book
    held = A.dropna(subset=["alloc"])
    mk = (held["alloc"] * held["coin"].map(dmean)).mean()
    book = held["alloc"] * held["fwd1"]
    out["book_bar_mean_gain"] = float(book.mean())
    out["book_bar_market_part"] = float(mk)
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c, ws in trades.items() for w, t in ws.items()], ignore_index=True)
    p = T["net_profit_loss_percent"]
    out["trades_n_mean_t"] = pd.Series({"n": len(p), "mean": p.mean(), "t": p.mean()/(p.std()/np.sqrt(len(p))),
        "share_pos": (p > 0).mean(), "sum_top10_over_total": p.nlargest(10).sum()/p.sum(),
        "median": p.median()})
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"])
    return out
