def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data.get("bars", {}); days = data.get("days", {}); trades = data.get("trades", {})
    inv = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w]
            inv.append({"coin": c, "window": w, "rows": len(b), "cols": len(b.columns),
                        "has_close": "close" in b.columns,
                        "n_trades": len(trades.get(c, {}).get(w, [])) if c in trades else 0})
    out["inventory"] = pd.DataFrame(inv) if inv else "no bars"
    if not inv:
        return out
    out["bar_columns"] = ", ".join(list(next(iter(next(iter(bars.values())).values())).columns)[:40])
    H = 5
    rows = []
    allret = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w]
            if "close" not in b.columns or len(b) < 70:
                continue
            cl = b["close"].astype(float).reset_index(drop=True)
            r = cl.pct_change()
            sd = r.rolling(30).std().shift(1)
            z = r / sd
            tr60 = cl / cl.shift(60) - 1
            vol30 = r.rolling(30).std()
            volrank = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            fwd = cl.shift(-H) / cl - 1
            pos = b["postRebalance_current_allocation"].reset_index(drop=True) if "postRebalance_current_allocation" in b.columns else pd.Series(np.nan, index=cl.index)
            for i in range(0, len(cl) - H, H):
                allret.append({"coin": c, "fwd": fwd[i]})
            df = pd.DataFrame({"coin": c, "window": w, "i": np.arange(len(cl)), "z": z, "tr60": tr60,
                               "vr": volrank, "fwd": fwd, "pos": pos})
            df = df[(df.i % H) == 0]
            rows.append(df)
    if not rows:
        return out
    A = pd.concat(rows).dropna(subset=["z", "fwd"])
    drift = pd.DataFrame(allret).dropna().groupby("coin")["fwd"].mean()
    A["unus"] = A["fwd"] - A["coin"].map(drift)
    A["trend"] = np.where(A.tr60 > 0.10, "rising", np.where(A.tr60 < -0.10, "falling", "choppy"))
    A["agit"] = np.where(A.vr.isna(), "na", np.where(A.vr > 0.5, "agitated", "calm"))
    A["zbin"] = pd.cut(A.z, [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["by_zbin_all"] = A.groupby("zbin").apply(summ)
    out["by_zbin_agit"] = A.groupby(["agit", "zbin"]).apply(summ)
    out["by_zbin_trend"] = A.groupby(["trend", "zbin"]).apply(summ)
    out["by_profile"] = A.groupby(["trend", "agit"]).apply(summ)
    # sign-aligned follow-through: z * unus correlation per agitation
    cc = []
    for k, g in A.groupby("agit"):
        g = g.dropna(subset=["z", "unus"])
        if len(g) > 10:
            rr, p = stats.spearmanr(g.z, g.unus)
            cc.append({"agit": k, "n": len(g), "spearman_z_unus": rr, "p": p})
    out["corr_by_agit"] = pd.DataFrame(cc)
    # absolute big days: |z|>2 followed by sign-aligned move
    A["aligned"] = np.sign(A.z) * A.unus
    out["aligned_by_absz"] = A.assign(az=pd.cut(A.z.abs(), [0, 0.5, 1, 1.5, 2, 3, 99])).groupby(["agit", "az"]).apply(
        lambda g: summ(g.assign(unus=g.aligned)))
    # book
    bk = []
    for c in days:
        for w in days[c]:
            d = days[c][w]
            if len(d):
                bk.append({"coin": c, "n": d["book_return"].notna().sum(), "book_mean%": 100 * d["book_return"].mean(),
                           "coin_mean%": 100 * d["coin_return"].mean()})
    if bk:
        out["book_by_coin"] = pd.DataFrame(bk).groupby("coin").agg({"n": "sum", "book_mean%": "mean", "coin_mean%": "mean"})
    out["share_in_position"] = float((A.pos.fillna(0).abs() > 0).mean())
    return out
