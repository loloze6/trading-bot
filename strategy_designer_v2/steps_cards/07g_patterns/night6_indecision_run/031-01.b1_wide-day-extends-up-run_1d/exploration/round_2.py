import numpy as np, pandas as pd

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            n = len(b)
            c, o, h, l = b["close"].astype(float), b["open"].astype(float), b["high"].astype(float), b["low"].astype(float)
            rng = (h - l)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame(index=range(n))
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(n)
            d["ret1"] = (c / c.shift(1) - 1).values
            d["ret5"] = (c / c.shift(5) - 1).values
            d["ret20"] = (c / c.shift(20) - 1).values
            d["rr"] = (rng / rng.rolling(20).mean()).values
            rz = rng.replace(0, np.nan)
            d["clv"] = ((c - l) / rz).values
            d["body"] = ((c - o).abs() / rz).values
            d["sbody"] = ((c - o) / rz).values
            d["vol20"] = d["ret1"].rolling(20).std().values
            d["fwd3"] = (c.shift(-3) / c - 1).values
            d["wd"] = ts.dt.weekday.values
            d["yr"] = ts.dt.year.values
            d["alloc"] = b["postRebalance_current_allocation"].astype(float).values
            d["fc"] = b["forecast"].astype(float).values
            d["day"] = ts.dt.floor("D").values
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["pos"] % 3 == 0].copy()
    mu = g.groupby("coin")["fwd3"].mean()
    sd = g.groupby("coin")["fwd3"].std()
    g["ex"] = g["fwd3"] - g["coin"].map(mu)
    g["z"] = g["ex"] / g["coin"].map(sd)

    def tdays(x, col="ex"):
        s = x.groupby("day")[col].sum()
        k = x.groupby("day")[col].size()
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return m / se if se > 0 else np.nan

    def tab(df, col, q=5):
        x = df.dropna(subset=[col, "ex"]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        res = []
        for bb, xx in x.groupby("b"):
            res.append({"b": bb, "n": len(xx), "days": xx["day"].nunique(), "mean_ex": xx["ex"].mean(),
                        "mean_z": xx["z"].mean(), "t_day": tdays(xx)})
        return pd.DataFrame(res).set_index("b").round(4)

    out["mean3 by coin"] = pd.DataFrame({"mean": mu, "sd": sd}).round(4)
    for col in ["ret1", "ret5", "ret20", "rr", "clv", "sbody", "vol20"]:
        try: out["q5 " + col] = tab(g, col)
        except Exception as e: out["q5 " + col] = str(e)
    up = g[g["ret5"] > 0]; dn = g[g["ret5"] <= 0]
    for nm, df, col in [("UP rr", up, "rr"), ("DN rr", dn, "rr"), ("UP ret1", up, "ret1"), ("DN ret1", dn, "ret1"), ("UP clv", up, "clv"), ("DN clv", dn, "clv")]:
        try: out[nm] = tab(df, col)
        except Exception as e: out[nm] = str(e)
    try:
        x = g.dropna(subset=["rr", "body", "ex", "ret5"]).copy()
        x["wide"] = x["rr"] > x.groupby("coin")["rr"].transform("median")
        x["flat"] = x["body"] < 0.25
        x["run"] = np.where(x["ret5"] > 0, "up", "dn")
        x["sex"] = np.where(x["run"] == "up", x["ex"], -x["ex"])
        res = []
        for k, xx in x.groupby(["run", "wide", "flat"]):
            res.append({"run": k[0], "wide": k[1], "flat": k[2], "n": len(xx), "m_rundir": xx["sex"].mean(), "t_day": tdays(xx, "sex")})
        out["run-dir excess by wide/flat"] = pd.DataFrame(res).round(4)
    except Exception as e: out["wideflat"] = str(e)
    out["weekday ex"] = g.groupby("wd")["ex"].agg(["size", "mean"]).round(4)
    out["year ex"] = g.groupby("yr")["ex"].agg(["size", "mean"]).round(4)
    out["regime share up5"] = A.groupby("coin")["ret5"].apply(lambda s: (s > 0).mean()).round(3)

    # book
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; dd["win"] = w
            D.append(dd)
    D = pd.concat(D, ignore_index=True)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["win", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean"), yr=("yr", "first")).dropna()
    out["book by year"] = bk.groupby("yr").agg(n=("b", "size"), book=("b", "mean"), hold=("h", "mean"),
        bsd=("b", "std")).assign(sh=lambda r: r["book"] / r["bsd"] * np.sqrt(365)).round(5)
    out["book vs hold corr"] = float(bk["b"].corr(bk["h"]))
    beta = np.polyfit(bk["h"], bk["b"], 1)
    out["book on hold slope, intercept"] = f"{beta[0]:.3f}, {beta[1]:.6f}"
    # book in up/down hold days
    bk["hq"] = pd.qcut(bk["h"], 5, labels=False)
    out["book by hold-day quintile"] = bk.groupby("hq")[["b", "h"]].mean().round(5)

    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades by entry fc q"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), fc=("entry_forecast", "mean"),
        net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"),
        dur_d=("duration_minutes", lambda s: s.mean() / 1440)).round(3)
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean")).round(3)
    # held vs not held excess
    g["held"] = g["alloc"].abs() > 0
    out["ex by held"] = g.groupby("held")["ex"].agg(["size", "mean"]).round(4)
    return out
