def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        parts = []
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"]; v = d["volume"]
            d["win"] = w
            d["r1"] = c.pct_change()
            d["r6"] = c / c.shift(6) - 1
            d["f18"] = c.shift(-18) / c - 1
            d["f6"] = c.shift(-6) / c - 1
            vm = v.shift(1).rolling(180, min_periods=60).mean()
            d["vr1"] = v / vm
            d["vr6"] = v.rolling(6).mean() / v.shift(6).rolling(180, min_periods=60).mean()
            d["sd1"] = d["r1"].shift(1).rolling(180, min_periods=60).std()
            s = np.sign(d["r1"]).fillna(0)
            grp = (s != s.shift()).cumsum()
            d["run"] = s.groupby(grp).cumcount().add(1) * s
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["pos"] = np.arange(len(d))
            d["alloc"] = d["postRebalance_current_allocation"]
            parts.append(d)
        a = pd.concat(parts)
        g = a[a["pos"] % 18 == 0].dropna(subset=["f18"])
        mu, sd = g["f18"].mean(), g["f18"].std()
        g6 = a[a["pos"] % 6 == 0].dropna(subset=["f6"])
        mu6, sd6 = g6["f6"].mean(), g6["f6"].std()
        a["coin"] = coin
        a["z"] = (a["f18"] - mu) / sd
        a["ex"] = a["f18"] - mu
        a["z6"] = (a["f6"] - mu6) / sd6
        a["r1n"] = a["r1"] / a["sd1"]
        a["r6n"] = a["r6"] / (a["sd1"] * np.sqrt(6))
        rows.append(a)
    A = pd.concat(rows)
    G = A[A["pos"] % 18 == 0].dropna(subset=["z", "vr1", "r1n"]).copy()
    out = {}
    def tab(df, key, col="z"):
        t = df.groupby(key)[col].agg(["mean", "std", "count"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std").round(3)
    # graded: volume on down vs up bars
    G["lvr"] = np.log(G["vr1"])
    G["vq"] = pd.qcut(G["lvr"], 5, labels=False)
    G["dn"] = np.where(G["r1n"] < 0, "down", "up")
    G["rq"] = pd.qcut(G["r1n"], 3, labels=False)
    out["vr1 quintile x bar tercile (z18)"] = tab(G, ["vq", "rq"])
    # regression z ~ lvr, lvr*downbar_size
    G["dsz"] = (-G["r1n"]).clip(lower=0)
    G["inter"] = G["lvr"].clip(lower=0) * G["dsz"]
    X = np.column_stack([np.ones(len(G)), G["lvr"], G["r1n"], G["inter"]])
    b, *_ = np.linalg.lstsq(X, G["z"].values, rcond=None)
    res = G["z"].values - X @ b
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=4)
    out["regression z18 on lvr, r1n, lvr+*down"] = pd.DataFrame({"coef": b, "t": b / np.sqrt(np.diag(cov))}, index=["const", "lvr", "r1n", "inter"]).round(3)
    # 1-day (6-bar) volume and 1-day return
    G6 = A[A["pos"] % 6 == 0].dropna(subset=["z6", "vr6", "r6n"]).copy()
    G6["vq"] = pd.qcut(np.log(G6["vr6"]), 4, labels=False)
    G6["rq"] = pd.qcut(G6["r6n"], 3, labels=False)
    out["1d volume quartile x 1d return tercile (z6, next day)"] = tab(G6, ["vq", "rq"], "z6")
    Gs = G.dropna(subset=["r6n", "vr6"]).copy()
    Gs["vq"] = pd.qcut(np.log(Gs["vr6"]), 4, labels=False)
    Gs["rq"] = pd.qcut(Gs["r6n"], 3, labels=False)
    out["1d volume quartile x 1d return tercile (z18)"] = tab(Gs, ["vq", "rq"])
    # stability: high vol & down 1d return, by year
    sub = Gs[(Gs["vq"] == 3) & (Gs["rq"] == 0)]
    out["top vol, bottom 1d return, by year (z18)"] = tab(sub, "year")
    out["top vol, bottom 1d return, by coin (z18)"] = tab(sub, "coin")
    # book: positions vs signal
    B = A.dropna(subset=["alloc"])
    out["mean alloc and share in market"] = pd.Series({"mean_alloc": B["alloc"].mean(), "share_nonzero": (B["alloc"].abs() > 1e-6).mean()}).round(4)
    # book days: largest losses
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            D.append(df.assign(coin=coin, win=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["coin_return"], 5, labels=False)
    t = D.groupby("bq")[["book_return", "coin_return"]].mean() * 100
    out["book vs coin daily by coin-return quintile pct"] = t.round(3)
    return out
