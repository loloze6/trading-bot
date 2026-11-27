import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].astype(float).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            depth = (c - hi) / hi / sd
            choppy = b["regime"].astype(str).isin(["trending", "unknown"])
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                              "r1": r1, "depth": depth, "choppy": choppy,
                              "ts": pd.to_datetime(b["timestamp"])})
            for h in [1, 3, 5, 7, 10]:
                d[f"f{h}"] = c.shift(-h) / c - 1 - ((1 + mu) ** h - 1)
                d[f"z{h}"] = d[f"f{h}"] / (np.sqrt(h) * r1.std())
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["choppy"] & D["depth"].notna()].copy()
    D["up"] = D["r1"] > 0
    out = {}
    # grade by depth bins (fixed, std units), up days vs down vs all, h=5 non-overlapping
    bins = [-np.inf, -4, -2.5, -1.5, -0.5, 0.01]
    res = []
    for h in [3, 5, 7, 10]:
        for side, m in [("up", D["up"]), ("down", ~D["up"]), ("all", D["up"] | ~D["up"])]:
            s = D[m & (D["pos"] % h == 0)].dropna(subset=[f"f{h}"])
            # short gain graded: -depth * excess (depth negative -> short)
            g = s["depth"] * s[f"f{h}"]  # positive when deep & falls
            byday = (g - g.mean()).groupby(s["ts"].dt.floor("D")).sum()
            t_day = g.mean() * len(g) / np.sqrt((byday ** 2).sum())
            rho = stats.spearmanr(s["depth"], s[f"f{h}"])[0]
            strength = (-np.sign(s["depth"].where(s["depth"] < 0, np.nan)) * s[f"z{h}"]).mean()
            res.append({"h": h, "side": side, "n": len(s), "days": byday.size,
                        "graded_gain": g.mean(), "t_day": t_day, "rho": rho,
                        "strength_short": -s[f"z{h}"][s["depth"] < 0].mean()})
    out["graded"] = pd.DataFrame(res)
    s = D[D["up"] & (D["pos"] % 5 == 0)].dropna(subset=["f5"]).copy()
    s["b"] = pd.cut(s["depth"], bins)
    out["up_h5_bins"] = s.groupby("b").agg(n=("f5", "count"), f5=("f5", "mean"))
    # robustness: all 5 grid offsets, up days, h=5
    off = []
    for o in range(5):
        s2 = D[D["up"] & (D["pos"] % 5 == o)].dropna(subset=["f5"])
        off.append({"offset": o, "n": len(s2), "rho": stats.spearmanr(s2["depth"], s2["f5"])[0],
                    "graded": (s2["depth"] * s2["f5"]).mean()})
    out["up_h5_offsets"] = pd.DataFrame(off)
    # up days, h=5, all offsets pooled (overlapping, descriptive) by coin and window
    s3 = D[D["up"]].dropna(subset=["f5"])
    out["up_h5_by_coin"] = s3.groupby("coin").apply(lambda x: pd.Series({
        "n": len(x), "rho": stats.spearmanr(x["depth"], x["f5"])[0],
        "deep_f5": x[x["depth"] < -2.5]["f5"].mean(), "shallow_f5": x[x["depth"] > -1]["f5"].mean()}))
    out["up_h5_by_win"] = s3.groupby("win").apply(lambda x: pd.Series({
        "n": len(x), "rho": stats.spearmanr(x["depth"], x["f5"])[0], "mean_f5": x["f5"].mean()}))
    out["up_h5_by_year"] = s3.groupby(s3["ts"].dt.year).apply(lambda x: pd.Series({
        "n": len(x), "rho": stats.spearmanr(x["depth"], x["f5"])[0]}))
    return out
