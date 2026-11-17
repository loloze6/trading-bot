import pandas as pd, numpy as np
from scipy import stats

def tt(v):
    v = pd.Series(v).dropna()
    return v.mean() / v.std() * np.sqrt(len(v)) if len(v) > 2 else np.nan

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float); hi = b["high"].astype(float); vol = b["volume"].astype(float)
            r1 = cl.pct_change()
            d = pd.DataFrame({"coin": c, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b))})
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            for L in (10, 30, 60, 90):
                d[f"dist{L}"] = cl / hi.shift(1).rolling(L).max() - 1
            d["volz"] = np.log(vol.rolling(5).mean() / vol.shift(5).rolling(30).mean())
            d["vol20"] = r1.rolling(20).std()
            for h in (5, 10, 20, 30):
                d[f"f{h}"] = cl.shift(-h) / cl - 1
            # break of prior 30d high: does close stay above that level 10 bars later
            lvl = hi.shift(1).rolling(30).max()
            d["brk"] = (cl > lvl).astype(float)
            d["hold10"] = (cl.shift(-10) > lvl).astype(float).where(cl.shift(-10).notna())
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # robustness across grid offsets, h=10, dist30 top quintile vs rest
    off = []
    for o in range(10):
        g = D[(D["pos"] - o) % 10 == 0].dropna(subset=["dist30", "f10"]).copy()
        g["x"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
        g["q"] = pd.qcut(g["dist30"], 5, labels=False)
        sl = stats.linregress(g["dist30"], g["x"])
        off.append({"off": o, "top_x": g.loc[g.q == 4, "x"].mean(), "top_t": tt(g.loc[g.q == 4, "x"]),
                    "slope_t": sl.slope / sl.stderr, "n": len(g)})
    out["grid_offsets_h10"] = pd.DataFrame(off)
    # horizons and lookbacks: top quintile excess, slope t
    hz = []
    for h in (5, 10, 20, 30):
        g = D[D["pos"] % h == 0].copy()
        g["x"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        for L in (10, 30, 60, 90):
            s = g.dropna(subset=[f"dist{L}", "x"]).copy()
            s["q"] = pd.qcut(s[f"dist{L}"], 5, labels=False)
            sl = stats.linregress(s[f"dist{L}"], s["x"])
            hz.append({"h": h, "L": L, "top_x": s.loc[s.q == 4, "x"].mean(), "top_t": tt(s.loc[s.q == 4, "x"]),
                       "q0_x": s.loc[s.q == 0, "x"].mean(), "slope_t": sl.slope / sl.stderr, "n": len(s)})
    out["horizon_lookback"] = pd.DataFrame(hz)
    # h=10, dist30: by coin and by year (top quintile pooled threshold)
    g = D[D["pos"] % 10 == 0].dropna(subset=["dist30", "f10"]).copy()
    g["x"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
    g["q"] = pd.qcut(g["dist30"], 5, labels=False)
    top = g[g.q == 4]
    out["top_by_coin"] = top.groupby("coin")["x"].agg(["mean", "count", tt])
    out["top_by_year"] = top.groupby("year")["x"].agg(["mean", "count", tt])
    out["top_by_windowthird"] = top.assign(t3=pd.cut(top.wn, [0, 8, 16, 24])).groupby("t3")["x"].agg(["mean", "count", tt])
    # graded inside near-high: dist30 > -0.05 slope
    nh = g[g.dist30 > -0.05]
    sl = stats.linregress(nh["dist30"], nh["x"])
    out["near_high_slope"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(nh)})
    # volume interaction in top quintile
    tv = top.dropna(subset=["volz"]).copy()
    tv["vh"] = tv["volz"] > tv["volz"].median()
    out["top_by_volume"] = tv.groupby("vh")["x"].agg(["mean", "count", tt])
    tv2 = top.dropna(subset=["vol20"]).copy()
    tv2["vh"] = tv2["vol20"] > g["vol20"].median()
    out["top_by_vol20"] = tv2.groupby("vh")["x"].agg(["mean", "count", tt])
    # break continuation
    bk = g[g.brk == 1].dropna(subset=["hold10"])
    out["break30_hold10_share"] = pd.Series({"share_above": bk["hold10"].mean(), "n": len(bk), "x_mean": bk["x"].mean(), "t": tt(bk["x"])})
    return out
