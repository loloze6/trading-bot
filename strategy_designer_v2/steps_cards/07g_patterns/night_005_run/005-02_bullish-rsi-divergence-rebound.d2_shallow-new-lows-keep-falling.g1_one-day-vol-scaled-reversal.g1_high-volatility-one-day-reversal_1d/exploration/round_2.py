import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol
            nxt = c.shift(-1) / c - 1
            r3 = c / c.shift(3) - 1
            ts = pd.to_datetime(b["timestamp"])
            rng = (b["high"] - b["low"]) / c
            d = pd.DataFrame({"coin": coin, "w": w, "r": r, "z": z, "vol": vol, "nxt": nxt, "r3": r3,
                              "rng": rng, "f": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "rvs": b["sizing_realised_vol"], "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "fade": b.get("debug_info.components.fade.post_pipeline_value"),
                              "lv": b.get("debug_info.components.lowvol_move.post_pipeline_value")})
            rows.append(d)
    D = pd.concat(rows)
    D["ex"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    E = D.dropna(subset=["z", "ex"]).copy()
    # vol level: rank of 20d vol pooled per coin (exploratory)
    E["vq"] = E.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    E["zq"] = pd.qcut(E["z"], 5, labels=False)
    out["n_E"] = len(E)
    out["ex_bps_zq_x_volq"] = (E.pivot_table(index="zq", columns="vq", values="ex", aggfunc="mean") * 1e4).round(1)
    res = []
    groups = [("all", E)] + [(f"coin {k}", g) for k, g in E.groupby("coin")] + [(f"vq {k}", g) for k, g in E.groupby("vq")] \
        + [(f"yr {k}", g) for k, g in E.groupby("yr")] + [("z<0", E[E.z < 0]), ("z>0", E[E.z > 0])]
    for name, g in groups:
        s = stats.linregress(g["z"], g["ex"])
        res.append({"grp": name, "slope_bps": s.slope * 1e4, "t": s.slope / s.stderr, "n": len(g)})
    out["slope_ex_on_z"] = pd.DataFrame(res).round(2)
    # 3-day return, range as predictors of next day
    rr = []
    for x in ["r3", "rng", "f"]:
        g = E.dropna(subset=[x])
        s = stats.linregress(g[x], g["ex"]); rr.append({"x": x, "slope": s.slope, "t": s.slope / s.stderr, "n": len(g)})
    out["other_1d_slopes"] = pd.DataFrame(rr).round(4)
    # next-day return by weekday of the next day, per coin
    E["wdn"] = (E["wd"] + 1) % 7
    wt = E.groupby(["wdn"])["nxt"].agg(["mean", "std", "count"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["ret_by_weekday_of_return_day"] = wt.round(5)
    wc = E.groupby(["coin", "wdn"])["nxt"].mean().unstack().mul(1e4).round(1)
    out["ret_bps_coin_x_weekday"] = wc
    yr = E[E.wdn.isin([2, 5])].groupby("yr")["nxt"].mean().mul(1e4).round(1)
    out["tue_fri_ret_bps_by_year"] = yr
    # book: days data, big loss / gain days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            x["prev_coin"] = x["coin_return"].shift(1); x["next_coin"] = x["coin_return"].shift(-1)
            dd.append(x)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    q = DD["book_return"].quantile([0.05, 0.95])
    lo = DD[DD.book_return <= q.iloc[0]]; hi = DD[DD.book_return >= q.iloc[1]]
    out["extreme_book_days"] = pd.DataFrame({
        "n": [len(lo), len(hi)],
        "prev_coin_bps": [lo.prev_coin.mean() * 1e4, hi.prev_coin.mean() * 1e4],
        "same_coin_bps": [lo.coin_return.mean() * 1e4, hi.coin_return.mean() * 1e4],
        "next_coin_bps": [lo.next_coin.mean() * 1e4, hi.next_coin.mean() * 1e4]}, index=["worst5%", "best5%"]).round(1)
    return out
