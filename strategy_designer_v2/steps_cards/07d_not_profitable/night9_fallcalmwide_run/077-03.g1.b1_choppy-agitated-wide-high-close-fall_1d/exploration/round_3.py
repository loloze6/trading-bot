def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = (b.high - b.low)
            cl = (b.close - b.low) / rng.replace(0, np.nan)
            r = b.close.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            width = (rng / b.close) / sd30
            z = (width - width.rolling(60, min_periods=20).mean()) / width.rolling(60, min_periods=20).std()
            nxt = b.close.shift(-1) / b.close - 1
            d = pd.DataFrame({"coin": coin, "w": w, "day": pd.to_datetime(b.timestamp).dt.floor("D"),
                              "regime": b.regime, "cl": cl, "width": width, "z": z, "nxt": nxt, "r1": r,
                              "alloc": b.postRebalance_current_allocation})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A.regime.isin(["mean_reversion", "unknown"])
    A["nxt"] = A.nxt.fillna(0)
    cost = 0.0022
    hi = A.inprof & (A.cl >= 0.75)
    lo = A.inprof & (A.cl <= 0.25)
    zc = A.z.clip(-2, 3).fillna(0)
    grade = (1 + zc / 2).clip(0, 2.5)          # graded by width, about 1 for usual width
    variants = {
        "tested: high close short, graded": np.where(hi, -grade, 0.0),
        "high close short, size only widening (z>0 graded)": np.where(hi, -zc.clip(0, None), 0.0),
        "both sides: high short, low long, graded": np.where(hi, -grade, np.where(lo, grade, 0.0)),
        "both sides, size only widening": np.where(hi, -zc.clip(0, None), np.where(lo, zc.clip(0, None), 0.0)),
        "low close long only, graded": np.where(lo, grade, 0.0),
    }
    def book_stats(pos):
        g = pos * A.nxt.values - cost * np.abs(pos)
        B = pd.DataFrame({"w": A.w, "day": A.day, "g": g}).groupby(["w", "day"]).g.mean()
        wo = sorted(B.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))
        B = pd.concat([B.loc[x] for x in wo])
        eq = (1 + B).cumprod(); fall = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(B)) - 1
        return pd.Series({"sharpe": B.mean() / B.std() * np.sqrt(365), "yearly": yr, "fall": fall,
                          "calmar": yr / -fall if fall < 0 else np.nan, "cases": int((pos != 0).sum())})
    out = {}
    out["simulated books (unit size, cost 0.22%)"] = pd.DataFrame({k: book_stats(np.asarray(v)) for k, v in variants.items()}).T
    H = A.groupby(["w", "day"]).nxt.mean()
    out["holding sharpe (same days)"] = H.mean() / H.std() * np.sqrt(365)
    # where the tested book lost: w12 and the worst active bars
    act = A[A.regime == "mean_reversion"].copy()
    act["pnl"] = act.alloc * act.nxt
    act["zhalf"] = np.where(act.z > 0, "widening z>0", "z<=0")
    out["active bars by z half"] = act.groupby("zhalf").agg(n=("pnl", "size"), pnl_sum=("pnl", "sum"), nxt_mean=("nxt", "mean"), alloc=("alloc", "mean"))
    out["active bars by window x z half: pnl sum"] = act.groupby(["w", "zhalf"]).pnl.sum().unstack()
    # condition alone check: wide days (z>0) in profile with mid close, short and long sign
    mid = A[A.inprof & (A.cl > 0.25) & (A.cl < 0.75)]
    out["in-profile mid-close, z>0: next-day mean (long sign)"] = pd.Series({"n": int((mid.z > 0).sum()), "mean": mid[mid.z > 0].nxt.mean()})
    return out
