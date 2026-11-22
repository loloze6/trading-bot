import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            sma = c.rolling(180, min_periods=180).mean()
            dist = c / sma - 1
            past18 = c / c.shift(18) - 1
            past6 = c / c.shift(6) - 1
            vol36 = r1.rolling(36).std()
            vol360 = r1.rolling(360, min_periods=120).std()
            vratio = v.rolling(6).mean() / v.rolling(36).mean()
            sgn = np.sign(r1).fillna(0)
            grp = (sgn != sgn.shift()).cumsum()
            run = sgn.groupby(grp).cumcount() + 1
            run = run * sgn
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.iloc[idx].values,
                "dist": dist.iloc[idx].values, "fc": b["forecast"].iloc[idx].values,
                "p18": past18.iloc[idx].values, "p6": past6.iloc[idx].values,
                "vratio": vratio.iloc[idx].values, "run": run.iloc[idx].values,
                "vrel": (vol36 / vol360).iloc[idx].values,
                "hour": ts.dt.hour.iloc[idx].values, "wd": ts.dt.weekday.iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values,
                "pz": (past18 / (vol360 * np.sqrt(18))).iloc[idx].values,
            })
            rows.append(d)
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def qtab(col, q=5):
        s = g.dropna(subset=[col]).copy()
        s["q"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = s.groupby("q")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["xmean"] = s.groupby("q")[col].mean()
        return t.drop(columns="std")
    for col in ["dist", "p18", "pz", "p6", "vratio", "vrel", "run"]:
        out["q_" + col] = qtab(col)
    # below-average side
    neg = g[g["dist"] < 0]
    sl = stats.linregress(neg["dist"], neg["ex"])
    out["below_avg_slope"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(neg)}"
    pos = g[g["dist"] > 0]
    sl = stats.linregress(pos["dist"], pos["ex"])
    out["above_avg_slope"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(pos)}"
    # fade-volume interaction among strong up runs (brief)
    s = g.dropna(subset=["pz", "vratio"]).copy()
    s["up"] = s["pz"] > s.groupby("coin")["pz"].transform(lambda x: x.quantile(0.8))
    s["dn"] = s["pz"] < s.groupby("coin")["pz"].transform(lambda x: x.quantile(0.2))
    s["fade"] = s["vratio"] < s.groupby("coin")["vratio"].transform("median")
    out["runs_x_fade"] = s[s.up | s.dn].groupby(["up", "fade"])["ex"].agg(["mean", "count"])
    # vol regime x dist
    s = g.dropna(subset=["vrel", "dist"]).copy()
    s["hiv"] = s["vrel"] > s.groupby("coin")["vrel"].transform("median")
    res = {}
    for k, ss in s.groupby("hiv"):
        l = stats.linregress(ss["dist"], ss["ex"]); res[str(k)] = [l.slope, l.slope / l.stderr, len(ss)]
    out["dist_slope_by_hivol"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    out["by_coin_dist"] = g.dropna(subset=["dist"]).groupby("coin").apply(
        lambda x: pd.Series({"t": (lambda l: l.slope / l.stderr)(stats.linregress(x["dist"], x["ex"])), "n": len(x)}))
    out["by_year_pos"] = g[g.fc > 0].groupby("year")["ex"].agg(["mean", "count"])
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["cprev3"] = d["close"] / d["close"].shift(3) - 1
            dd.append(d)
    D = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"] = D.groupby("wd")[["book_return", "coin_return"]].mean()
    hi = D["book_return"].quantile(0.99); lo = D["book_return"].quantile(0.01)
    out["extreme_days_prev3"] = pd.DataFrame({
        "top1pct": [D[D.book_return >= hi]["cprev3"].mean(), (D.book_return >= hi).sum()],
        "bot1pct": [D[D.book_return <= lo]["cprev3"].mean(), (D.book_return <= lo).sum()],
        "all": [D["cprev3"].mean(), len(D)]}, index=["mean coin prev3", "n"])
    out["hour_ex"] = g.groupby("hour")["ex"].agg(["mean", "count"])
    return out
