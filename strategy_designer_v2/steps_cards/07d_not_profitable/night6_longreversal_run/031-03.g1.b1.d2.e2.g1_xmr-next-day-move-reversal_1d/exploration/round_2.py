def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coin = list(data["bars"].keys())[0]
    wins = sorted(data["bars"][coin].keys(), key=lambda w: int(w[1:]))
    rows = []
    for w in wins:
        b = data["bars"][coin][w].copy().reset_index(drop=True)
        b["w"] = w
        b["year"] = pd.to_datetime(b["timestamp"]).dt.year
        b["r"] = b["close"].pct_change()
        b["rnext"] = b["close"].shift(-1) / b["close"] - 1
        b["r2"] = b["close"].shift(-2) / b["close"] - 1
        b["r3"] = b["close"].shift(-3) / b["close"] - 1
        b["vol30"] = b["r"].rolling(30, min_periods=20).std()
        b["z"] = b["r"] / b["vol30"]
        b["ret60"] = b["close"] / b["close"].shift(60) - 1
        b["pos"] = b["postRebalance_current_allocation"]
        rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    c = 0.0031 / 2

    def book(posfun, name):
        res = []
        for w, g in B.groupby("w", sort=False):
            p = posfun(g).fillna(0).values
            prev = np.r_[0, p[:-1]]
            ret = p * g["rnext"].fillna(0).values - np.abs(p - prev) * c
            res.append(pd.DataFrame({"w": w, "year": g["year"].values, "ret": ret}))
        R = pd.concat(res, ignore_index=True)
        eq = (1 + R["ret"]).cumprod()
        dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(R)) - 1
        sh = R["ret"].mean() / R["ret"].std() * np.sqrt(365)
        byyr = R.groupby("year")["ret"].sum()
        return {"mean": R["ret"].mean(), "sharpe": sh, "yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                "turn": np.nan, "worst_year_sum": byyr.min(), "y2025": byyr.get(2025, np.nan)}

    v = {}
    v["actual (rebuilt)"] = book(lambda g: g["pos"], "a")
    v["long side only"] = book(lambda g: g["pos"].clip(lower=0), "l")
    v["short side only"] = book(lambda g: g["pos"].clip(upper=0), "s")
    v["long only, x2"] = book(lambda g: 2 * g["pos"].clip(lower=0), "l2")
    v["long only, z<-0.5"] = book(lambda g: g["pos"].clip(lower=0).where(g["z"] < -0.5, 0), "l5")
    v["long only, held 3d (max of last 3)"] = book(lambda g: g["pos"].clip(lower=0).rolling(3, min_periods=1).max(), "l3")
    v["long only, avg of last 3"] = book(lambda g: g["pos"].clip(lower=0).rolling(3, min_periods=1).mean(), "la3")
    v["full, avg of last 3"] = book(lambda g: g["pos"].rolling(3, min_periods=1).mean(), "fa3")
    v["holding coin"] = book(lambda g: pd.Series(1.0, index=g.index), "h")
    out["variants"] = pd.DataFrame(v).T

    # condition check: long-only after falls vs fall days; coin's next-day/3-day returns by z bucket, non-overlap-ish
    B["zb"] = pd.cut(B["z"], [-20, -2, -1, -0.5, 0, 0.5, 1, 2, 20])
    g = B.groupby("zb").agg(n=("rnext", "size"), r1=("rnext", "mean"), r2=("r2", "mean"), r3=("r3", "mean"))
    out["coin fwd by z"] = g
    out["coin mean r2, r3"] = pd.Series({"r2": B["r2"].mean(), "r3": B["r3"].mean()})
    # fall days by trend state: next-day return
    B["tr"] = pd.cut(B["ret60"], [-10, -0.2, 0, 0.2, 10])
    f = B[B["z"] < -1]
    g = f.groupby("tr").agg(n=("rnext", "size"), r1=("rnext", "mean"), sd=("rnext", "std"))
    g["t"] = g["r1"] / (g["sd"] / np.sqrt(g["n"]))
    out["after z<-1 by ret60"] = g
    r = B[B["z"] > 1]
    g = r.groupby("tr").agg(n=("rnext", "size"), r1=("rnext", "mean"), sd=("rnext", "std"))
    g["t"] = g["r1"] / (g["sd"] / np.sqrt(g["n"]))
    out["after z>1 by ret60"] = g
    # 2025 window: short side vs long side gains
    y = B[B["year"] == 2025]
    out["2025 gain by side"] = y.assign(side=np.sign(y["pos"]), gain=y["pos"] * y["rnext"]).groupby("side")["gain"].agg(["size", "sum", "mean"])
    out["2025 coin total"] = (1 + y["r"].fillna(0)).prod() - 1
    return out
