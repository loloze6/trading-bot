import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H_list = [6, 18, 42, 84]
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = df["high"].astype(float); lo = df["low"].astype(float)
            r6 = c / c.shift(6) - 1
            usual = r6.abs().rolling(180, min_periods=45).mean()
            depth = (-r6 / usual)  # raw scaled fall, positive = fall
            rng = (hi.rolling(6).max() / lo.rolling(6).min() - 1)
            rng_usual = rng.rolling(180, min_periods=45).mean()
            rng_ratio = rng / rng_usual
            ret30 = c / c.shift(180) - 1
            fc = df["forecast"].astype(float)
            n = len(df)
            for H in H_list:
                for i in range(0, n - H, H):
                    recs.append(dict(coin=coin, win=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     H=H, fc=fc.iloc[i], depth=depth.iloc[i], rng_ratio=rng_ratio.iloc[i],
                                     ret30=ret30.iloc[i], fwd=c.iloc[i + H] / c.iloc[i] - 1))
    R = pd.DataFrame(recs)
    R["drift"] = R.groupby(["coin", "H"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin", "H"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"] / R["sd"]
    out = {}
    def slope_t(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10 or d[x].std() == 0: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[x], d["ex"])
        return (s.slope, s.slope / s.stderr, len(d))
    rows = []
    for H in H_list:
        d = R[R.H == H]
        for x in ["fc", "depth", "rng_ratio"]:
            s, t, n = slope_t(d, x)
            rows.append(dict(H=H, x=x, slope=s, t=t, n=n))
    out["slope_by_horizon"] = pd.DataFrame(rows)
    d84 = R[R.H == 84].copy()
    act = d84[d84.fc > 0].copy()
    act["q"] = pd.qcut(act.fc.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    g = act.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), ex=("ex", "mean"), strength=("str", "mean"))
    g.loc["flat"] = [ (d84.fc == 0).sum(), 0, d84[d84.fc == 0].ex.mean(), d84[d84.fc == 0].str.mean()]
    out["by_fc_quartile_84"] = g
    def grp(d, k):
        return d.groupby(k).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", lambda v: v.mean() / (v.std() / np.sqrt(len(v)))))
    out["active_by_coin_84"] = grp(act, "coin")
    out["active_by_year_84"] = grp(act, "year")
    act["trend"] = np.where(act.ret30 > 0, "up30", "down30")
    out["active_by_trend_84"] = grp(act, "trend")
    d84["rq"] = pd.qcut(d84.rng_ratio.rank(method="first"), 4, labels=["r1", "r2", "r3", "r4"])
    d84["panic"] = np.where(d84.depth > 0, "fall", "rise")
    out["range_x_fall_84"] = d84.groupby(["panic", "rq"]).agg(n=("ex", "size"), ex=("ex", "mean"), strength=("str", "mean"))
    # deepest falls by raw depth, other horizons
    rows = []
    for H in H_list:
        d = R[(R.H == H)].dropna(subset=["depth"])
        for lab, m in [("depth>2", d.depth > 2), ("depth>1", d.depth > 1), ("0<depth<=1", (d.depth > 0) & (d.depth <= 1)), ("rise", d.depth <= 0)]:
            v = d[m].ex
            rows.append(dict(H=H, grp=lab, n=len(v), ex=v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    out["depth_groups_by_H"] = pd.DataFrame(rows)
    return out
