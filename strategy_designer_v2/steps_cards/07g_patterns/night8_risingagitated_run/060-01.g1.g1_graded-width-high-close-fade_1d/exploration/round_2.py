def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            r1 = c / c.shift(1) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "nxt": c.shift(-1) / c - 1, "r1": r1,
                "cloc": (c - l) / (h - l).replace(0, np.nan),
                "vol20": r1.rolling(20, min_periods=10).std(),
                "r60": c / c.shift(60) - 1,
                "inprof": (b["regime"] != "chop").astype(int),
                "year": ts.dt.year, "day": ts.dt.floor("D"),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["exs"] = d["ex"] / d["coin"].map(d.groupby("coin")["nxt"].std())
    d = d.dropna(subset=["nxt", "r1"])
    d["z1"] = d["r1"] / d["vol20"]

    def summ(g):
        dd = g.groupby("day")["ex"].sum()
        t = dd.sum() / np.sqrt((dd**2).sum() - dd.sum()**2 / len(dd)) if len(dd) > 2 else np.nan
        return pd.Series({"n": len(g), "days": g["day"].nunique(),
                          "mean_ex_pct": 100 * g["ex"].mean(),
                          "strength": g["exs"].mean(), "t_day": t})
    out = {}
    P = d[d["inprof"] == 1]
    up = P[P["r1"] > -0.0077]
    out["prof_nondown_by_year"] = up.groupby("year").apply(summ)
    out["prof_nondown_by_coin"] = up.groupby("coin").apply(summ)
    out["prof_z1_q"] = P.groupby(pd.qcut(P["z1"], 6)).apply(summ)
    out["prof_up_z1_q"] = P[P["r1"] > 0].groupby(pd.qcut(P.loc[P["r1"] > 0, "z1"], 3)).apply(summ)
    d["vol_q"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    O = d[(d["inprof"] == 0) & (d["vol_q"] == 2)]
    Ou = O[O["r1"] > 0]
    out["out_hivol_up_z1q"] = Ou.groupby(pd.qcut(Ou["z1"], 3)).apply(summ)
    out["out_hivol_up_by_year"] = Ou.groupby("year").apply(summ)
    d["trend"] = pd.cut(d["r60"], [-10, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    H = d[(d["vol_q"] == 2) & (d["r1"] > 0)]
    out["hivol_up_by_trend"] = H.groupby("trend").apply(summ)
    out["hivol_up_by_coin"] = H.groupby("coin").apply(summ)
    return out
