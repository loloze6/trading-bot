import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1,
                "r5": c / c.shift(5) - 1,
                "r1": c / c.shift(1) - 1,
                "r30": c / c.shift(30) - 1,
                "dlow": c / lo.shift(1).rolling(30).min() - 1,
                "dhigh": c / hi.shift(1).rolling(30).max() - 1,
                "rr": rng.rolling(20).mean() / rng.rolling(60).mean(),
                "vol20": c.pct_change().rolling(20).std(),
                "fc": b["forecast"].astype(float),
            })
            df["pos"] = np.arange(len(df))
            df = df[df["pos"] % H == 0]
            rows.append(df)
    g = pd.concat(rows)
    g = g.dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["unu"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["unu"] / g["coin"].map(usual)
    # standardise features per coin by vol
    g["r5z"] = g["r5"] / (g["vol20"] * np.sqrt(5))
    g["r30z"] = g["r30"] / (g["vol20"] * np.sqrt(30))

    def bucket(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        out = d.groupby("b").agg(n=("z", "size"), mean_unu=("unu", "mean"), mean_z=("z", "mean"),
                                 sd=("unu", "std"), feat=(col, "mean"))
        out["t"] = out["mean_unu"] / (out["sd"] / np.sqrt(out["n"]))
        return out.drop(columns="sd").round(4)

    res = {}
    res["drift_usual"] = pd.DataFrame({"drift": drift, "usual": usual, "n": g.groupby("coin").size()}).round(4)
    for col in ["r5z", "r30z", "dlow", "dhigh", "rr", "vol20"]:
        res["q_" + col] = bucket(col)
    # situations
    sit = {}
    m1 = (g["r30"] < 0) & (g["dlow"] < 0)
    m2 = m1 & (g["rr"] > 1)
    m3 = (g["r30"] < 0) & (g["dlow"] >= 0)
    m4 = (g["r30"] > 0) & (g["dhigh"] > 0)
    for k, m in {"down_break": m1, "down_break_widerng": m2, "down_nobreak": m3, "up_newhigh": m4}.items():
        s = g.loc[m, "unu"]
        sit[k] = {"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan}
    res["situations"] = pd.DataFrame(sit).T.round(4)
    # weekday daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin
            x["wd"] = pd.to_datetime(x["day"]).dt.weekday
            x["prev"] = x["coin_return"].shift(1)
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    wd = D.groupby("wd")["coin_return"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["weekday"] = wd.round(5)
    # next day after big day moves
    D["pz"] = D.groupby("coin")["prev"].transform(lambda s: s / s.std())
    D["pb"] = pd.cut(D["pz"], [-99, -2, -1, 0, 1, 2, 99])
    nd = D.dropna(subset=["pb"]).groupby("pb", observed=True)["coin_return"].agg(["size", "mean", "std"])
    nd["t"] = nd["mean"] / (nd["std"] / np.sqrt(nd["size"]))
    res["nextday_after_move"] = nd.round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    res["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean"]).round(3) if len(T) else "none"
    return res
