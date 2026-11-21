import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    H = [5, 10, 26]
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year
            df["ret1"] = r1
            df["ret5"] = c / c.shift(5) - 1
            df["ret26"] = c / c.shift(26) - 1
            df["vol20"] = r1.rolling(20).std()
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            df["kij_dist"] = c / kij - 1
            rng = hi.rolling(26).max() / lo.rolling(26).min() - 1
            df["range26"] = rng
            df["hi_near"] = c / hi.rolling(26).max() - 1
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["n"] = len(b)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out["window_len"] = D.groupby("coin")["n"].describe()[["min", "mean", "max"]]
    res = []
    for h in H:
        G = D[D["pos"] % h == 0].copy()
        drift = G.groupby("coin")[f"f{h}"].transform("mean")
        sd = G.groupby("coin")[f"f{h}"].transform("std")
        G["z"] = (G[f"f{h}"] - drift) / sd
        for feat in ["ret1", "ret5", "ret26", "vol20", "kij_dist", "range26", "hi_near"]:
            # standardise feature per coin
            g = G.dropna(subset=[feat, "z"])
            fz = (g[feat] - g.groupby("coin")[feat].transform("mean")) / g.groupby("coin")[feat].transform("std")
            slope, ic, rr, p, se = stats.linregress(fz, g["z"])
            percoin = g.assign(fz=fz).groupby("coin").apply(lambda x: np.corrcoef(x.fz, x.z)[0, 1])
            res.append({"h": h, "feat": feat, "n": len(g), "corr": rr, "t": slope / se,
                        "coins_pos": int((percoin > 0).sum()), "coins": len(percoin)})
    out["feature_vs_future_z"] = pd.DataFrame(res)
    # weekday one-day returns, all bars (1-bar non-overlap trivially)
    G = D.dropna(subset=["ret1"]).copy()
    G["f1"] = G.groupby(["coin", "win"])["ret1"].shift(-1)
    wd = G.dropna(subset=["f1"]).groupby("wd")["f1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["next_day_by_weekday"] = wd
    # 10d after large |ret5| by sign, quintiles of ret5 standardised by vol
    h = 10
    G = D[D["pos"] % h == 0].dropna(subset=["ret5", "vol20", "f10"]).copy()
    G["u"] = G["f10"] - G.groupby("coin")["f10"].transform("mean")
    G["s5"] = G["ret5"] / (G["vol20"] * np.sqrt(5))
    G["q"] = pd.qcut(G["s5"], 5, labels=False)
    q = G.groupby("q")["u"].agg(["mean", "std", "count"]); q["t"] = q["mean"] / (q["std"] / np.sqrt(q["count"]))
    out["f10_unusual_by_ret5_over_vol_quintile"] = q
    G["vq"] = G.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    v = G.groupby("vq")["u"].agg(["mean", "std", "count"]); v["t"] = v["mean"] / (v["std"] / np.sqrt(v["count"]))
    out["f10_unusual_by_vol_tercile"] = v
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    out["book_by_coin"] = DD.groupby("coin")[["book_return", "coin_return"]].mean()
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
