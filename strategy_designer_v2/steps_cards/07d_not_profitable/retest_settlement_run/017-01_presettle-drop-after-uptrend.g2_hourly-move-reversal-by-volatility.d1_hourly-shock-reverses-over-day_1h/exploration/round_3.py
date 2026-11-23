import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            sd = r1.rolling(24).std(); z = r1 / sd
            ts = pd.to_datetime(b["timestamp"], utc=True)
            fwd = c.shift(-24) / c - 1
            r24p = (c / c.shift(24) - 1) / (sd * np.sqrt(24))
            rows.append(pd.DataFrame({"coin": coin, "w": w, "z": z.values, "fwd": fwd.values,
                "hour": ts.dt.hour.values, "year": ts.dt.year.values, "r24p": r24p.values}))
    g = pd.concat(rows).dropna()
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["tot"] = -np.sign(g["z"]) * g["fwd"]
    g["unus"] = -np.sign(g["z"]) * g["ex"]
    g["az"] = g["z"].abs()
    out = {}
    def summ(df, by):
        a = df.groupby(by, observed=True).agg(n=("tot", "size"), total=("tot", "mean"),
                                              unusual=("unus", "mean"), s=("unus", "std"))
        a["t"] = a["unusual"] / (a["s"] / np.sqrt(a["n"]))
        a[["total", "unusual"]] *= 100
        return a.drop(columns="s").round(3)
    # each hour of day: one case per day -> non-overlapping for 24h
    big = g[g.az > 1]
    out["|z|>1 by bar-start hour (one case per day)"] = summ(big, "hour")
    sett = {7, 15, 23}  # bars closing at 08,16,00 UTC
    g["settle"] = np.where(g["hour"].isin(sett), "closes_at_settle",
                   np.where(g["hour"].isin({8, 16, 0}), "first_after", "other"))
    g["zb"] = pd.cut(g["az"], [0, 0.5, 1, 1.5, 2, 3, 100])
    out["by settle class x |z| bin"] = summ(g, ["settle", "zb"])
    gs = g[(g.settle == "closes_at_settle") & (g.az > 1)].copy()
    out["settle-closing |z|>1 by year"] = summ(gs, "year")
    gs["with_trend"] = np.sign(gs["z"]) == np.sign(gs["r24p"])
    out["settle-closing |z|>1 by with prior 24h trend"] = summ(gs, "with_trend")
    gs["side"] = np.where(gs["z"] < 0, "long", "short")
    out["settle-closing |z|>1 by side"] = summ(gs, "side")
    # condition alone: settle hour without the signal (quiet hour)
    q = g[(g.settle == "closes_at_settle") & (g.az <= 0.5)]
    out["settle-closing quiet hours: mean ex fwd % (no direction)"] = pd.Series({
        "n": len(q), "mean_ex%": q["ex"].mean() * 100,
        "t": q["ex"].mean() / (q["ex"].std() / np.sqrt(len(q)))}).round(3)
    return out
