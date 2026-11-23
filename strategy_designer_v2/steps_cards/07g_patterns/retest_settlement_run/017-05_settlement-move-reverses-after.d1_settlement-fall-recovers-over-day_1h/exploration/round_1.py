def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []      # per hour-of-day samples
    grid = {24: [], 72: []}
    hourly = []
    for coin, wins in bars.items():
        # coin drift per horizon over all windows (non-overlapping)
        drift = {}
        for H in (24, 72):
            r = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                r.append(c[idx + H] / c[idx] - 1)
            drift[H] = np.concatenate(r).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ts = pd.to_datetime(df["timestamp"])
            hr = ts.dt.hour.values
            r2 = c / c.shift(2) - 1
            s2 = r2 / r2.abs().rolling(720, min_periods=200).mean()
            f24 = c.shift(-24) / c - 1 - drift[24]
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=200).std()
            vr = df["volume"] / df["volume"].rolling(720, min_periods=200).median()
            hourly.append(pd.DataFrame({"coin": coin, "hour_close": (hr + 1) % 24,
                                        "fwd1": r1.shift(-1).values, "vr": vr.values}))
            rows.append(pd.DataFrame({"coin": coin, "hour_close": (hr + 1) % 24, "s2": s2.values,
                                      "f24": f24.values}))
            for H in (24, 72):
                rp = c / c.shift(H) - 1
                sp = rp / rp.abs().rolling(720, min_periods=200).mean()
                fH = c.shift(-H) / c - 1 - drift[H]
                fraw = c.shift(-H) / c - 1
                idx = np.arange(0, len(c), H)
                g = pd.DataFrame({"coin": coin, "sp": sp.values[idx], "f": fH.values[idx],
                                  "fraw": fraw.values[idx],
                                  "vol": vol.values[idx]})
                grid[H].append(g)
    out = {}
    R = pd.concat(rows).dropna()
    res = []
    for h, g in R.groupby("hour_close"):
        sl = stats.linregress(g["s2"], g["f24"])
        fall = g[g["s2"] < 0]
        res.append({"hour_close": h, "n": len(g), "slope_bp": sl.slope * 1e4,
                    "t_slope": sl.slope / sl.stderr,
                    "fall_mean_f24_pct": fall["f24"].mean() * 100,
                    "strong_fall_mean_pct": g[g["s2"] < -1.5]["f24"].mean() * 100,
                    "n_strong": (g["s2"] < -1.5).sum()})
    out["2h_move_vs_next24h_by_close_hour"] = pd.DataFrame(res).round(3)
    Hh = pd.concat(hourly).dropna()
    hh = Hh.groupby("hour_close").agg(mean_next1h_bp=("fwd1", lambda x: x.mean() * 1e4),
                                     t=("fwd1", lambda x: x.mean() / x.std() * np.sqrt(len(x))),
                                     vol_ratio=("vr", "median"))
    out["next_hour_return_by_close_hour"] = hh.round(3)
    for H in (24, 72):
        G = pd.concat(grid[H]).dropna()
        G["q"] = pd.qcut(G["sp"], 5, labels=False)
        G["vt"] = G.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
        t1 = G.groupby("q").agg(n=("f", "size"), sp=("sp", "mean"),
                                fex_pct=("f", lambda x: x.mean() * 100),
                                t=("f", lambda x: x.mean() / x.std() * np.sqrt(len(x))),
                                fraw_pct=("fraw", lambda x: x.mean() * 100))
        out[f"past{H}h_quintile_vs_next{H}h"] = t1.round(3)
        t2 = G.groupby(["vt", "q"]).agg(n=("f", "size"), fex_pct=("f", lambda x: x.mean() * 100),
                                       t=("f", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
        out[f"past{H}h_by_voltercile_quintile"] = t2.round(3)
        pc = []
        for coin, g in G.groupby("coin"):
            sl = stats.linregress(g["sp"], g["f"])
            pc.append({"coin": coin, "n": len(g), "slope_bp": sl.slope * 1e4, "t": sl.slope / sl.stderr})
        out[f"past{H}h_slope_by_coin"] = pd.DataFrame(pc).round(3)
    return out
