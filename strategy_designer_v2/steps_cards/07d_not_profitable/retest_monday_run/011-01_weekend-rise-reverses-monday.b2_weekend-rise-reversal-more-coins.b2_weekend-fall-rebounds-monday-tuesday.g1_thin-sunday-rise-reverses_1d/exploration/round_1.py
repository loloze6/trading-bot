def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    v = (1 + B["book_return"]).cumprod(); dd = v / v.cummax() - 1
    B["dd"] = dd.values
    out["book_by_window"] = B.groupby(level=0).agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), mindd=("dd", "min"), n=("book_return", "size"))
    # cases
    cs = []
    for c, ws in data["bars"].items():
        drift_parts = []
        for w, b in ws.items():
            cl = b["close"].values
            drift_parts += list(cl[2::2][:len(cl[0::2][:len(cl[2::2])])] / cl[0::2][:len(cl[2::2])] - 1)
        drift = np.mean(drift_parts); usual = np.std(drift_parts)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; ts = pd.to_datetime(b["timestamp"])
            f2 = cl.shift(-2) / cl - 1
            r1 = cl / cl.shift(1) - 1
            r20 = cl / cl.shift(20) - 1
            r7 = cl / cl.shift(7) - 1
            vr = b["volume"].shift(1).rolling(60, min_periods=20).mean() / b["volume"]
            absm = r1.abs().rolling(60, min_periods=20).mean()
            vol20 = r1.rolling(20).std()
            fri = cl.shift(2) / cl.shift(3) - 1  # sat rise (bar before)
            sat = cl.shift(1) / cl.shift(2) - 1
            alloc = b["postRebalance_current_allocation"]
            t = pd.DataFrame({"coin": c, "w": w, "sun": ts.dt.weekday == 6, "fc": b["forecast"], "f2": f2, "r1": r1 / absm,
                              "r20": r20, "r7": r7, "vr": vr, "sat": sat, "vol20": vol20, "alloc": alloc,
                              "year": ts.dt.year, "drift": drift, "usual": usual})
            cs.append(t)
    C = pd.concat(ignore_index=True, objs=cs)
    C["un"] = -(C["f2"] - C["drift"])
    C["tot"] = -C["f2"]
    S = C[C["sun"] & (C["fc"] < 0)].dropna(subset=["f2"])
    def g(df, col, q=5):
        x = df.copy(); x["q"] = pd.qcut(x[col], q, duplicates="drop", labels=False)
        return x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), un=("un", "mean"), tot=("tot", "mean"), n=("un", "size"),
                                  t=("un", lambda s: s.mean() / s.std() * np.sqrt(len(s))), alloc=("alloc", "mean"))
    out["by_r20"] = g(S, "r20")
    out["by_r7"] = g(S, "r7")
    out["by_rise"] = g(S, "r1")
    out["by_vr"] = g(S, "vr")
    out["by_vol20"] = g(S, "vol20")
    out["by_year"] = S.groupby("year").agg(un=("un", "mean"), tot=("tot", "mean"), n=("un", "size"))
    # condition alone: non-Sunday-rise bars (2-bar grid approx all), by r20 quintile on same cuts
    N = C[~(C["sun"] & (C["fc"] < 0))].dropna(subset=["f2", "r20"])
    N = N.iloc[::2]
    cuts = S["r20"].quantile([0, .2, .4, .6, .8, 1]).values
    cuts[0] = -np.inf; cuts[-1] = np.inf
    N["q"] = pd.cut(N["r20"], cuts, labels=False)
    out["nosignal_by_r20"] = N.groupby("q").agg(un=("un", "mean"), n=("un", "size"))
    # Sunday falls: do they rebound? (other side)
    F = C[C["sun"] & (C["r1"] < 0)].dropna(subset=["f2"])
    out["sunday_fall_long_unusual"] = pd.Series({"mean_long_unusual": -F["un"].mean(), "t": -F["un"].mean() / F["un"].std() * np.sqrt(len(F)), "n": len(F)})
    # trades
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.Series({"n": len(tr), "mean_gross": tr["profit_loss_percent"].mean(), "mean_net": tr["net_profit_loss_percent"].mean(),
                               "dur_days_mean": tr["duration_minutes"].mean() / 1440, "share_short": (tr["side"] == "SHORT").mean()})
    return out
