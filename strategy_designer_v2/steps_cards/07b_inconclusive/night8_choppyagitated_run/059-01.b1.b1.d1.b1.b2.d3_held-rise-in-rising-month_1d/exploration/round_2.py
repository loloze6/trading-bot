import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [7, 14, 21]
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
            hi7 = df["high"].rolling(7).max(); lo7 = df["low"].rolling(7).min()
            pos = (c - lo7) / (hi7 - lo7)
            for i in range(0, n, 7):
                reg = df["regime"].iloc[i]
                rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "inprof": reg in ("trending", "unknown"), "trend": reg == "trending",
                       "sc": sc.iloc[i], "r30": r30.iloc[i], "pos": pos.iloc[i], "f": df["forecast"].iloc[i]}
                for h in H:
                    rec[f"r{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    cs = pd.DataFrame(rows)
    for h in H:
        m = pd.DataFrame(gridr[h], columns=["coin", "r"]).groupby("coin")["r"].mean()
        cs[f"x{h}"] = cs[f"r{h}"] - cs["coin"].map(m)
    out = {}
    def reg(d, xcol, ycol):
        d = d.dropna(subset=[xcol, ycol])
        if len(d) < 5: return {"n": len(d)}
        s = stats.linregress(d[xcol], d[ycol])
        y = d[ycol]
        return {"n": len(d), "slope": s.slope, "slope_t": s.slope / s.stderr,
                "mean": y.mean(), "t_mean": y.mean() / (y.std() / np.sqrt(len(y)))}
    rs = []
    prof = cs[cs["inprof"]]
    rises = prof[prof["sc"] > 0]
    for h in H:
        for name, d in [("profile_all", prof), ("profile_rises", rises),
                        ("profile_rises_no_w18", rises[rises["win"] != "w18"]),
                        ("tested_cases", cs[cs["f"] > 0]),
                        ("tested_no_w18", cs[(cs["f"] > 0) & (cs["win"] != "w18")]),
                        ("nonprofile_rises", cs[(~cs["inprof"]) & (cs["sc"] > 0)])]:
            r = reg(d, "sc", f"x{h}"); r.update({"h": h, "set": name}); rs.append(r)
    out["grading_scaled_rise"] = pd.DataFrame(rs)
    d = rises.dropna(subset=["x7", "sc"]).copy()
    d["q"] = pd.qcut(d["sc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["profile_rises_by_sc_quartile_x7"] = d.groupby("q").agg(n=("x7", "size"), mean_x7=("x7", "mean"),
                                                                 mean_x21=("x21", "mean"), sc=("sc", "mean"))
    out["profile_rises_r30_grading"] = pd.DataFrame([dict(reg(rises, "r30", "x7"), h=7), dict(reg(rises, "r30", "x21"), h=21)])
    out["profile_rises_by_year_x7"] = rises.dropna(subset=["x7"]).groupby("year")["x7"].agg(["size", "mean"])
    out["tested_r30_grading"] = pd.DataFrame([dict(reg(cs[cs["f"] > 0], "r30", "x7"), h=7)])
    return out
