def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin drift/usual per horizon
        per_h = {}
        for h in (18, 72):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs)
            per_h[h] = (rs.mean(), rs.std()) if len(rs) > 2 else (np.nan, np.nan)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            r1 = np.log(c).diff()
            maxh12 = hi.shift(1).rolling(12).max()
            minl12 = lo.shift(1).rolling(12).min()
            brk_up = (c > maxh12).astype(float)
            brk_dn = (c < minl12).astype(float)
            width = (hi.rolling(12).max() - lo.rolling(12).min()) / c
            width_rel = width / width.rolling(360, min_periods=120).median()
            vol42 = r1.rolling(42).std()
            vol_rel = vol42 / vol42.rolling(360, min_periods=120).median()
            ret42 = c / c.shift(42) - 1
            ret42z = ret42 / (vol42 * np.sqrt(42))
            ret6 = c / c.shift(6) - 1
            ret6z = ret6 / (vol42 * np.sqrt(6))
            ts = pd.to_datetime(df["timestamp"])
            for h in (18, 72):
                d, u = per_h[h]
                idx = np.arange(0, len(c) - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                sub = pd.DataFrame({
                    "coin": coin, "w": w, "h": h,
                    "fwd": fwd, "unus": fwd - d, "str": (fwd - d) / u,
                    "absstr": np.abs(fwd - d) / u,
                    "brk_up": brk_up.values[idx], "brk_dn": brk_dn.values[idx],
                    "width_rel": width_rel.values[idx], "vol_rel": vol_rel.values[idx],
                    "ret42z": ret42z.values[idx], "ret6z": ret6z.values[idx],
                    "wd": ts.dt.weekday.values[idx], "hr": ts.dt.hour.values[idx],
                    "year": ts.dt.year.values[idx],
                    "fc": df["forecast"].values[idx],
                })
                rows.append(sub)
    A = pd.concat(rows, ignore_index=True)

    def grp(df, col, q=5, val="str"):
        d = df.dropna(subset=[col, val]).copy()
        if q:
            d["g"] = d.groupby("coin")[col].transform(
                lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        else:
            d["g"] = d[col]
        o = d.groupby("g")[val].agg(["mean", "std", "count"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.drop(columns="std").round(4)

    out = {}
    for h in (18, 72):
        D = A[A.h == h]
        out[f"h{h}_ret42z_q"] = grp(D, "ret42z")
        out[f"h{h}_ret6z_q"] = grp(D, "ret6z")
        out[f"h{h}_volrel_q"] = grp(D, "vol_rel")
        out[f"h{h}_width_q_abs"] = grp(D, "width_rel", val="absstr")
        out[f"h{h}_brkup"] = grp(D, "brk_up", q=0)
        out[f"h{h}_brkdn"] = grp(D, "brk_dn", q=0)
        out[f"h{h}_year"] = grp(D, "year", q=0)
    D = A[A.h == 18]
    out["h18_weekday"] = grp(D, "wd", q=0)
    # breakout direction by width tercile (h18)
    d = D.dropna(subset=["width_rel"]).copy()
    d["wq"] = d.groupby("coin")["width_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["dir"] = d["brk_up"] - d["brk_dn"]
    dd = d[d["dir"] != 0].copy()
    dd["signed"] = dd["str"] * dd["dir"]
    o = dd.groupby("wq")["signed"].agg(["mean", "std", "count"])
    o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["h18_breakdir_by_width"] = o.round(4)
    d72 = A[A.h == 72].dropna(subset=["width_rel"]).copy()
    d72["wq"] = d72.groupby("coin")["width_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d72["dir"] = d72["brk_up"] - d72["brk_dn"]
    dd = d72[d72["dir"] != 0].copy()
    dd["signed"] = dd["str"] * dd["dir"]
    o = dd.groupby("wq")["signed"].agg(["mean", "std", "count"])
    o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["h72_breakdir_by_width"] = o.round(4)
    # book: daily
    dl = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.dropna(subset=["book_return", "coin_return"])
            dl.append(pd.DataFrame({"coin": coin, "year": pd.to_datetime(x["day"]).dt.year.values,
                                    "b": x["book_return"].values, "c": x["coin_return"].values}))
    B = pd.concat(dl)
    by = B.groupby("year").agg(book=("b", "mean"), hold=("c", "mean"), n=("b", "count"))
    by["book_sharpe"] = B.groupby("year")["b"].apply(lambda s: s.mean() / s.std() * np.sqrt(365))
    by["hold_sharpe"] = B.groupby("year")["c"].apply(lambda s: s.mean() / s.std() * np.sqrt(365))
    out["book_by_year"] = by.round(5)
    by2 = B.groupby("coin").agg(book=("b", "mean"), hold=("c", "mean"))
    out["book_by_coin"] = by2.round(5)
    return out
