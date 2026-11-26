def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            absmove = c.diff().abs().rolling(30).sum()
            er = (c - c.shift(30)).abs() / absmove
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            sd30 = r.rolling(30).std()
            mv7 = ret7 / (sd30 * np.sqrt(7))
            mv1 = r / sd30
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            sd_rel = sd30 / r.rolling(30).std().rolling(90, min_periods=30).mean()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "er": er, "ret30": ret30, "mv7": mv7, "mv1": mv1,
                               "fwd7": fwd7, "fwd1": fwd1, "sdrel": sd_rel,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "regime": b["regime"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    grid = D[D["pos"] % 7 == 0].dropna(subset=["fwd7", "mv7", "er", "ret30"]).copy()
    drift = grid.groupby("coin")["fwd7"].mean()
    grid["u7"] = grid["fwd7"] - grid["coin"].map(drift)
    grid["s"] = np.sign(grid["mv7"])
    grid["u7dir"] = grid["u7"] * grid["s"]
    grid["chop"] = np.where(grid["er"] < 0.3, "chop", "trend")
    grid["align"] = np.where(np.sign(grid["ret30"]) == grid["s"], "aligned", "against")
    grid["mvq"] = pd.qcut(grid["mv7"].abs(), 3, labels=["small", "mid", "large"])
    def agg(g):
        x = g["u7dir"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["fwd7 in mv7 direction by chop x align x size"] = grid.groupby(["chop", "align", "mvq"]).apply(agg)
    grid["volq"] = pd.qcut(grid["sdrel"], 3, labels=["calm", "mid", "agit"])
    out["fwd7 dir by chop x vol level"] = grid.groupby(["chop", "volq"]).apply(agg)
    # 30d momentum alone
    grid["s30"] = np.sign(grid["ret30"])
    grid["u30"] = grid["u7"] * grid["s30"]
    grid["erq"] = pd.qcut(grid["er"], 4, labels=["er1", "er2", "er3", "er4"])
    out["fwd7 in ret30 direction by ER quartile"] = grid.groupby("erq").apply(lambda g: pd.Series({"n": len(g), "mean": g["u30"].mean(), "t": g["u30"].mean() / (g["u30"].std() / np.sqrt(len(g)))}))
    # daily: weekday & after large 1d moves
    d1 = D.dropna(subset=["fwd1", "mv1"]).copy()
    d1["u1"] = d1["fwd1"] - d1["coin"].map(d1.groupby("coin")["fwd1"].mean())
    out["next-day return by weekday of signal bar"] = d1.groupby("wd")["u1"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    d1["mv1q"] = pd.qcut(d1["mv1"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["next-day ret by today's scaled move quintile"] = d1.groupby("mv1q")["u1"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # book: by window, by side
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; days.append(dd)
    Dy = pd.concat(days)
    out["book mean daily ret by window"] = Dy.groupby("w")[["book_return", "coin_return"]].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    out["regime share"] = D["regime"].value_counts(normalize=True)
    return out
