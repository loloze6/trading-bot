import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, o, h, l = b["close"], b["open"], b["high"], b["low"]
            rng = (h - l)
            d = pd.DataFrame({"coin": coin, "win": w})
            d = d.reindex(range(len(b))); d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(b))
            d["ret1"] = c / c.shift(1) - 1
            d["ret5"] = c / c.shift(5) - 1
            d["ret20"] = c / c.shift(20) - 1
            d["rr"] = rng / rng.rolling(20).mean()
            d["clv"] = ((c - l) / rng.replace(0, np.nan))
            d["body"] = ((c - o).abs() / rng.replace(0, np.nan))
            d["vol20"] = d["ret1"].rolling(20).std()
            d["fwd3"] = c.shift(-3) / c - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["alloc"] = b["postRebalance_current_allocation"]
            d["fc"] = b["forecast"]
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["pos"] % 3 == 0].copy()
    mu = g.groupby("coin")["fwd3"].mean()
    sd = g.groupby("coin")["fwd3"].std()
    g["ex"] = g["fwd3"] - g["coin"].map(mu)
    g["z"] = g["ex"] / g["coin"].map(sd)
    g["volq"] = g.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def tab(df, col, q=5):
        x = df.dropna(subset=[col, "ex"]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = x.groupby("b").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_z=("z", "mean"), sd=("ex", "std"))
        r["t"] = r["mean_ex"] / (r["sd"] / np.sqrt(r["n"]))
        return r.drop(columns="sd").round(4)
    out = {}
    out["mean3 by coin"] = pd.DataFrame({"mean": mu, "sd": sd}).round(4)
    for col in ["ret1", "ret5", "ret20", "rr", "clv", "body", "vol20"]:
        out["q5 " + col] = tab(g, col)
    up = g[g["ret5"] > 0]; dn = g[g["ret5"] <= 0]
    out["UP rr"] = tab(up, "rr"); out["DN rr"] = tab(dn, "rr")
    out["UP clv"] = tab(up, "clv"); out["DN clv"] = tab(dn, "clv")
    # brief: wide range & flat body
    x = g.dropna(subset=["rr", "body", "ex"]).copy()
    x["wide"] = x["rr"] > x.groupby("coin")["rr"].transform("median")
    x["flat"] = x["body"] < 0.25
    x["run"] = np.where(x["ret5"] > 0, "up", "dn")
    x["sex"] = np.where(x["run"] == "up", x["ex"], -x["ex"])  # in run direction
    r = x.groupby(["run", "wide", "flat"]).agg(n=("sex", "size"), m=("sex", "mean"), s=("sex", "std"))
    r["t"] = r["m"] / (r["s"] / np.sqrt(r["n"]))
    out["run-dir excess by wide/flat"] = r.drop(columns="s").round(4)
    out["weekday"] = g.groupby("wd")["ex"].agg(["size", "mean"]).round(4)
    out["volq x ret5sign"] = x.assign(vq=g.loc[x.index, "volq"]).groupby(["vq", "run"])["ex"].agg(["size", "mean"]).round(4)
    out["by coin up-regime ex"] = up.groupby("coin")["ex"].agg(["size", "mean"]).round(4)
    out["regime share by coin"] = A.groupby("coin")["ret5"].apply(lambda s: (s > 0).mean()).round(3)
    return out
