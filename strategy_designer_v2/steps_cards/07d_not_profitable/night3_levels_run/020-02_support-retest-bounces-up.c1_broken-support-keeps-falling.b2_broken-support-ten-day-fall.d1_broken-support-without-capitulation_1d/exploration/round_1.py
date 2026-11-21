def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    # coin mean daily return over all windows
    rows = []
    cell_rows = []
    trd = []
    for coin, wins in data["bars"].items():
        dr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        mu_d = dr.mean()
        # coin's 10-bar mean on grid
        g_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            g_all += list(c[idx + H] / c[idx] - 1)
        mu10 = np.mean(g_all); sd10 = np.std(g_all)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            nxt = c.shift(-1) / c - 1
            ret90 = c / c.shift(90) - 1
            # 30-day return as situation context, computed inside window only
            r30 = c / c.shift(30) - 1
            r10p = c / c.shift(10) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": pos, "nxt": nxt, "reg": b["regime"],
                               "f": b["forecast"], "r30": r30, "r10p": r10p,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["gain"] = df["pos"] * df["nxt"]
            df["drift"] = df["pos"] * mu_d
            rows.append(df)
            cv = c.values
            idx = np.arange(0, len(cv) - H, H)
            for i in idx:
                f = b["forecast"].iloc[i]
                if f != 0 and not np.isnan(f):
                    r = cv[i + H] / cv[i] - 1
                    cell_rows.append({"coin": coin, "win": w, "f": f, "reg": b["regime"].iloc[i],
                                      "tot": np.sign(f) * r, "unus": np.sign(f) * (r - mu10),
                                      "r30": r30.iloc[i], "r10p": r10p.iloc[i],
                                      "year": pd.to_datetime(b["timestamp"].iloc[i]).year})
    bars = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    cells = pd.DataFrame(cell_rows)
    bars["side"] = np.where(bars.pos > 0, "long", np.where(bars.pos < 0, "short", "flat"))
    g = bars.groupby(["reg", "side"]).agg(n=("gain", "size"), gain_sum=("gain", "sum"),
                                          gain_mean=("gain", "mean"), drift_mean=("drift", "mean"),
                                          abs_pos=("pos", lambda x: x.abs().mean()))
    g["timing_mean"] = g["gain_mean"] - g["drift_mean"]
    out["gain by regime side (per bar, before cost)"] = g
    out["share bars short/long/flat"] = bars["side"].value_counts(normalize=True)
    # by year
    gy = bars.groupby("year").agg(gain=("gain", "mean"), drift=("drift", "mean"), pos=("pos", "mean"))
    out["by year"] = gy
    # cells by r30 quintile, short side only
    s = cells[cells.f < 0].copy()
    s["q30"] = pd.qcut(s["r30"], 5, labels=False)
    out["short cells by prior 30d return quintile"] = s.groupby("q30").agg(n=("tot", "size"), r30=("r30", "mean"),
                                                                          tot=("tot", "mean"), unus=("unus", "mean"))
    s["q10"] = pd.qcut(s["r10p"], 5, labels=False)
    out["short cells by prior 10d return quintile"] = s.groupby("q10").agg(n=("tot", "size"), r10=("r10p", "mean"),
                                                                          tot=("tot", "mean"), unus=("unus", "mean"))
    s["qf"] = pd.qcut(s["f"].abs(), 4, labels=False, duplicates="drop")
    out["short cells by |f| quartile"] = s.groupby("qf").agg(n=("tot", "size"), f=("f", "mean"), tot=("tot", "mean"), unus=("unus", "mean"))
    l = cells[cells.f > 0]
    out["long cells"] = pd.Series({"n": len(l), "tot": l.tot.mean(), "unus": l.unus.mean(),
                                   "t_tot": stats.ttest_1samp(l.tot, 0).statistic if len(l) > 2 else np.nan})
    out["short cells summary"] = pd.Series({"n": len(s), "tot": s.tot.mean(), "unus": s.unus.mean(),
                                            "t_tot": stats.ttest_1samp(s.tot, 0).statistic})
    out["cells by coin"] = cells.groupby("coin").agg(n=("tot", "size"), tot=("tot", "mean"), unus=("unus", "mean"))
    return out
