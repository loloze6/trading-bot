def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            H = c.rolling(30).max(); L = c.rolling(30).min()
            pos = (c - L) / (H - L)
            net = (c - c.shift(30)).abs()
            flat = 1 - net / (H - L)
            ret1d = c.pct_change()
            vol20 = ret1d.rolling(20).std()
            r5back = c / c.shift(5) - 1
            for h in (1, 5, 10, 20):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, pos=pos[i], flat=flat[i],
                                     fwd=fwd[i], vol=vol20[i], r5b=r5back[i],
                                     fc=df["forecast"].iloc[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["d"] = 2 * R["pos"] - 1
    R["side"] = np.sign(R["d"])
    R["cont"] = R["side"] * (R["fwd"] - R["drift"])  # continuation, unusual
    R = R.dropna(subset=["d", "flat", "fwd"])
    R = R[R["side"] != 0]
    # by horizon: continuation mean & t
    g = R.groupby("h")["cont"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["continuation_by_horizon"] = g
    R5 = R[R["h"] == 5].copy()
    R5["dist_q"] = pd.qcut(R5["d"].abs(), 5, labels=False)
    R5["flat_q"] = pd.qcut(R5["flat"], 3, labels=False)
    t = R5.groupby(["dist_q", "flat_q"])["cont"].agg(["mean", "count"])
    out["h5_cont_by_dist_x_flat"] = t
    for h in (5, 10, 20):
        Rh = R[R["h"] == h].copy()
        Rh["dist_q"] = pd.qcut(Rh["d"].abs(), 5, labels=False)
        a = Rh.groupby("dist_q")["cont"].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        out[f"h{h}_cont_by_dist"] = a
    # side: above vs below
    a = R5.groupby("side")["cont"].agg(["mean", "std", "count"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["h5_cont_by_side"] = a
    # continuation by year
    # by coin
    a = R5.groupby("coin")["cont"].agg(["mean", "count"])
    out["h5_cont_by_coin"] = a
    # by window
    a = R5.groupby("w")["cont"].mean()
    out["h5_cont_by_window"] = a
    # strength of continuation
    R5["usual"] = R5.groupby("coin")["fwd"].transform("std")
    out["h5_strength_cont_top2dist"] = float((R5.loc[R5["dist_q"] >= 3, "cont"] / R5.loc[R5["dist_q"] >= 3, "usual"]).mean())
    out["h5_total_cont_top2dist"] = float((R5.loc[R5["dist_q"] >= 3, "side"] * R5.loc[R5["dist_q"] >= 3, "fwd"]).mean())
    # book: daily returns split by held side
    br = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            b = bars[coin][w]
            b = b.assign(day=pd.to_datetime(b["timestamp"]).dt.floor("D"))
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            dd2 = dd.copy(); dd2["day"] = pd.to_datetime(dd2["day"]).dt.floor("D")
            dd2["al_prev"] = dd2["day"].map(al).shift(1)
            dd2["coin"] = coin; dd2["w"] = w
            dd2["year"] = dd2["day"].dt.year
            br.append(dd2)
    B = pd.concat(br).dropna(subset=["book_return", "al_prev"])
    B["held"] = np.where(B["al_prev"] > 0, "long", np.where(B["al_prev"] < 0, "short", "flat"))
    a = B.groupby("held")["book_return"].agg(["mean", "count", "sum"])
    out["book_daily_by_held_side"] = a
    out["book_daily_by_year"] = B.groupby("year")["book_return"].mean()
    out["mean_abs_alloc"] = float(B["al_prev"].abs().mean())
    return out
