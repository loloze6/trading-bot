def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # coin mean daily return over all windows
    cm = {}
    for c in bars:
        r = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        cm[c] = r.mean()
    # bar-level decomposition (1d bars): position gain vs drift part
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].fillna(0)
            nxt = b["close"].shift(-1) / b["close"] - 1
            d = pd.DataFrame({"coin": c, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "pos": pos, "ret": nxt, "fc": b["forecast"], "regime": b["regime"],
                              "close": b["close"]})
            d["gain"] = d["pos"] * d["ret"]
            d["drift"] = d["pos"] * cm[c]
            # 60d trend recomputed within window (approx, only from available bars)
            d["tr60"] = d["close"] / d["close"].shift(60) - 1
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["ret"])
    out["overall"] = pd.Series({"mean_gain": D.gain.mean(), "mean_drift_part": D.drift.mean(),
                                "timing": D.gain.mean() - D.drift.mean(),
                                "share_long": (D.pos > 0).mean(), "share_short": (D.pos < 0).mean(),
                                "mean_pos_when_in": D.pos[D.pos != 0].mean()})
    g = D.groupby("coin").agg(gain=("gain", "sum"), drift=("drift", "sum"), n=("gain", "size"),
                              inpos=("pos", lambda x: (x != 0).mean()))
    g["share_of_total_gain"] = g.gain / g.gain.sum()
    out["by_coin"] = g.sort_values("gain", ascending=False)
    gw = D.groupby("win").agg(gain=("gain", "sum"), drift=("drift", "sum"),
                              coinret=("ret", "mean"), inpos=("pos", lambda x: (x != 0).mean()))
    out["by_window"] = gw
    gy = D.groupby("year").agg(gain=("gain", "sum"), drift=("drift", "sum"), coinret=("ret", "mean"))
    out["by_year"] = gy
    # forecast slope at several horizons, in-regime, non-overlapping grid
    res = []
    for h in [1, 3, 5, 10, 20]:
        xs, ys, ds = [], [], []
        for c in bars:
            # drift per h
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                allr += list(cl[idx + h] / cl[idx] - 1)
            dr = np.mean(allr) if allr else 0
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                f = b["forecast"].values[idx]; reg = b["regime"].values[idx]
                m = (reg == "unknown") & ~np.isnan(f)
                xs += list(f[m]); ys += list(cl[idx + h][m] / cl[idx][m] - 1 - dr)
        xs = np.array(xs); ys = np.array(ys)
        sl = stats.linregress(xs, ys)
        hi = ys[xs > 5]; lo = ys[(xs < 0)]
        res.append({"h": h, "n": len(xs), "slope": sl.slope, "t": sl.slope / sl.stderr,
                    "mean_all": ys.mean(), "t_all": ys.mean() / (ys.std(ddof=1) / np.sqrt(len(ys))),
                    "mean_fc_gt5": hi.mean(), "mean_fc_lt0": lo.mean(), "n_lt0": len(lo)})
    out["horizons"] = pd.DataFrame(res)
    # forecast bins at 5 days
    xs, ys = [], []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b["close"].values
            idx = np.arange(0, len(cl) - 5, 5)
            f = b["forecast"].values[idx]; reg = b["regime"].values[idx]
            m = (reg == "unknown") & ~np.isnan(f)
            xs += list(f[m]); ys += list(cl[idx + 5][m] / cl[idx][m] - 1 - cm[c] * 5)
    B = pd.DataFrame({"f": xs, "y": ys})
    B["bin"] = pd.qcut(B.f, 6, duplicates="drop")
    out["fc_bins_5d"] = B.groupby("bin").y.agg(["mean", "count", "std"])
    # gain by forecast bin daily
    Din = D[D.pos != 0].copy()
    Din["fbin"] = pd.qcut(Din.fc, 5, duplicates="drop")
    out["gain_by_fc_bin"] = Din.groupby("fbin").agg(gain=("gain", "mean"), drift=("drift", "mean"),
                                                    ret=("ret", "mean"), n=("gain", "size"))
    # top trades
    T = pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c]])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "share_long": (T.side == "LONG").mean(),
                               "sum": p.sum(), "top10_sum": p.head(10).sum(), "top20_sum": p.head(20).sum(),
                               "median": p.median(), "win_rate": (p > 0).mean()})
    return out
