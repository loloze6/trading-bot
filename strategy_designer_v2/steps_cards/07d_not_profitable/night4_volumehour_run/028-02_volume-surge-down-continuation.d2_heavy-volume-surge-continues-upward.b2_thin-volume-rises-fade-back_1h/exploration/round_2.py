def explore(data):
    import numpy as np, pandas as pd
    out = {}
    hs = [2, 4, 6, 24]
    rows = []
    for coin, wins in data["bars"].items():
        drift = {}; sd = {}
        for h in hs:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.append(c[idx + h] / c[idx] - 1)
            rr = np.concatenate(rr); drift[h] = rr.mean(); sd[h] = rr.std()
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            v = b["volume"].astype(float).reset_index(drop=True)
            r1 = c.pct_change()
            scale = r1.abs().rolling(720, min_periods=240).mean()
            df = pd.DataFrame({"z": r1 / scale, "vr": v / v.rolling(720, min_periods=240).mean()})
            for h in hs:
                df[f"raw{h}"] = c.shift(-h) / c - 1 - drift[h]
                df[f"s{h}"] = df[f"raw{h}"] / sd[h]
            df = df.iloc[::4]; df["coin"] = coin; df["w"] = w
            rows.append(df)
    d = pd.concat(rows).dropna()
    d["side"] = np.sign(d["z"])
    d["zb"] = pd.cut(d["z"].abs(), [0, 1, 2, 3, 5, 100])
    d["vb"] = pd.cut(d["vr"], [0, 1, 2, 4, 1000])
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    # forward raw return (not signed) after falls, by vol x |z|
    f = d[d["side"] < 0]
    g = f.groupby(["vb", "zb"], observed=True)
    r = pd.DataFrame({"n": g.size()})
    for h in [4, 24]:
        r[f"ret{h}_bp"] = g[f"raw{h}"].mean() * 1e4; r[f"t{h}"] = g[f"raw{h}"].apply(tt)
    out["after FALL hours: unusual fwd return (bp)"] = r.round(2)
    rr_ = d[d["side"] > 0]
    g = rr_.groupby(["vb", "zb"], observed=True)
    r = pd.DataFrame({"n": g.size()})
    for h in [4, 24]:
        r[f"ret{h}_bp"] = g[f"raw{h}"].mean() * 1e4; r[f"t{h}"] = g[f"raw{h}"].apply(tt)
    out["after RISE hours: unusual fwd return (bp)"] = r.round(2)
    # graded heavy-vol falls: score = |z|*log(vr) for falls with vr>1
    hf = f[f["vr"] > 1].copy()
    hf["score"] = hf["z"].abs() * np.log(hf["vr"])
    hf["q"] = pd.qcut(hf["score"], 5, labels=False)
    g = hf.groupby("q")
    out["heavy-vol falls graded by |z|*log(vr) quintile"] = pd.DataFrame({
        "n": g.size(), "score_mean": g["score"].mean(),
        "ret6_bp": g["raw6"].mean() * 1e4, "t6": g["raw6"].apply(tt),
        "strength6": g["s6"].mean(), "ret24_bp": g["raw24"].mean() * 1e4, "t24": g["raw24"].apply(tt)}).round(3)
    # consistency of top: falls vr>2 |z|>2 by coin and by year-ish window groups
    top = f[(f["vr"] > 2) & (f["z"].abs() > 2)].copy()
    top["wn"] = top["w"].str[1:].astype(int)
    top["wg"] = pd.cut(top["wn"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    g = top.groupby(["coin", "wg"], observed=True)
    out["heavy falls by coin x window group"] = pd.DataFrame({"n": g.size(),
        "ret6_bp": g["raw6"].mean() * 1e4, "ret24_bp": g["raw24"].mean() * 1e4}).round(1)
    # book decomposition
    bb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            x = b[["close", "postRebalance_current_allocation", "total_portfolio_value", "postRebalance_total_value"]].astype(float).reset_index(drop=True)
            x["nxt"] = x["close"].shift(-1) / x["close"] - 1
            x["gain"] = x["postRebalance_current_allocation"] * x["nxt"]
            x["fee"] = (x["total_portfolio_value"] - x["postRebalance_total_value"]) / x["total_portfolio_value"]
            x["coin"] = coin; bb.append(x)
    bb = pd.concat(bb).dropna()
    nb = len(bb) / 2
    days = nb / 24
    mh = bb.groupby("coin")["nxt"].transform("mean")
    out["book per day (mean over coins), %"] = pd.Series({
        "gross gain": bb["gain"].sum() / 2 / days * 100,
        "fees": -bb["fee"].sum() / 2 / days * 100,
        "market part": (bb["postRebalance_current_allocation"] * mh).sum() / 2 / days * 100,
        "timing part": (bb["gain"] - bb["postRebalance_current_allocation"] * mh).sum() / 2 / days * 100,
        "turnover per day": (bb["postRebalance_current_allocation"].groupby(bb["coin"]).diff().abs()).sum() / 2 / days,
    }).round(4)
    return out
