def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    mu = {}
    for c, ws in bars.items():
        mu[c] = pd.concat([df["close"].pct_change().dropna() for df in ws.values()]).mean()
    rows = []
    blocks = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].values
            a = df["postRebalance_current_allocation"].fillna(0).values
            n = len(df)
            on = f > 0
            # days since forecast turned on (run length), -1 if off
            run = np.full(n, -1); k = -1
            for i in range(n):
                if on[i]:
                    k = k + 1 if k >= 0 else 0
                else:
                    k = -1
                run[i] = k
            r1 = pd.Series(cl).pct_change()
            vol20 = r1.rolling(20).std().values
            ret20past = pd.Series(cl).pct_change(20).values
            ex20 = np.full(n, np.nan)
            for i in range(n - 20):
                ex20[i] = cl[i + 20] / cl[i] - 1 - 20 * mu[c]
            for s in range(0, n, 20):
                idx = [i for i in range(s, min(s + 20, n)) if not np.isnan(ex20[i])]
                if not idx: continue
                bs = sum(a[i] * ex20[i] for i in idx)
                blocks.append((c, w, bs, any(a[i] != 0 for i in idx), np.mean(a[idx])))
            for i in range(0, n - 20, 20):
                rows.append((c, w, f[i], a[i], run[i], vol20[i], ret20past[i], ex20[i]))
    R = pd.DataFrame(rows, columns=["coin", "win", "f", "a", "run", "vol", "past20", "ex"])
    B = pd.DataFrame(blocks, columns=["coin", "win", "bs", "nz", "ma"])
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "med_ex": g.ex.median(),
                          "share_pos": (g.ex > 0).mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out = {}
    on = R[R.f > 0].copy()
    on["age"] = pd.cut(on.run, [-1, 19, 59, 149, 10000], labels=["0-19d", "20-59d", "60-149d", "150d+"])
    out["on_by_age"] = on.groupby("age").apply(summ)
    on["vq"] = pd.qcut(on.vol.rank(method="first"), 3, labels=["lowvol", "midvol", "highvol"])
    out["on_by_vol"] = on.groupby("vq").apply(summ)
    on["pq"] = pd.qcut(on.past20.rank(method="first"), 3, labels=["p_low", "p_mid", "p_high"])
    out["on_by_past20"] = on.groupby("pq").apply(summ)
    # allocation-weighted on grid
    out["on_alloc_weighted_mean_ex"] = float((on.a * on.ex).sum() / on.a.sum())
    out["on_mean_alloc_by_vol"] = on.groupby("vq").a.mean()
    # block-level
    Bn = B.copy()
    out["blocks_by_coin"] = Bn.groupby("coin").bs.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    top = Bn.bs.sort_values(ascending=False)
    out["block_mean_all"] = float(Bn.bs.mean())
    out["block_mean_drop_top10"] = float(top.iloc[10:].mean())
    out["block_t_drop_top10"] = float(top.iloc[10:].mean() / (top.iloc[10:].std() / np.sqrt(len(top) - 10)))
    # book decomposition
    dd = []
    for c, ws in days.items():
        for w, d in ws.items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d2 = d.copy(); d2["day"] = pd.to_datetime(d2["day"]).dt.floor("D")
            d2 = d2.merge(al.rename("al").reset_index(), on="day", how="left")
            d2["coin"] = c
            dd.append(d2)
    D = pd.concat(dd)
    D = D.dropna(subset=["book_return", "coin_return"])
    mud = D.groupby("coin").coin_return.mean()
    D["drift"] = D.al.fillna(0) * D.coin.map(mud)
    out["book_mean_daily"] = float(D.book_return.mean())
    out["book_drift_part"] = float(D.drift.mean())
    out["book_timing_part"] = float(D.book_return.mean() - D.drift.mean())
    return out
