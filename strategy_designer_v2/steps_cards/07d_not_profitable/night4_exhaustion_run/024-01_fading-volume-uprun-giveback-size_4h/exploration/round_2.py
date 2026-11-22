def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            grid.extend(list(c[idx + H] / c[idx] - 1))
        grid = np.array(grid); drift, usual = np.nanmean(grid), np.nanstd(grid)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]; r1 = c.pct_change()
            up = (r1 > 0).astype(int); dn = (r1 < 0).astype(int)
            # streak length
            def streak(s):
                g = (s != s.shift()).cumsum()
                return s.groupby(g).cumsum()
            df = pd.DataFrame({
                "upn": streak(up), "dnn": streak(dn),
                "fade": v.rolling(2).mean() < v.rolling(4).mean(),
                "sg": (c / c.shift(4) - 1) / r1.rolling(180).std(),
                "fwd": c.shift(-H) / c - 1, "cell": np.arange(len(b)) // H,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "r1next": c.shift(-1) / c - 1, "regime": b["regime"],
                "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["coin"] = coin; df["win"] = w
            df["unus"] = df["fwd"] - drift; df["drift1"] = drift / H
            rows.append(df)
    F = pd.concat(rows, ignore_index=True)
    A = F.dropna(subset=["fwd", "sg"])
    out = {}
    def tstat(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    # down streaks of >=4 any volume, graded by sg quintile, long direction
    D = A[A.dnn >= 4].groupby(["coin", "win", "cell"]).head(1).copy()
    D["q"] = pd.qcut(D["sg"], 4, labels=False)
    out["dn4_any_by_sg_q_long_unusual"] = D.groupby("q").apply(lambda s: pd.concat([tstat(s.unus), pd.Series({"sg": s.sg.mean(), "total": s.fwd.mean()})]))
    out["dn4_any_by_fade_q0"] = D[D.q == 0].groupby("fade").apply(lambda s: tstat(s.unus))
    out["dn4_q0_by_year"] = D[D.q == 0].groupby("year")["unus"].agg(["size", "mean"])
    out["dn4_q0_by_coin"] = D[D.q == 0].groupby("coin")["unus"].agg(["size", "mean"])
    # correlation of sg with unusual inside down streaks
    out["dn4_corr_sg_unus"] = float(np.corrcoef(D.sg, D.unus)[0, 1])
    U = A[A.upn >= 4].groupby(["coin", "win", "cell"]).head(1).copy()
    U["q"] = pd.qcut(U["sg"], 4, labels=False)
    out["up4_any_by_sg_q_long_unusual"] = U.groupby("q").apply(lambda s: pd.concat([tstat(s.unus), pd.Series({"sg": s.sg.mean()})]))
    # book: where does gain come from
    F["gain"] = F.alloc * F.r1next
    F["mkt"] = F.alloc * F.drift1
    F["state"] = np.where(F.fc < 0, "fc_short", np.where(F.alloc.abs() > 1e-9, "held_fc0", "flat"))
    out["book_by_state"] = F.groupby("state").agg(bars=("gain", "size"), alloc=("alloc", "mean"),
        gain_per_bar=("gain", "mean"), mkt_part=("mkt", "mean"))
    out["regime_counts_when_fc_nonzero"] = F[F.fc != 0].regime.value_counts()
    out["long_alloc_share_active"] = float((F.alloc > 1e-9).sum() / (F.alloc.abs() > 1e-9).sum())
    return out
