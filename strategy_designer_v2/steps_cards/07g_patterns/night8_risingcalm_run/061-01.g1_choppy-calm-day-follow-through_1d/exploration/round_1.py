import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = r1 / sd30
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            tr60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "z": z, "r1": r1, "fwd": fwd, "fwd1": fwd1, "tr60": tr60,
                "inprof": (b["regime"] == "unknown").values,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "rngz": rng / sd30, "clv": clv,
                "sd30": sd30,
            })
            df["sd_rel"] = df["sd30"] / df["sd30"].rolling(60, min_periods=30).median()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # coin mean 5-day return over grid
    G = A[(A["pos"] % H == 0) & A["fwd"].notna() & A["z"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    G["sex"] = np.sign(G["z"]) * G["ex"]
    def summ(g):
        n = len(g); m = g["sex"].mean(); s = g["sex"].std()
        return pd.Series({"n": n, "mean_signed_ex": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan,
                          "mean_ex": g["ex"].mean()})
    out = {}
    G["zbin"] = pd.cut(G["z"].abs(), [0, 0.5, 1, 1.5, 2, 3, 99])
    out["absz_bins_by_profile"] = G.groupby(["inprof", "zbin"], observed=True).apply(summ)
    G["trb"] = pd.cut(G["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    G["vb"] = np.where(G["sd_rel"] > 1, "agit", "calm")
    G["big"] = G["z"].abs() > 1.5
    out["big_day_by_trend_vol"] = G[G["big"]].groupby(["trb", "vb", np.sign(G["z"])], observed=True).apply(summ)
    # slope ex on z by profile
    res = {}
    for k, g in G.groupby("inprof"):
        sl = stats.linregress(g["z"], g["ex"]); res[str(k)] = [len(g), sl.slope, sl.slope / sl.stderr]
    out["slope_ex_on_z_by_inprof"] = pd.DataFrame(res, index=["n", "slope", "t"]).T
    # up vs down big days, all bars
    out["sign_z_big_all"] = G[G["big"]].groupby(np.sign(G["z"])).apply(summ)
    # range & close location: wide range days
    G["rbin"] = pd.qcut(G["rngz"], 5, duplicates="drop")
    G["cb"] = pd.cut(G["clv"], [-0.01, 0.25, 0.75, 1.01], labels=["low", "mid", "high"])
    out["rng_quint_closeloc_fwd_ex"] = G.groupby(["rbin", "cb"], observed=True)["ex"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # weekday: next-day return ex
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out["weekday_next1"] = A.groupby("wd")["ex1"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # book: days in position, long vs short
    pos = A[A["alloc"].abs() > 0]
    pos = pos.assign(g=pos["alloc"] * pos["fwd1"], side=np.sign(pos["alloc"]))
    out["book_gain_by_side"] = pos.groupby("side")["g"].agg(["count", "mean", "sum"])
    # book daily returns largest moves
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"n": len(bk), "mean": bk.mean(), "sd": bk.std(),
                                   "top10_sum": bk.nlargest(10).sum(), "bot10_sum": bk.nsmallest(10).sum()})
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "sum"])
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["dur_d"], [0, 5, 6, 10, 30, 999])
    out["trades_by_side_dur"] = T.groupby(["side", "db"], observed=True)["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    return out
