import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = {"1d":6, "3d":18, "7d":42}
    rows = []; hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r6 = c / c.shift(6) - 1
            usual = r6.abs().rolling(180, min_periods=45).mean()
            z = r6 / usual
            rng = (hi.rolling(6).max() - lo.rolling(6).min()) / c.shift(6)
            rr = rng / rng.rolling(180, min_periods=45).mean()
            r42p = c / c.shift(42) - 1
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.shift(-1) / c - 1
            hourly.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year, "r1": r1, "coin": coin, "win": w}))
            for hn, h in H.items():
                idx = np.arange(0, len(b) - h, h)
                fwd = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "win": w, "yr": ts.iloc[idx].dt.year.values, "h": hn, "fwd": fwd.values,
                    "z": z.iloc[idx].values, "rr": rr.iloc[idx].values, "prior7": r42p.iloc[idx].values}))
    d = pd.concat(rows, ignore_index=True)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["sd"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["ex"] = d["fwd"] - d["drift"]; d["str"] = d["ex"] / d["sd"]
    d = d.dropna(subset=["z", "rr", "str"])
    def agg(g):
        n = len(g); m = g["str"].mean(); s = g["str"].std()
        return pd.Series({"n": n, "strength": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan})
    out = {}
    # graded panic score: fall depth x range ratio
    d["pscore"] = (-d["z"]).clip(lower=0) * d["rr"]
    pos = d[d.pscore > 0].copy()
    pos["pbin"] = pos.groupby("h")["pscore"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["panic_score_quintiles"] = pos.groupby(["h", "pbin"]).apply(agg).unstack(0).round(3)
    pc = {}
    for hn in H:
        g = d[d.h == hn]
        r, p = stats.spearmanr(g["pscore"], g["str"]); pc[hn] = (round(r, 4), round(p, 4), len(g))
    out["spearman_pscore"] = pd.DataFrame(pc, index=["rho", "p", "n"])
    # range ratio split by direction of 24h move
    d["dir"] = np.where(d["z"] < 0, "down", "up")
    d["rrbin"] = d.groupby("h")["rr"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["rr_by_dir_3d"] = d[d.h == "3d"].groupby(["dir", "rrbin"]).apply(agg).unstack(0).round(3)
    out["rr_by_dir_1d"] = d[d.h == "1d"].groupby(["dir", "rrbin"]).apply(agg).unstack(0).round(3)
    # panic robustness
    pan = d[(d.z < -1.5) & (d.rr > 1.8)]
    out["panic_1d_by_coin"] = pan[pan.h == "1d"].groupby("coin").apply(agg).round(3)
    out["panic_1d_by_year"] = pan[pan.h == "1d"].groupby("yr").apply(agg).round(3)
    out["panic_3d_by_year"] = pan[pan.h == "3d"].groupby("yr").apply(agg).round(3)
    # prior 7d momentum robustness on 3d
    d["p7bin"] = d.groupby("h")["prior7"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["mom_3d_by_coin_top_minus_bot"] = d[d.h == "3d"].groupby("coin").apply(
        lambda g: pd.Series({"top": g[g.p7bin == 4]["str"].mean(), "bot": g[g.p7bin == 0]["str"].mean(),
                             "t": stats.ttest_ind(g[g.p7bin == 4]["str"], g[g.p7bin == 0]["str"], equal_var=False).statistic})).round(3)
    # hour 16 / friday robustness
    hh = pd.concat(hourly).dropna(subset=["r1"])
    def tt(g):
        return pd.Series({"mean_bp": g["r1"].mean() * 1e4, "t": g["r1"].mean() / (g["r1"].std() / np.sqrt(len(g))), "n": len(g)})
    out["h16_by_coin"] = hh[hh.hour == 16].groupby("coin").apply(tt).round(2)
    out["h16_by_year"] = hh[hh.hour == 16].groupby("yr").apply(tt).round(2)
    out["h20_by_year"] = hh[hh.hour == 20].groupby("yr").apply(tt).round(2)
    out["fri_by_year"] = hh[hh.wd == 4].groupby("yr").apply(tt).round(2)
    out["fri_by_hour"] = hh[hh.wd == 4].groupby("hour").apply(tt).round(2)
    out["all_by_year"] = hh.groupby("yr").apply(tt).round(2)
    return out
