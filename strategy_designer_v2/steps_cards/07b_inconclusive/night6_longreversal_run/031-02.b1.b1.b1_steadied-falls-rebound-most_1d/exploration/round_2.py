import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    H = 30
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            reg = b["regime"].values
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                fwd = c[t + H] / c[t] - 1
                r30 = c[t] / c[t - 30] - 1 if t >= 30 else np.nan
                r60 = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                r90 = c[t] / c[t - 90] - 1 if t >= 90 else np.nan
                # share of the last 30 bars in regime
                rows.append(dict(coin=coin, win=w, year=ts.iloc[t].year, day=ts.iloc[t].normalize(),
                                 fwd=fwd, r30=r30, r60=r60, r90=r90, reg=reg[t] == "mean_reversion",
                                 fc=b["forecast"].iloc[t],
                                 lh=b.get("debug_info.components.ret30.last_history_value", pd.Series([np.nan]*n)).iloc[t]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    out = {}
    R = df[df.reg].copy()
    # consistency of r30 recomputed vs recorded
    out["regime: corr lh vs r30 recomputed"] = f"{R[['lh','r30']].dropna().corr().iloc[0,1]:.3f}, n={R[['lh','r30']].dropna().shape[0]}"
    # regime mean ex clustered by day
    def tday(d):
        s = d.groupby("day")["ex"].sum()
        n = len(d); m = d["ex"].mean()
        se = np.sqrt((s - d.groupby("day")["ex"].size() * m).pow(2).sum()) / n
        return pd.Series(dict(cases=n, days=len(s), mean_ex=m, t_day=m / se if se > 0 else np.nan))
    out["regime overall ex (day-clustered)"] = tday(R)
    R["sideR"] = np.where(R["r30"] > 0, "r30>0", "r30<=0")
    out["regime by r30 sign, day-clustered"] = R.dropna(subset=["r30"]).groupby("sideR").apply(tday)
    # regime: ex on r60, r90 (deeper fall -> bigger rebound?)
    def reg(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 8:
            return pd.Series(dict(n=len(d)))
        s = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope / s.stderr))
    out["regime ex on r60"] = reg(R, "r60")
    out["regime ex on r90"] = reg(R, "r90")
    out["regime ex on r30 (fraction)"] = reg(R, "r30")
    # regime by r30 tercile, by fold-like year group
    R["half"] = np.where(R["year"] <= 2022, "<=2022", ">=2023")
    out["regime by r30 sign x half"] = R.dropna(subset=["r30"]).groupby(["half", "sideR"])["ex"].agg(["count", "mean"])
    # outside regime, consistent r30 quintiles: momentum?
    N = df[~df.reg].dropna(subset=["r30"]).copy()
    N["q"] = pd.qcut(N["r30"], 5, labels=False)
    g = N.groupby("q").agg(n=("ex", "size"), r30=("r30", "mean"), ex=("ex", "mean"), sd=("ex", "std"))
    g["t"] = g["ex"] / (g["sd"] / np.sqrt(g["n"]))
    out["non-regime by r30 quintile"] = g
    out["non-regime ex on r30"] = reg(N, "r30")
    # all bars with r60 deep fall (bottom quintile of r60) vs rest
    A = df.dropna(subset=["r60"]).copy()
    A["q60"] = pd.qcut(A["r60"], 5, labels=False)
    g = A.groupby("q60").agg(n=("ex", "size"), r60=("r60", "mean"), ex=("ex", "mean"), sd=("ex", "std"))
    g["t"] = g["ex"] / (g["sd"] / np.sqrt(g["n"]))
    out["all by r60 quintile"] = g
    return out
