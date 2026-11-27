import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allrows = []
    for coin, wins in bars.items():
        drift_parts = []
        for w, b in wins.items():
            r = b["close"].pct_change()
            drift_parts.append(r.dropna())
        drift = pd.concat(drift_parts).mean()
        sd = pd.concat(drift_parts).std()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            nxt = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            rr = rng / rng.rolling(20).mean()
            vol20 = r1.rolling(20).std()
            f5 = (c.shift(1) / c.shift(6) - 1) / (vol20.shift(1) * np.sqrt(5))
            tr60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            vpct = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            fc = b["forecast"].fillna(0)
            prev = fc.shift(1).fillna(0)
            case = (fc <= -2) & ((prev == 0) | (fc - prev <= -2))
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            df = pd.DataFrame({"coin": coin, "w": w, "day": day, "fc": fc, "r1": r1, "rr": rr,
                               "f5": f5, "tr60": tr60, "vpct": vpct, "nxt": nxt,
                               "unus_short": -(nxt - drift), "z": -(nxt - drift) / sd,
                               "year": day.dt.year, "case": case})
            allrows.append(df)
    A = pd.concat(allrows)
    A = A[A["nxt"].notna()]
    def summ(g):
        if len(g) < 3:
            return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": g["unus_short"].mean(), "t": np.nan})
        d = g.groupby("day")["unus_short"].sum()
        m = g["unus_short"].mean()
        nd = len(d)
        se = np.sqrt(((d - g.groupby("day")["unus_short"].count() * m) ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": nd, "mean": m, "t": m / se if se > 0 else np.nan,
                          "strength": g["z"].mean()})
    C = A[A["case"]].copy()
    out = {}
    out["cases_all"] = summ(C)
    out["fc_desc"] = C["fc"].describe()
    out["fc_share_at_cap"] = float((C["fc"] <= -19.99).mean())
    C["fcq"] = pd.qcut(C["fc"].abs().rank(method="first"), 3, labels=["small", "mid", "large"])
    out["by_fc_tercile"] = C.groupby("fcq").apply(summ)
    C["f5q"] = pd.qcut(C["f5"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["by_fall5_tercile"] = C.groupby("f5q").apply(summ)
    C["rrq"] = pd.qcut(C["rr"].rank(method="first"), 3, labels=["lessw", "mid", "widest"])
    out["by_range_tercile"] = C.groupby("rrq").apply(summ)
    C["r1q"] = pd.qcut(C["r1"].rank(method="first"), 3, labels=["smallup", "mid", "bigup"])
    out["by_upday_tercile"] = C.groupby("r1q").apply(summ)
    out["by_coin"] = C.groupby("coin").apply(summ)
    out["by_window"] = C.groupby("w").apply(summ)
    C["agit"] = np.where(C["vpct"] > 0.5, "agitated", "calm")
    out["by_agitation"] = C.groupby("agit").apply(summ)
    # broader: falling market, up day wide, any prior week; graded by range
    B = A[(A["tr60"] < -0.10) & (A["r1"] > 0) & (A["rr"] > 1)].copy()
    out["fall_wideup_all"] = summ(B)
    B["rrq"] = pd.qcut(B["rr"].rank(method="first"), 3, labels=["lessw", "mid", "widest"])
    out["fall_wideup_by_range"] = B.groupby("rrq").apply(summ)
    B["f5q"] = pd.cut(B["f5"], [-99, -1.5, -1, -0.5, 0, 99])
    out["fall_wideup_by_f5"] = B.groupby("f5q").apply(summ)
    return out
