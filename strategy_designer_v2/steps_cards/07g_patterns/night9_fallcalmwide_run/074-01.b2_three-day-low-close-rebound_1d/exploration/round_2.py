import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"]; r1 = c.pct_change()
            std30 = r1.rolling(30).std()
            rng = (d["high"] - d["low"])
            out = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(d)),
                                "day": pd.to_datetime(d["timestamp"]).dt.floor("D"),
                                "yr": pd.to_datetime(d["timestamp"]).dt.year,
                                "width": rng / c / std30,
                                "loc": (d["high"] - c) / rng.replace(0, np.nan),
                                "ret": r1 / std30.shift(1),
                                "tr60": c / c.shift(60) - 1,
                                "inprof": d["regime"] != "chop"})
            for h in (1, 2, 3):
                out[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3):
        dr = A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    def ct(sub, h):
        s = sub[sub["pos"] % h == 0].dropna(subset=[f"u{h}"])
        if len(s) < 3: return (len(s), 0, np.nan, np.nan)
        dd = s.groupby("day")[f"u{h}"].sum()
        nd = len(dd)
        t = dd.mean() / (dd.std() / np.sqrt(nd)) * 1.0 if nd > 2 else np.nan
        return (len(s), nd, s[f"u{h}"].mean(), t)
    up = A["tr60"] > 0.10; dn = A["tr60"] < -0.10
    wide = A["width"] >= 2
    res = {}
    # 1: in-profile low-close days, graded by width (all locations >=0.75)
    sub = A[A["inprof"] & up & (A["loc"] >= 0.75)].copy()
    sub["wb"] = pd.cut(sub["width"], [0, 1, 1.5, 2, 3, np.inf])
    r = []
    for b, g in sub.groupby("wb", observed=True):
        for h in (1, 3):
            n, nd, mu, t = ct(g, h); r.append({"wb": str(b), "h": h, "n": n, "days": nd, "u": mu, "t": t})
    res["inprof_lowclose_by_width"] = pd.DataFrame(r).round(4)
    # 2: in-profile wide days by location bins, h1
    sub = A[A["inprof"] & up & wide].copy()
    sub["lb"] = pd.cut(sub["loc"], [-0.01, 0.25, 0.5, 0.75, 0.9, 1.01])
    r = []
    for b, g in sub.groupby("lb", observed=True):
        for h in (1, 3):
            n, nd, mu, t = ct(g, h); r.append({"lb": str(b), "h": h, "n": n, "days": nd, "u": mu, "t": t})
    res["inprof_wide_by_loc"] = pd.DataFrame(r).round(4)
    # 3: in-profile wide low close: by year, h1 and h2
    sub = A[A["inprof"] & up & wide & (A["loc"] >= 0.75)]
    r = []
    for y, g in sub.groupby("yr"):
        for h in (1, 2):
            n, nd, mu, t = ct(g, h); r.append({"yr": y, "h": h, "n": n, "days": nd, "u": mu, "t": t})
    res["inprof_wideLow_by_year"] = pd.DataFrame(r).round(4)
    r = []
    for h in (1, 2, 3):
        n, nd, mu, t = ct(sub, h); r.append({"h": h, "n": n, "days": nd, "u": mu, "t": t})
    res["inprof_wideLow_horizons_clustered"] = pd.DataFrame(r).round(4)
    # 4: falling market wide high close fade, graded by width and loc
    sub = A[dn & (A["loc"] <= 0.25)].copy()
    sub["wb"] = pd.cut(sub["width"], [0, 1, 1.5, 2, 3, np.inf])
    r = []
    for b, g in sub.groupby("wb", observed=True):
        for h in (1, 3):
            n, nd, mu, t = ct(g, h); r.append({"wb": str(b), "h": h, "n": n, "days": nd, "u": mu, "t": t})
    res["falling_highclose_by_width"] = pd.DataFrame(r).round(4)
    sub = A[dn & wide & (A["loc"] <= 0.25)]
    r = []
    for y, g in sub.groupby("yr"):
        n, nd, mu, t = ct(g, 1); r.append({"yr": y, "n": n, "days": nd, "u1": mu, "t": t})
    res["falling_wideHigh_by_year_h1"] = pd.DataFrame(r).round(4)
    r = []
    for k, m in {"inprof": A["inprof"], "outprof": ~A["inprof"]}.items():
        n, nd, mu, t = ct(sub[m.loc[sub.index]], 1); r.append({"k": k, "n": n, "days": nd, "u1": mu, "t": t})
    res["falling_wideHigh_inprof_split"] = pd.DataFrame(r).round(4)
    # 5: sharp down z in rising market, h1
    sub = A[up].copy()
    sub["zb"] = pd.cut(sub["ret"], [-np.inf, -3, -2, -1, 1, 2, np.inf])
    r = []
    for b, g in sub.groupby("zb", observed=True):
        for k, m in {"in": g["inprof"], "out": ~g["inprof"]}.items():
            n, nd, mu, t = ct(g[m], 1); r.append({"zb": str(b), "prof": k, "n": n, "days": nd, "u1": mu, "t": t})
    res["rising_z_h1"] = pd.DataFrame(r).round(4)
    return res
