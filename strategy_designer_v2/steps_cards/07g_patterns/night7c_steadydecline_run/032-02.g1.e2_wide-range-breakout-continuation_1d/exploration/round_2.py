def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ret28": c / c.shift(28) - 1,
                "rr": rng / rng.rolling(28).mean(),
                "prox": c / c.rolling(28).max(),
                "prox14": c / c.rolling(14).max(),
                "prox56": c / c.rolling(56).max(),
                "proxlow": c / c.rolling(28).min(),
                "vol28": r1.rolling(28).std(),
                "fwd": c.shift(-H) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "pos": np.arange(len(b)),
            })
            df["vollvl"] = df["vol28"] / df["vol28"].rolling(60, min_periods=20).median()
            df["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows).dropna(subset=["fwd", "prox"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["str"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    def summ(s):
        s = s.dropna(); n = len(s); m = s.mean()
        t = m / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_ex_%": 100 * m, "t": t})
    def dayt(sub):
        d = sub.groupby("day")["ex"].sum(); n_d = len(d)
        # t with cases of one day together
        m = sub["ex"].mean(); se = np.sqrt((d - sub.groupby("day")["ex"].count() * m).pow(2).sum()) / len(sub)
        return pd.Series({"n": len(sub), "days": n_d, "mean_ex_%": 100 * m, "t_day": m / se, "strength": sub["str"].mean()})
    out = {}
    g["qp"] = pd.qcut(g["prox"], 10, labels=False)
    out["prox_deciles"] = g.groupby("qp").apply(lambda s: pd.concat([dayt(s), pd.Series({"prox_min": s["prox"].min(), "prox_max": s["prox"].max()})]))
    top = g["prox"] >= 0.999
    out["at_high_vs_not"] = g.groupby(top).apply(dayt)
    out["at_high_by_rr"] = g[top].groupby(g.loc[top, "rr"] >= 1).apply(dayt)
    out["at_high_by_ret28_tercile"] = g[top].groupby(pd.qcut(g.loc[top, "ret28"], 3, labels=False)).apply(dayt)
    out["at_high_by_window"] = g[top].groupby("win")["ex"].apply(summ).unstack()
    out["at_high_by_coin"] = g[top].groupby("coin")["ex"].apply(summ).unstack()
    for f in ["prox14", "prox56"]:
        out["q_" + f] = g.groupby(pd.qcut(g[f], 5, labels=False, duplicates="drop"))["ex"].apply(summ).unstack()
    # graded among not-at-high: distance below high
    nh = g[~top]
    out["below_high_q"] = nh.groupby(pd.qcut(nh["prox"], 5, labels=False)).apply(dayt)
    # pullback zone (0.90-0.97) split by ret28 sign and vol
    pb = g[(g["prox"] > 0.88) & (g["prox"] < 0.97)]
    out["pullback_by_ret28sign"] = pb.groupby(pb["ret28"] > 0).apply(dayt)
    out["pullback_by_vol"] = pb.groupby(pb["vollvl"] >= 1).apply(dayt)
    out["pullback_by_window"] = pb.groupby("win")["ex"].apply(summ).unstack()
    # near low
    out["q_proxlow_day"] = g.groupby(pd.qcut(g["proxlow"], 5, labels=False)).apply(dayt)
    # fwd10 for at-high
    g["ex10"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    out["at_high_fwd10"] = g.groupby(top)["ex10"].apply(summ).unstack()
    return out
