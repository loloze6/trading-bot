def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = [24, 48, 96, 168]
    rows = []
    hourly = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().shift(1).rolling(720, min_periods=120).mean()
            ratio = r24 / mabs
            r720 = c / c.shift(720) - 1
            vol = np.log(c).diff().rolling(720, min_periods=120).std()
            r1 = c.shift(-1) / c - 1
            hourly.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1}))
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                fwd = (c.values[idx + h] / c.values[idx]) - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "ratio": ratio.values[idx],
                                          "r720": r720.values[idx], "vol": vol.values[idx], "fwd": fwd}))
    R = pd.concat(rows, ignore_index=True)
    R["drift"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin", "h"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"] / R["sd"]
    R = R.dropna(subset=["ratio"])
    bins = [-np.inf, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, np.inf]
    R["rb"] = pd.cut(R["ratio"], bins).astype(str)
    def summ(g):
        return pd.Series({"n": len(g), "ex_bps": g["ex"].mean() * 1e4,
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "strength": g["str"].mean()})
    out = {}
    for h in H:
        out[f"by_ratio_h{h}"] = R[R.h == h].groupby("rb").apply(summ)
    D = R[(R.h == 48) & (R.ratio < -1)].copy()
    D["trend"] = np.where(D["r720"] > 0, "up30d", "down30d")
    out["drops_h48_by_trend"] = D.groupby("trend").apply(summ)
    U = R[(R.h == 48) & (R.ratio > 1)].copy()
    U["trend"] = np.where(U["r720"] > 0, "up30d", "down30d")
    out["rises_h48_by_trend"] = U.groupby("trend").apply(summ)
    A = R[R.h == 48].dropna(subset=["vol"]).copy()
    A["vt"] = A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=["lowvol", "midvol", "highvol"])).astype(str)
    A["side"] = np.where(A.ratio < -1, "drop>1", np.where(A.ratio > 1, "rise>1", "mid"))
    out["h48_vol_x_side"] = A.groupby(["vt", "side"]).apply(summ)
    out["h48_by_coin_drops"] = R[(R.h == 48) & (R.ratio < -1)].groupby("coin").apply(summ)
    out["spearman_ratio_ex"] = pd.DataFrame({h: stats.spearmanr(R[R.h == h]["ratio"], R[R.h == h]["ex"]) for h in H}, index=["rho", "p"])
    Hh = pd.concat(hourly).dropna()
    Hh["ex"] = Hh["r1"] - Hh.groupby("coin")["r1"].transform("mean")
    g = Hh.groupby("hour")["ex"]
    out["by_hour_bps"] = pd.DataFrame({"bps": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    g = Hh.groupby("wd")["ex"]
    out["by_wd_bps"] = pd.DataFrame({"bps": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    return out
