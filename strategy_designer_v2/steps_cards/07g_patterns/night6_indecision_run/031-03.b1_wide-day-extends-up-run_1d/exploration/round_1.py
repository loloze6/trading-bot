import numpy as np
import pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30:
                continue
            rng = b["high"] - b["low"]
            ratio = rng / rng.rolling(20).mean()
            c = b["close"]
            r5 = c / c.shift(5) - 1
            r1 = c / c.shift(1) - 1
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            body = (b["close"] - b["open"]) / rng.replace(0, np.nan)
            clv = (b["close"] - b["low"]) / rng.replace(0, np.nan)
            vol20 = r1.rolling(20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": b["timestamp"], "pos": np.arange(len(b)),
                "ratio": ratio, "r5": r5, "r1": r1, "fwd3": fwd3, "fwd1": fwd1,
                "body": body, "clv": clv, "vol20": vol20,
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ts"] = pd.to_datetime(d["ts"])
    g = d[d["pos"] % 3 == 0].copy()
    drift = g.groupby("coin")["fwd3"].mean()
    usual = g.groupby("coin")["fwd3"].std()
    g["unus"] = g["fwd3"] - g["coin"].map(drift)
    g["str"] = g["unus"] / g["coin"].map(usual)
    g = g.dropna(subset=["unus", "ratio", "r5"])

    def summ(sub):
        s = sub.groupby(sub["ts"].dt.floor("D"))["unus"].sum()
        D = len(s)
        n = len(sub)
        m = sub["unus"].mean()
        if D < 3:
            return pd.Series({"n": n, "days": D, "mean_unus%": m * 100, "t_day": np.nan})
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / n
        return pd.Series({"n": n, "days": D, "mean_unus%": m * 100,
                          "strength": sub["str"].mean(), "t_day": m / se})

    g["wide"] = np.where(g["ratio"] >= 1.5, "wide", "normal")
    g["r5q"] = pd.qcut(g["r5"], 5, labels=["q1low", "q2", "q3", "q4", "q5high"])
    out = {}
    out["by_wide_r5q"] = g.groupby(["wide", "r5q"]).apply(summ)
    g["ratiob"] = pd.cut(g["ratio"], [0, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 99])
    g["dir1"] = np.where(g["r1"] > 0, "up", "down")
    out["by_ratio_daydir"] = g.groupby(["ratiob", "dir1"]).apply(summ)
    gw = g[g["wide"] == "wide"].copy()
    gw["clvb"] = pd.cut(gw["clv"], [-0.01, 0.25, 0.5, 0.75, 1.01])
    out["wide_by_closeloc_r5sign"] = gw.groupby(["clvb", np.where(gw["r5"] > 0, "r5up", "r5down")]).apply(summ)
    g["volq"] = g.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["lowvol", "mid", "highvol"]))
    out["by_vol_r5sign"] = g.groupby(["volq", np.where(g["r5"] > 0, "r5up", "r5down")]).apply(summ)
    out["by_coin_wide_up"] = g[(g["wide"] == "wide") & (g["r5"] > 0)].groupby("coin").apply(summ)
    out["by_year_wide_up"] = g[(g["wide"] == "wide") & (g["r5"] > 0)].groupby(g["ts"].dt.year).apply(summ)
    return out
