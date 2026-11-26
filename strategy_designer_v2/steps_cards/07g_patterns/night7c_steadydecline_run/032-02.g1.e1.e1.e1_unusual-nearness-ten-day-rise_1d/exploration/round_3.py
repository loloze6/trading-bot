def explore(data):
    import numpy as np, pandas as pd
    out = {}
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.sort_values("day").copy(); d["coin"] = coin; d["win"] = w
            c = d["close"].astype(float)
            d["r1"] = c.pct_change()
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["sd60"] = d["r1"].rolling(60, min_periods=20).std().shift(1)
            d["z"] = d["r1"] / d["sd60"]
            d["r28"] = c / c.shift(28) - 1
            d["calm"] = d["r1"].rolling(10).std() / d["sd60"]
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    D = D.dropna(subset=["z"])
    def tday(s, col):
        dd = s.groupby("day")[col].sum()
        return dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd))) if len(dd) > 2 else np.nan, len(dd)
    # falls only, graded, several horizons; non-overlap grid on h per window for h>1
    res = []
    for h in (1, 2, 3, 5):
        q = D.dropna(subset=[f"f{h}"]).copy()
        q["x"] = q[f"f{h}"] - q.groupby("coin")[f"f{h}"].transform("mean")
        q = q[q.groupby(["coin", "win"]).cumcount() % h == 0]
        for side, s in (("fall", q[q.z < 0]), ("rise", q[q.z > 0])):
            s = s.copy(); s["g"] = -s["z"].clip(-5, 5) * s["x"]
            t, n = tday(s, "g")
            big = s[s.z.abs() >= 2]
            res.append({"h": h, "side": side, "mean_g": s["g"].mean(), "t_day": t, "days": n,
                        "big_n": len(big), "big_mean_x": big["x"].mean()})
    out["graded_by_side_horizon"] = pd.DataFrame(res).round(4)
    # falls of z<=-2: by window, coin, by calm vs not, by r28 sign
    q = D.dropna(subset=["f1"]).copy()
    q["x"] = q["f1"] - q.groupby("coin")["f1"].transform("mean")
    big = q[q.z <= -2].copy()
    out["bigfall_next1_by_win"] = big.groupby("win")["x"].agg(["mean", "count"]).round(4)
    out["bigfall_next1_by_coin"] = big.groupby("coin")["x"].agg(["mean", "count"]).round(4)
    big["r28neg"] = big["r28"] < 0
    out["bigfall_next1_by_r28neg"] = big.groupby("r28neg")["x"].agg(["mean", "count"]).round(4)
    big["calmhalf"] = big["calm"] < big["calm"].median()
    out["bigfall_next1_by_calm"] = big.groupby("calmhalf")["x"].agg(["mean", "count"]).round(4)
    # graded falls inside r28<0 vs >=0
    f = q[q.z < 0].copy(); f["g"] = -f["z"].clip(-5, 5) * f["x"]
    r = []
    for k, s in f.dropna(subset=["r28"]).groupby(f["r28"] < 0):
        t, n = tday(s, "g"); r.append({"r28neg": k, "mean_g": s["g"].mean(), "t_day": t, "days": n})
    out["graded_fall_by_r28sign"] = pd.DataFrame(r).round(4)
    return out
