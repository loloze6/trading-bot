def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r24 = c / c.shift(24) - 1
            m = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / m
            r720 = c / c.shift(720) - 1
            vol_s = c.pct_change().rolling(72).std()
            vol_l = c.pct_change().rolling(720).std()
            df = pd.DataFrame({"z": z, "r720": r720, "vr": vol_s / vol_l,
                               "alloc": b["postRebalance_current_allocation"]})
            for h in (24, 72, 120):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df = df.iloc[::24]
            df["coin"] = coin; df["win"] = w
            rows.append(df)
    D = pd.concat(rows)
    # normalise forward returns by coin's drift / usual move
    for h in (24, 72, 120):
        g = D.groupby("coin")[f"f{h}"]
        D[f"u{h}"] = (D[f"f{h}"] - g.transform("mean")) / g.transform("std")
    D = D.dropna(subset=["z", "f24"])
    D["zb"] = pd.cut(D["z"], [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 2, 99])
    t = D.groupby("zb", observed=True).agg(n=("f24", "size"), f24=("f24", "mean"), u24=("u24", "mean"),
                                           u72=("u72", "mean"), u120=("u120", "mean"))
    out["by_drop_multiple"] = t
    dr = D[D["z"] < -1].copy()
    dr["trend"] = pd.qcut(dr["r720"], 3, labels=["down30d", "mid", "up30d"])
    out["drops_by_30d_trend"] = dr.groupby("trend", observed=True).agg(
        n=("f24", "size"), f24=("f24", "mean"), u24=("u24", "mean"), u72=("u72", "mean"), u120=("u120", "mean"))
    dr["volr"] = pd.qcut(dr["vr"], 3, labels=["calm", "mid", "hot"])
    out["drops_by_vol_ratio"] = dr.groupby("volr", observed=True).agg(
        n=("f24", "size"), f24=("f24", "mean"), u24=("u24", "mean"), u72=("u72", "mean"))
    out["drops_by_coin"] = dr.groupby("coin").agg(n=("f24", "size"), f24=("f24", "mean"), u24=("u24", "mean"))
    # book: days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dd.append(d)
    DD = pd.concat(dd)
    pw = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    pw = pw.reset_index()
    pw["wn"] = pw["win"].str[1:].astype(int)
    pw = pw.sort_values(["wn", "day"])
    out["book_vs_hold_by_window"] = pw.groupby("wn").agg(book=("book_return", "mean"), hold=("coin_return", "mean"),
                                                        bsd=("book_return", "std"))
    eq = (1 + pw["book_return"]).cumprod()
    ddn = eq / eq.cummax() - 1
    out["deepest_fall"] = float(ddn.min())
    pw["dd"] = ddn.values
    out["windows_in_deepest_10pct_dd"] = pw[pw["dd"] < ddn.min() * 0.5].groupby("wn").agg(
        days=("dd", "size"), book=("book_return", "mean"), hold=("coin_return", "mean"))
    # book returns on days by coin trend (corr)
    out["corr_book_hold_daily"] = float(pw["book_return"].corr(pw["coin_return"]))
    return out
