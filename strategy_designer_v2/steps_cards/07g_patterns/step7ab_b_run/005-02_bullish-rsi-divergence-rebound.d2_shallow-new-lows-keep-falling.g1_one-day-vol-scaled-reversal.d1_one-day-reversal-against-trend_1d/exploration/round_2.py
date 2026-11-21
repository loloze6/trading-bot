def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        mu = pd.concat([b["close"].pct_change().dropna() for b in wins.values()]).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=10).std()
            vol60 = r1.rolling(60, min_periods=30).std()
            ma50 = c.rolling(50, min_periods=50).mean()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z": r1 / vol, "clv": (c - b["low"]) / rng, "regime": b["regime"],
                "fc": b["forecast"], "vol": vol, "volratio": vol / vol60,
                "dist": c / ma50 - 1, "r20": c / c.shift(20) - 1,
            })
            for h in [1, 3, 5]:
                d[f"f{h}"] = c.shift(-h) / c - 1 - mu * h
            d["f1n"] = d["f1"] / vol
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def tstat(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    act = D[D["fc"] != 0].copy()
    act["dirn"] = np.sign(act["fc"]) * act["f1n"]
    act["dir"] = np.sign(act["fc"]) * act["f1"]
    act["volq"] = act.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    act["vrq"] = act.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["active_strength_by_volq_side"] = act.groupby([np.sign(act["fc"]), "volq"])["dirn"].apply(tstat).unstack()
    out["active_dir_by_volq_side"] = act.groupby([np.sign(act["fc"]), "volq"])["dir"].apply(tstat).unstack()
    out["active_strength_by_volratio"] = act.groupby([np.sign(act["fc"]), "vrq"])["dirn"].apply(tstat).unstack()

    # all bars: reversal in vol-normalised terms, -z * f1n, by vol tercile and regime (z beyond 1)
    big = D[D["z"].abs() > 1].copy()
    big["rev"] = -np.sign(big["z"]) * big["f1n"]
    big["volq"] = big.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["bigmove_reversal_by_regime_sign_volq"] = big.groupby(["regime", np.sign(big["z"]), "volq"])["rev"].apply(tstat).unstack()

    # correlation of vol level with reversal among big moves: graded?
    cr = {}
    for (rg, s), g in big.groupby(["regime", np.sign(big["z"])]):
        g = g.dropna(subset=["rev", "vol"])
        g["vr"] = g.groupby("coin")["vol"].rank(pct=True)
        r = np.corrcoef(g["vr"], g["rev"])[0, 1]
        cr[(rg, s)] = pd.Series({"n": len(g), "corr": r, "t": r * np.sqrt((len(g) - 2) / (1 - r * r))})
    out["corr_volrank_reversal"] = pd.DataFrame(cr).T

    # distance from 50d avg grading in chop rises / mr falls
    act["distq"] = act.groupby(["coin", np.sign(act["fc"])])["dist"].transform(
        lambda s: pd.qcut(s.abs(), 3, labels=False, duplicates="drop"))
    out["active_strength_by_absdistq"] = act.groupby([np.sign(act["fc"]), "distq"])["dirn"].apply(tstat).unstack()

    # 5-day non-overlapping, short side by vol tercile
    a5 = act[act["pos"] % 5 == 0].copy()
    a5["d5n"] = np.sign(a5["fc"]) * a5["f5"] / (a5["vol"] * np.sqrt(5))
    out["active_5d_strength_by_side_volq"] = a5.groupby([np.sign(a5["fc"]), "volq"])["d5n"].apply(tstat).unstack()

    # chop regime all bars, 20-day return grading on next 3 days (non overlapping)
    ch = D[(D["regime"] == "chop") & (D["pos"] % 3 == 0)].copy()
    ch["f3n"] = ch["f3"] / (ch["vol"] * np.sqrt(3))
    ch["r20q"] = ch.groupby("coin")["r20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["chop_3d_by_r20q"] = ch.groupby("r20q")["f3n"].apply(tstat).unstack()
    return out
