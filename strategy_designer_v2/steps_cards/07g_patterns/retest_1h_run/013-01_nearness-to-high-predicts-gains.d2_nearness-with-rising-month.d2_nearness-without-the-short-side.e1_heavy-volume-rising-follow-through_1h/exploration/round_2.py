import pandas as pd, numpy as np
from scipy import stats

def tt(s):
    s = s.dropna()
    return pd.Series({"mean": s.mean(), "n": len(s), "t": s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan})

def explore(data):
    hh = []; grid24 = []; grid72 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change(); sd = r1.rolling(480).std()
            ts = pd.to_datetime(b["timestamp"])
            hh.append(pd.DataFrame({"coin": coin, "yr": ts.dt.year, "hour": ts.dt.hour, "r": r1, "z": r1 / sd,
                                    "nxt": r1.shift(-1), "f24": c.shift(-24) / c - 1}))
            f = pd.DataFrame({"coin": coin, "yr": ts.dt.year, "win": w,
                              "z24": (c / c.shift(24) - 1) / (sd * np.sqrt(24)),
                              "z1": r1 / sd,
                              "f24": c.shift(-24) / c - 1,
                              "relvol": v.rolling(24).mean() / v.rolling(480).mean() - 1,
                              "trend": (b["regime"] == "trending").astype(int),
                              "f72": c.shift(-72) / c - 1})
            grid24.append(f.iloc[np.arange(0, len(b), 24)])
            grid72.append(f.iloc[np.arange(0, len(b), 72)])
    H = pd.concat(hh).dropna(subset=["r"])
    H["late"] = H["hour"].isin([21, 22])
    late_by_year = H[H.late].groupby("yr")["r"].apply(tt).unstack()
    late_by_coin = H[H.late].groupby("coin")["r"].apply(tt).unstack()
    other_by_year = H[~H.late].groupby("yr")["r"].apply(tt).unstack()
    # graded: next-hour after negative z, regression of nxt on z within z<0
    neg = H[H.z < 0].dropna(subset=["nxt", "z"])
    sl = stats.linregress(neg["z"], neg["nxt"])
    H["zb"] = pd.cut(H["z"], [-np.inf, -3, -1.5, 1.5, 3, np.inf])
    rev24 = H.groupby("zb", observed=True)["f24"].apply(tt).unstack()
    big = H[H.z < -1.5]
    rev_by_year = big.groupby("yr")["nxt"].apply(tt).unstack()
    rev_by_coin = big.groupby("coin")["nxt"].apply(tt).unstack()
    # daily-scale graded reversal on 24h grid
    G = pd.concat(grid24).dropna(subset=["f24", "z24"])
    G["ex"] = G["f24"] - G.groupby("coin")["f24"].transform("mean")
    G["q"] = pd.qcut(G["z24"], 5, labels=False)
    day_q = G.groupby("q")["ex"].apply(tt).unstack()
    s2 = stats.linregress(G["z24"].clip(-4, 4), G["ex"])
    day_reg_by_year = G.groupby("yr").apply(lambda d: pd.Series({"n": len(d), "slope_t": stats.linregress(d["z24"].clip(-4, 4), d["ex"]).slope / stats.linregress(d["z24"].clip(-4, 4), d["ex"]).stderr}))
    # relvol in all bars by year and coin, 72 grid
    K = pd.concat(grid72).dropna(subset=["f72", "relvol"])
    K["ex"] = K["f72"] - K.groupby("coin")["f72"].transform("mean")
    rv_year = K.groupby("yr").apply(lambda d: pd.Series({"n": len(d), "t": stats.linregress(d["relvol"].clip(-1, 3), d["ex"]).slope / stats.linregress(d["relvol"].clip(-1, 3), d["ex"]).stderr}))
    rv_coin = K.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "t": stats.linregress(d["relvol"].clip(-1, 3), d["ex"]).slope / stats.linregress(d["relvol"].clip(-1, 3), d["ex"]).stderr}))
    K["q"] = pd.qcut(K["relvol"].rank(method="first"), 5, labels=False)
    rv_q = K.groupby(["trend", "q"])["ex"].apply(tt).unstack()
    return {"late_by_year": late_by_year.round(6), "late_by_coin": late_by_coin.round(6), "other_by_year": other_by_year.round(6),
            "neg_z_nexthour_slope": f"slope {sl.slope:.6f} t {sl.slope/sl.stderr:.2f} n {len(neg)}",
            "rev24_by_zbin": rev24.round(5), "rev_by_year": rev_by_year.round(6), "rev_by_coin": rev_by_coin.round(6),
            "day_q": day_q.round(5), "day_reg": f"slope {s2.slope:.6f} t {s2.slope/s2.stderr:.2f} n {len(G)}",
            "day_reg_by_year": day_reg_by_year.round(2), "relvol_year": rv_year.round(2), "relvol_coin": rv_coin.round(2),
            "relvol_q_by_trend": rv_q.round(5)}
