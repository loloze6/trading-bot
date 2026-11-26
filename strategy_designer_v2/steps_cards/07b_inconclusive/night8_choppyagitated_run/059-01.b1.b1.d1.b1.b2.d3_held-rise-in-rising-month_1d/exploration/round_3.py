import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [7, 21]
    rows = []
    gridr = {h: [] for h in H}
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; n = len(c)
            for h in H:
                for i in range(0, n - h, h):
                    gridr[h].append((coin, c.iloc[i + h] / c.iloc[i] - 1))
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30).mean()
            sc = r7 / mabs
            r30 = c / c.shift(30) - 1
            for i in range(0, n, 7):
                reg = df["regime"].iloc[i]
                rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "inprof": reg in ("trending", "unknown"),
                       "sc": sc.iloc[i], "r30": r30.iloc[i]}
                for h in H:
                    rec[f"r{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    cs = pd.DataFrame(rows)
    for h in H:
        m = pd.DataFrame(gridr[h], columns=["coin", "r"]).groupby("coin")["r"].mean()
        cs[f"x{h}"] = cs[f"r{h}"] - cs["coin"].map(m)
    def reg(d, xcol, ycol):
        d = d.dropna(subset=[xcol, ycol])
        if len(d) < 5: return {"n": len(d)}
        s = stats.linregress(d[xcol], d[ycol]); y = d[ycol]
        return {"n": len(d), "slope": s.slope, "slope_t": s.slope / s.stderr,
                "mean": y.mean(), "t_mean": y.mean() / (y.std() / np.sqrt(len(y)))}
    out = {}
    prof = cs[cs["inprof"]]
    rises = prof[prof["sc"] > 0]
    rs = []
    for h in H:
        for name, d in [("rises", rises), ("rises_no_w18", rises[rises["win"] != "w18"]),
                        ("rises_r30pos", rises[rises["r30"] > 0]),
                        ("rises_r30pos_no_w18", rises[(rises["r30"] > 0) & (rises["win"] != "w18")])]:
            for xc in ["sc", "r30"]:
                r = reg(d, xc, f"x{h}"); r.update({"h": h, "set": name, "x": xc}); rs.append(r)
    out["grading"] = pd.DataFrame(rs)
    d = rises.dropna(subset=["x7", "r30"]).copy()
    d["q"] = pd.qcut(d["r30"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["rises_by_r30_tercile"] = d.groupby("q").agg(n=("x7", "size"), mean_x7=("x7", "mean"),
                                                     r30=("r30", "mean"))
    d2 = d[d["win"] != "w18"]
    out["rises_by_r30_tercile_no_w18"] = d2.groupby("q").agg(n=("x7", "size"), mean_x7=("x7", "mean"))
    out["w18_share_of_rises"] = float((rises["win"] == "w18").mean())
    return out
