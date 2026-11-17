import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    cm = {}
    H = [1, 3, 5, 10]
    for coin, wins in bars.items():
        grid = {h: [] for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            for h in H:
                for i in range(0, n - h, h):
                    grid[h].append(c[i + h] / c[i] - 1)
            reg = df["regime"].values
            vr = df.get("debug_info.components.volratio.last_history_value")
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(20).std().shift(1)
            ret30 = pd.Series(c) / pd.Series(c).shift(30) - 1
            last = -10
            for i in range(n):
                if reg[i] == "mean_reversion" and i - last >= 3:
                    last = i
                    rng = df["high"][i] - df["low"][i]
                    d = dict(coin=coin, win=w, year=pd.Timestamp(df["timestamp"][i]).year,
                             vr=vr[i] if vr is not None else np.nan,
                             z=r1[i] / sd[i] if sd[i] and sd[i] > 0 else np.nan,
                             wick=(c[i] - df["low"][i]) / rng if rng > 0 else np.nan,
                             r30=ret30[i])
                    for h in H:
                        d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                    rows.append(d)
        cm[coin] = {h: np.mean(grid[h]) for h in H}
    K = pd.DataFrame(rows)
    for h in H:
        K[f"x{h}"] = K[f"f{h}"] - K["coin"].map(lambda c: cm[c][h])
    out = {}

    def slope(d, y="x3", x="vr"):
        d = d[[x, y]].dropna()
        if len(d) < 8:
            return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d[y])
        return (r.slope, r.slope / r.stderr, len(d))

    out["horizon slopes on vr"] = pd.DataFrame({f"h{h}": slope(K, f"x{h}") for h in H}, index=["slope", "t", "n"]).T
    out["horizon mean excess all"] = pd.DataFrame({f"h{h}": [K[f"x{h}"].mean(), stats.ttest_1samp(K[f"x{h}"].dropna(), 0).statistic, K[f"x{h}"].notna().sum()] for h in H}, index=["mean", "t", "n"]).T
    out["by coin"] = pd.DataFrame({c: slope(g) + (g["x3"].mean(),) for c, g in K.groupby("coin")}, index=["slope", "t", "n", "meanx3"]).T
    out["by year"] = pd.DataFrame({y: slope(g) + (g["x3"].mean(),) for y, g in K.groupby("year")}, index=["slope", "t", "n", "meanx3"]).T
    K["vrq"] = pd.qcut(K["vr"], 3, labels=["lo", "mid", "hi"])
    out["vr terciles"] = K.groupby("vrq")[["vr", "x1", "x3", "x5", "x10"]].agg(["mean"]).assign(n=K.groupby("vrq").size())
    K["wq"] = pd.qcut(K["wick"], 3, labels=["lowwick", "mid", "highwick"])
    out["wick terciles"] = K.groupby("wq")[["wick", "x1", "x3", "x5", "x10"]].mean().assign(n=K.groupby("wq").size())
    out["slope vr by wick tercile"] = pd.DataFrame({str(q): slope(g) for q, g in K.groupby("wq")}, index=["slope", "t", "n"]).T
    K["rq"] = pd.qcut(K["r30"], 3, labels=["down30", "mid", "up30"])
    out["slope vr by 30d ret tercile"] = pd.DataFrame({str(q): slope(g) + (g["x3"].mean(),) for q, g in K.groupby("rq")}, index=["slope", "t", "n", "meanx3"]).T
    K["zq"] = pd.qcut(K["z"], 3, labels=["deepest", "mid", "mild"])
    out["slope vr by fall-size tercile"] = pd.DataFrame({str(q): slope(g) + (g["x3"].mean(),) for q, g in K.groupby("zq")}, index=["slope", "t", "n", "meanx3"]).T
    out["slope x3 on wick"] = slope(K, "x3", "wick")
    out["vr dist"] = K["vr"].describe()
    return out
