import numpy as np, pandas as pd
from scipy import stats

def swing_info(h, c, i, period=90, side=2, band=0.02):
    # swing highs in past `period` bars ending at i (pivot confirmed: needs side bars after)
    lo = max(side, i - period + 1)
    piv = []
    for j in range(lo, i - side + 1):
        if h[j] == h[j-side:j+side+1].max():
            piv.append(h[j])
    piv = np.array(piv)
    if len(piv) == 0:
        return np.nan, np.nan, np.nan, np.nan
    above = piv[piv >= c[i]]
    if len(above) == 0:
        D, N = np.nan, np.nan
    else:
        L = above.min()
        N = np.sum(np.abs(piv - L) / L <= band)
        D = (L / c[i] - 1) * 100
    # breakout: level just below today's close that was above yesterday's close
    below = piv[(piv < c[i]) & (piv >= c[i-1])] if i >= 1 else np.array([])
    if len(below):
        Lb = below.max()
        Nb = np.sum(np.abs(piv - Lb) / Lb <= band)
        brk = (c[i] / Lb - 1) * 100
    else:
        Nb, brk = np.nan, np.nan
    return N, D, Nb, brk

def tstat(s):
    s = s.dropna()
    return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan

def explore(data):
    bars = data["bars"]
    H = [1, 5, 10]
    drift = {}
    for coin, wins in bars.items():
        for hh in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - hh, hh)
                rs.extend(c[idx + hh] / c[idx] - 1)
            drift[(coin, hh)] = np.mean(rs)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values
            ts = pd.to_datetime(df["timestamp"])
            ma90 = pd.Series(c).rolling(90, min_periods=30).mean().values
            n = len(c)
            for i in range(0, n, 5):
                if i < 10: continue
                N, D, Nb, brk = swing_info(hi, c, i)
                d = {"coin": coin, "win": w, "year": ts.iloc[i].year, "fc": df["forecast"].iloc[i],
                     "N": N, "D": D, "Nb": Nb, "brk": brk,
                     "trend": "above" if c[i] > ma90[i] else ("below" if not np.isnan(ma90[i]) else np.nan)}
                for hh in H:
                    d[f"u{hh}"] = (c[i+hh]/c[i]-1 - drift[(coin, hh)]) if i + hh < n else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    # market-neutral diagnostic: demean u5 by year-trend cell? use year mean of all grid bars per coin
    g["u5_yr"] = g["u5"] - g.groupby(["coin", "year"])["u5"].transform("mean")
    res = {}
    near = g[(g["D"] <= 2)].copy()
    near["Nc"] = near["N"].clip(upper=5)
    res["near_by_N"] = near.groupby("Nc").agg(n=("u5", "count"), u1=("u1", "mean"), u5=("u5", "mean"),
                                              u10=("u10", "mean"), u5_yr=("u5_yr", "mean"))
    res["near_by_N_t5yr"] = near.groupby("Nc")["u5_yr"].apply(tstat)
    far = g[(g["D"] > 2) | g["D"].isna()]
    res["near_vs_far"] = pd.DataFrame({
        "n": [near["u5"].count(), far["u5"].count()],
        "u5": [near["u5"].mean(), far["u5"].mean()],
        "u5_yr": [near["u5_yr"].mean(), far["u5_yr"].mean()],
        "t_u5_yr_diff": [stats.ttest_ind(near["u5_yr"].dropna(), far["u5_yr"].dropna(), equal_var=False).statistic, np.nan]},
        index=["near<=2%", "far"])
    # slope of u5 on forecast within trend, and on market-neutral return
    act = g[g["fc"] < 0]
    sl = {}
    for k, s in [("all_u5yr", act), ("above_u5", act[act.trend == "above"]), ("below_u5", act[act.trend == "below"])]:
        col = "u5_yr" if k == "all_u5yr" else "u5"
        s = s.dropna(subset=[col])
        lr = stats.linregress(s["fc"], s[col])
        sl[k] = pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(s)})
    res["slopes"] = pd.DataFrame(sl).T
    # breakouts: close crossing above a cluster of swing highs
    b = g[g["Nb"].notna()].copy()
    b["Nbc"] = b["Nb"].clip(upper=4)
    res["breakout_by_N"] = b.groupby("Nbc").agg(n=("u5", "count"), u5=("u5", "mean"), u10=("u10", "mean"),
                                                u5_yr=("u5_yr", "mean"))
    res["breakout_t10"] = b.groupby("Nbc")["u10"].apply(tstat)
    res["nonbreak_u5_u10"] = pd.Series({"n": g["Nb"].isna().sum(), "u5": g.loc[g["Nb"].isna(), "u5"].mean(),
                                        "u10": g.loc[g["Nb"].isna(), "u10"].mean()})
    return res
