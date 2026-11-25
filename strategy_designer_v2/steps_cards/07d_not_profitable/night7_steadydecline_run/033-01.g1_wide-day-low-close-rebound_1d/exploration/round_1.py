def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["r2"] = b["close"].shift(-2) / b["close"] - 1
            b["tr60"] = b["close"] / b["close"].shift(60) - 1
            dr = b["close"].pct_change()
            b["dayret"] = dr
            b["vratio"] = dr.rolling(10).std() / dr.rolling(60).std()
            rng = b["high"] - b["low"]
            b["widemult"] = rng / rng.rolling(20).mean()
            b["cl"] = (b["high"] + b["low"] - 2 * b["close"]) / rng.replace(0, np.nan)
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["r1"]
            b["chg"] = (b["pos"] - b["previous_allocation"]).abs()
            b["coin"] = c
            b["w"] = w
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r1"].mean()
    d["x1"] = d["r1"] - d["coin"].map(mu)
    d["sg"] = np.sign(d["forecast"])
    d["sx"] = d["sg"] * d["x1"]
    d["sx2"] = d["sg"] * (d["r2"] - 2 * d["coin"].map(mu))
    out = {}

    def summ(g, col):
        m = g[col].mean(); s = g[col].std(); n = g[col].count()
        return pd.DataFrame({"mean": m, "n": n, "t": m / (s / np.sqrt(n))})

    # 1. forecast deciles: graded next-day excess and 2-day excess
    d["fq"] = pd.qcut(d["forecast"], 10, labels=False, duplicates="drop")
    g = d.groupby("fq")
    out["deciles"] = pd.DataFrame({
        "f": g["forecast"].mean(), "x1": g["x1"].mean(),
        "t1": g["x1"].mean() / (g["x1"].std() / np.sqrt(g["x1"].count())),
        "sx2": g["sx2"].mean(), "n": g.size()})

    # 2. gross vs fee drag of the book, by side
    d["side"] = np.sign(d["pos"]).fillna(0)
    g = d.groupby("side")
    out["book_side"] = pd.DataFrame({
        "gross_per_day": g["gross"].mean(),
        "turnover": g["chg"].mean(),
        "fee_drag_est": g["chg"].mean() * 0.0019 / 2,
        "abs_pos": g["pos"].apply(lambda s: s.abs().mean()),
        "n": g.size()})

    # 3. strength of the signal: |forecast| bins, signed excess move vs cost
    d["absf"] = pd.cut(d["forecast"].abs(), [-0.01, 2, 5, 10, 15, 20.01])
    out["absf_side"] = summ(d.groupby(["absf", "sg"]), "sx")

    # 4. trend profile x side
    d["trend"] = np.where(d["tr60"] > 0.1, "rising",
                 np.where(d["tr60"] < -0.1, "falling",
                 np.where(d["tr60"].notna(), "choppy", "na")))
    out["trend_side"] = summ(d.groupby(["trend", "sg"]), "sx")

    # 5. strong cases (top fifth |forecast|) by agitation proxy and side
    strong = d["forecast"].abs() >= d["forecast"].abs().quantile(0.8)
    d["strong"] = strong
    d["vq"] = pd.qcut(d["vratio"], 3, labels=False)
    out["strong_vq_side"] = summ(d[strong].groupby(["vq", "sg"]), "sx")

    # 6. strong cases by the day's own direction (down day closing low vs up day closing low)
    d["dd"] = np.sign(d["dayret"])
    out["strong_dd_side"] = summ(d[strong].groupby(["sg", "dd"]), "sx")

    # 7. condition check: wide day alone vs close location alone (no signal side)
    d["wq"] = pd.qcut(d["widemult"], 4, labels=False)
    d["cq"] = pd.cut(d["cl"], [-1.01, -0.5, 0, 0.5, 1.01])
    out["wide_x_closeloc_x1"] = summ(d.groupby(["wq", "cq"]), "x1")

    # 8. by window: book and holding mean daily returns
    dd_ = pd.concat([x.assign(coin=c, w=w) for c, ws in data["days"].items() for w, x in ws.items()])
    out["by_window"] = dd_.groupby("w")[["book_return", "coin_return"]].mean()
    out["by_coin_strong_sx"] = summ(d[strong].groupby("coin"), "sx")
    return out
