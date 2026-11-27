def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            v30 = r1.rolling(30).std()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "vol30": v30,
                "agit": v30 > v30.expanding(30).median(),
                "choppy": (b["regime"] == "unknown"),
            })
            for H in (1, 3, 7):
                df[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def ct(s, days):
        s = pd.Series(s.values, index=days.values).dropna()
        if len(s) < 10: return (np.nan, np.nan, len(s))
        m = s.mean(); g = (s - m).groupby(level=0).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return (m, m / se, len(s))

    res = {}
    for H in (1, 3, 7):
        grid = A[A["pos"] % H == 0].dropna(subset=[f"f{H}", "r30"]).copy()
        drift = grid.groupby("coin")[f"f{H}"].mean(); sd = grid.groupby("coin")[f"f{H}"].std()
        grid["exs"] = (grid[f"f{H}"] - grid["coin"].map(drift)) / grid["coin"].map(sd)
        out = []
        for lab, sub in [("choppy r30<0", grid[grid.choppy & (grid.r30 < 0)]),
                         ("choppy r30>=0", grid[grid.choppy & (grid.r30 >= 0)]),
                         ("choppy r30<0 agit", grid[grid.choppy & (grid.r30 < 0) & grid.agit]),
                         ("choppy r30<0 calm", grid[grid.choppy & (grid.r30 < 0) & ~grid.agit]),
                         ("falling r30<0", grid[(grid.r60 < -0.10) & (grid.r30 < 0)]),
                         ("rising r30>=0", grid[(grid.r60 > 0.10) & (grid.r30 >= 0)])]:
            if len(sub) < 20: continue
            # graded: product of standardised r30 and excess (slope sign)
            z = (sub["r30"] - sub["r30"].mean()) / sub["r30"].std()
            m, t, n = ct(z * sub["exs"], sub["day"])
            m2, t2, _ = ct(sub["exs"], sub["day"])
            out.append({"grp": lab, "slope_cov": m, "t_slope": t, "mean_exs": m2, "t_mean": t2, "n": n})
        res[f"H={H}d: graded r30 -> excess"] = pd.DataFrame(out)
    return res
