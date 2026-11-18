def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    h = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            fwd = c.shift(-h) / c - 1
            ret5 = c / c.shift(5) - 1
            ret1 = c.pct_change()
            vr = np.log(v.rolling(5).mean() / v.rolling(30).mean())
            rv = ret1.rolling(20).std()
            rvr = np.log(ret1.rolling(5).std() / ret1.rolling(30).std())
            rng = ((b["high"] - b["low"]) / c).astype(float)
            rngr = np.log(rng.rolling(5).mean() / rng.rolling(30).mean())
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            idx = np.arange(len(b))
            g = (idx % h == 0)
            df = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "ret5": ret5, "ret1": ret1,
                               "vr": vr, "rv": rv, "rvr": rvr, "rngr": rngr, "wd": wd,
                               "fc": b["forecast"].astype(float), "reg": b["regime"],
                               "pos": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df[g])
    D = pd.concat(rows)
    D = D.dropna(subset=["fwd"])
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    D["absfwd"] = D["fwd"].abs()
    def grp(col, by, n=5, sub=None):
        S = D if sub is None else sub
        S = S.dropna(subset=[by, col])
        q = S.groupby("coin")[by].transform(lambda x: pd.qcut(x.rank(method="first"), n, labels=False))
        r = S.groupby(q)[col].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(5)
    down = D[D["ret5"] < 0]; up = D[D["ret5"] >= 0]
    out["down: ex by vr quintile"] = grp("ex", "vr", sub=down)
    out["up: ex by vr quintile"] = grp("ex", "vr", sub=up)
    out["all: ex by ret5 quintile"] = grp("ex", "ret5")
    out["all: absfwd by rngr quintile (compression)"] = grp("absfwd", "rngr")
    out["all: absfwd by vr quintile"] = grp("absfwd", "vr")
    out["all: ex by ret1 quintile"] = grp("ex", "ret1")
    out["all: ex by rv quintile"] = grp("ex", "rv")
    wdg = D.groupby("wd")["ex"].agg(["mean", "count", "std"]); wdg["t"] = wdg["mean"]/(wdg["std"]/np.sqrt(wdg["count"]))
    out["ex by weekday"] = wdg.round(5)
    # per coin slope t in down regime
    pc = {}
    for coin, s in down.dropna(subset=["vr"]).groupby("coin"):
        r = stats.linregress(s["vr"], s["ex"]); pc[coin] = (round(r.slope, 4), round(r.slope / r.stderr, 2), len(s))
    out["down per coin slope,t,n"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T
    pcu = {}
    for coin, s in up.dropna(subset=["vr"]).groupby("coin"):
        r = stats.linregress(s["vr"], s["ex"]); pcu[coin] = (round(r.slope, 4), round(r.slope / r.stderr, 2), len(s))
    out["up per coin slope,t,n"] = pd.DataFrame(pcu, index=["slope", "t", "n"]).T
    # book attribution
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(pd.DataFrame({"coin": coin, "win": w, "b": d["book_return"], "c": d["coin_return"]}))
    B = pd.concat(br)
    mc = B.groupby("coin")["c"].mean()
    out["book mean, coin mean by coin"] = B.groupby("coin")[["b", "c"]].mean().round(5)
    # positions on daily: approximate via bars last of day
    pos_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            p = b["postRebalance_current_allocation"].astype(float)
            pos_rows.append(pd.DataFrame({"coin": coin, "pos": p.values, "fc": b["forecast"].astype(float).values}))
    P = pd.concat(pos_rows)
    out["pos stats by coin"] = P.groupby("coin").agg(mean_pos=("pos", "mean"), share_short=("pos", lambda x: (x < 0).mean()), share_long=("pos", lambda x: (x > 0).mean())).round(3)
    mkt = (P.groupby("coin")["pos"].mean() * mc)
    out["market part per coin"] = mkt.round(6)
    out["market part overall"] = float(mkt.mean())
    out["book mean overall"] = float(B["b"].mean())
    return out
