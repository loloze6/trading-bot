def explore(data):
    import numpy as np, pandas as pd
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = {1: [], 3: [], 5: [], 10: []}
        frames = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            o, h, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = (h - l)
            mr20 = rng.rolling(20, min_periods=20).mean()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": np.arange(len(b)),
                "rr": rng / mr20,
                "flat": 1 - (c - o).abs() / rng.replace(0, np.nan),
                "loc": (c - l) / rng.replace(0, np.nan),
                "rise6": c / c.shift(6) - 1,
                "rise5p": c.shift(1) / c.shift(6) - 1,
                "r1": c / c.shift(1) - 1,
            })
            df["vol20"] = df["r1"].rolling(20, min_periods=20).std()
            df["z1"] = df["r1"] / df["vol20"].shift(1)
            for H in (1, 3, 5, 10):
                df[f"f{H}"] = c.shift(-H) / c - 1
                g = c.iloc[::H]
                rets[H] += list((g.shift(-1) / g - 1).dropna())
            df["wd"] = df["day"].dt.weekday
            df["cell3"] = df["pos"] // 3
            frames.append(df)
        drift[coin] = {H: (np.mean(rets[H]), np.std(rets[H], ddof=1)) for H in rets}
        rows.append(pd.concat(frames))
    A = pd.concat(rows, ignore_index=True)
    for H in (1, 3, 5, 10):
        A[f"u{H}"] = A[f"f{H}"] - A["coin"].map(lambda k: drift[k][H][0])
        A[f"s{H}"] = A[f"u{H}"] / A["coin"].map(lambda k: drift[k][H][1])

    def stat(mask, H=3, sign=1, dedup=True):
        d = A[mask & A[f"u{H}"].notna()].copy()
        if dedup:
            d["cellH"] = d["pos"] // H
            d = d.drop_duplicates(["coin", "win", "cellH"])
        if len(d) < 5:
            return pd.Series({"n": len(d)})
        u = sign * d[f"u{H}"]
        m = u.mean()
        g = (u - m).groupby(d["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(u) if D > 1 else np.nan
        return pd.Series({"n": len(d), "days": D, "mean_unusual": m, "t": m / se,
                          "strength": (sign * d[f"s{H}"]).mean(), "hit": (u > 0).mean()})

    out = {}
    wide = A["rr"] >= 1.5
    flat = A["flat"] >= 0.9
    up = A["rise6"] > 0
    rs = {}
    rs["wideflat_up"] = stat(wide & flat & up)
    rs["wideflat_down"] = stat(wide & flat & ~up)
    rs["wideflat_all"] = stat(wide & flat)
    rs["narrowflat_up(rr<1)"] = stat((A["rr"] < 1) & flat & up)
    rs["wide_nonflat_up(flat<0.5)"] = stat(wide & (A["flat"] < 0.5) & up)
    rs["wide_any_up"] = stat(wide & up)
    rs["wide_any_down"] = stat(wide & ~up)
    rs["all_bars_grid"] = stat(A["rr"].notna() & (A["pos"] % 3 == 0), dedup=False)
    out["1 situations, 3d long unusual"] = pd.DataFrame(rs).T

    hz = {}
    for H in (1, 3, 5, 10):
        hz[f"wideflat_up_h{H}"] = stat(wide & flat & up, H=H)
        hz[f"wideflat_down_h{H}"] = stat(wide & flat & ~up, H=H)
    out["2 horizons"] = pd.DataFrame(hz).T

    fb = {}
    for lo, hi in [(0, .3), (.3, .6), (.6, .8), (.8, .9), (.9, 1.01)]:
        fb[f"wide_up_flat{lo}-{hi}"] = stat(wide & up & (A["flat"] >= lo) & (A["flat"] < hi))
    out["3 flatness bins, wide up-run"] = pd.DataFrame(fb).T

    rb = {}
    for lo, hi in [(0, .7), (.7, 1), (1, 1.3), (1.3, 1.7), (1.7, 2.5), (2.5, 99)]:
        rb[f"rr{lo}-{hi}"] = stat((A["rr"] >= lo) & (A["rr"] < hi) & (A["pos"] % 3 == 0), dedup=False)
    out["4 range ratio bins, all grid"] = pd.DataFrame(rb).T

    lb = {}
    for lo, hi in [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)]:
        lb[f"loc{lo}-{hi}"] = stat(wide & (A["loc"] >= lo) & (A["loc"] < hi))
    out["5 close location in range, wide days"] = pd.DataFrame(lb).T

    zb = {}
    for lo, hi in [(-99, -2.5), (-2.5, -1.5), (-1.5, -.5), (-.5, .5), (.5, 1.5), (1.5, 2.5), (2.5, 99)]:
        zb[f"z{lo}-{hi}"] = stat((A["z1"] >= lo) & (A["z1"] < hi))
    out["6 after 1d move z bins"] = pd.DataFrame(zb).T

    out["7 weekday, all grid"] = pd.DataFrame({f"wd{d}": stat((A["wd"] == d) & (A["pos"] % 3 == 0), dedup=False) for d in range(7)}).T
    out["8 rise6 bins, wide days"] = pd.DataFrame({f"rise6_{lo}-{hi}": stat(wide & (A["rise6"] >= lo) & (A["rise6"] < hi))
                                                  for lo, hi in [(-9, -.15), (-.15, -.05), (-.05, 0), (0, .05), (.05, .15), (.15, 9)]}).T
    return out
