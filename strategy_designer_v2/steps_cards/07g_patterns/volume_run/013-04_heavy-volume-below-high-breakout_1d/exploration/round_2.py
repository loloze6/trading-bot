def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change(); n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(n),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "ret20p": c / c.shift(20) - 1,
                "ret5p": c / c.shift(5) - 1,
                "vr": v.rolling(10).mean() / v.rolling(30).mean(),
                "vr90": v.rolling(10).mean() / v.rolling(90, min_periods=60).mean(),
                "vol20": r1.rolling(20).std(),
                "f1": c.shift(-1) / c - 1,
                "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                "f20": c.shift(-20) / c - 1,
            }))
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 5, 10, 20]:
        g = A[A.pos % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A.coin.map(m)

    def slope(g, var, y):
        g = g.dropna(subset=[var, y])
        if len(g) < 15: return [np.nan, len(g), np.nan]
        z = g.groupby("coin")[var].rank(pct=True)
        sl = stats.linregress(z, g[y])
        return [round(sl.slope, 4), len(g), round(sl.slope / sl.stderr, 2)]

    res = {}
    for var, h in [("vr", 5), ("vr", 10), ("vr", 20), ("vr90", 5), ("vr90", 10), ("vr90", 20), ("ret20p", 10), ("ret20p", 20), ("ret20p", 5)]:
        g = A[A.pos % h == 0]
        res[f"{var}_x{h}"] = slope(g, var, f"x{h}")
    out["slopes_pooled"] = pd.DataFrame(res, index=["slope", "n", "t"]).T

    pc = {}
    for coin in A.coin.unique():
        g5 = A[(A.pos % 5 == 0) & (A.coin == coin)]
        g10 = A[(A.pos % 10 == 0) & (A.coin == coin)]
        pc[coin] = slope(g5, "vr", "x5")[::2] + slope(g10, "ret20p", "x10")[::2]
    out["per_coin"] = pd.DataFrame(pc, index=["vr_x5_slope", "vr_x5_t", "r20_x10_slope", "r20_x10_t"]).T

    halves = {}
    for nm, cond in [("w1-12", A.wn <= 12), ("w13-24", A.wn > 12)]:
        g5 = A[(A.pos % 5 == 0) & cond]; g10 = A[(A.pos % 10 == 0) & cond]
        halves[nm] = slope(g5, "vr", "x5") + slope(g10, "ret20p", "x10")
    out["halves"] = pd.DataFrame(halves, index=["vr_s", "vr_n", "vr_t", "r20_s", "r20_n", "r20_t"]).T

    # joint regression vr + ret20p on x5
    g = A[A.pos % 5 == 0].dropna(subset=["vr", "ret20p", "x5", "vol20"]).copy()
    for v_ in ["vr", "ret20p", "vol20"]:
        g[v_ + "_z"] = g.groupby("coin")[v_].rank(pct=True)
    X = np.column_stack([np.ones(len(g)), g.vr_z, g.ret20p_z, g.vol20_z])
    beta, *_ = np.linalg.lstsq(X, g.x5, rcond=None)
    resid = g.x5 - X @ beta
    s2 = resid.var(ddof=4); cov = s2 * np.linalg.inv(X.T @ X)
    out["joint_x5"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))},
                                   index=["const", "vr", "ret20p", "vol20"]).round(4)
    # vr effect split by sign of ret5p
    sp = {}
    for nm, cond in [("up5", g.ret5p > 0), ("down5", g.ret5p <= 0)]:
        sp[nm] = slope(g[cond], "vr", "x5")
    out["vr_by_ret5_sign"] = pd.DataFrame(sp, index=["slope", "n", "t"]).T

    # weekday consistency by coin and halves
    W = A.dropna(subset=["x1"])
    out["weekday_by_coin"] = (W.pivot_table(index="coin", columns="wd", values="x1", aggfunc="mean") * 1e4).round(1)
    out["weekday_by_half"] = (W.assign(h=np.where(W.wn <= 12, "a", "b")).pivot_table(index="h", columns="wd", values="x1", aggfunc="mean") * 1e4).round(1)

    # book: what precedes largest gains/losses
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D = D[D.book_return != 0]
    D["q"] = pd.qcut(D.book_return.rank(method="first"), 10, labels=False)
    out["book_active_days_deciles"] = D.groupby("q").agg(n=("book_return", "size"), br=("book_return", "mean"), cr=("coin_return", "mean")).round(4)
    out["book_active_share_days"] = round(len(D) / sum(len(d) for ws in data["days"].values() for d in ws.values()), 4)
    return out
