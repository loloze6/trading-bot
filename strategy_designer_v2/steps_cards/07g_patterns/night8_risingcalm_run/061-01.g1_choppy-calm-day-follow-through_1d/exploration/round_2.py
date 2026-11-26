import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = r1 / sd30
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)), "z": z,
                "fwd": c.shift(-H) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "sd_rel": sd30 / sd30.rolling(120, min_periods=60).median(),
                "inprof": (b["regime"] == "unknown").values,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    for hname, h in [("fwd2", 2), ("fwd", 5), ("fwd10", 10)]:
        G = A[(A["pos"] % h == 0) & A[hname].notna() & A["z"].notna()].copy()
        G["ex"] = G[hname] - G["coin"].map(G.groupby("coin")[hname].mean())
        G["side"] = np.where(G["z"] > 0, "up", "down")
        res = {}
        for s, g in G.groupby("side"):
            sl = stats.linregress(g["z"].abs(), np.sign(g["z"]) * g["ex"])
            res[s] = [len(g), sl.slope, sl.slope / sl.stderr]
        out["graded_slope_signed_ex_on_absz_" + hname] = pd.DataFrame(res, index=["n", "slope", "t"]).T
        # by window/year stability, up days, |z|>1.5
        g = G[(G["z"] > 1.5)]
        out["up_big_by_window_" + hname] = g.groupby("w")["ex"].agg(["count", "mean"])
        G["vb"] = np.where(G["sd_rel"] > 1, "agit", "calm")
        G["trb"] = pd.cut(G["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
        res = {}
        for (v, s), gg in G.groupby(["vb", "side"]):
            if len(gg) > 10:
                sl = stats.linregress(gg["z"].abs(), np.sign(gg["z"]) * gg["ex"])
                res[f"{v}_{s}"] = [len(gg), sl.slope, sl.slope / sl.stderr]
        out["graded_by_vol_side_" + hname] = pd.DataFrame(res, index=["n", "slope", "t"]).T
        res = {}
        for (tb, s), gg in G.groupby(["trb", "side"], observed=True):
            if len(gg) > 10:
                sl = stats.linregress(gg["z"].abs(), np.sign(gg["z"]) * gg["ex"])
                res[f"{tb}_{s}"] = [len(gg), sl.slope, sl.slope / sl.stderr]
        out["graded_by_trend_side_" + hname] = pd.DataFrame(res, index=["n", "slope", "t"]).T
    return out
