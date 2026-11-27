def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    rows = []
    allbars = []
    drift = {}
    for coin, ws in bars.items():
        r = {h: [] for h in H}
        for w, df in ws.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                r[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: (np.mean(r[h]) if r[h] else np.nan, np.std(r[h], ddof=1) if len(r[h]) > 1 else np.nan) for h in H}
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            loc = np.where(hi > lo, (c - lo) / (hi - lo), np.nan)
            ret5 = pd.Series(c).pct_change(5).values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.fall_depth.last_history_value", pd.Series(np.nan, index=df.index)).values
            reg = df["regime"].astype(str).values
            # cases: first bar with forecast <= -2 in each 5-bar grid cell
            for s in range(0, n, 5):
                for t in range(s, min(s + 5, n)):
                    if f[t] <= -2:
                        rec = dict(coin=coin, w=w, year=year[t], day=day[t], f=f[t], raw=raw[t], loc=loc[t], ret5=ret5[t])
                        for h in H:
                            if t + h < n:
                                rec[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[coin][h][0])
                            else:
                                rec[f"u{h}"] = np.nan
                        rows.append(rec)
                        break
            # in-profile bars (regime not chop), grid of 5, any upper-half close
            for t in range(0, n - 5, 5):
                allbars.append(dict(coin=coin, w=w, year=year[t], day=day[t], inprof=reg[t] != "chop", active=reg[t] == "mean_reversion",
                                    loc=loc[t], ret5=ret5[t],
                                    u2=-(c[min(t+2,n-1)] / c[t] - 1 - drift[coin][2][0]) if t+2<n else np.nan,
                                    u5=-(c[t + 5] / c[t] - 1 - drift[coin][5][0])))
    cs = pd.DataFrame(rows); ab = pd.DataFrame(allbars)

    def tpool(d, col):
        d = d.dropna(subset=[col])
        if len(d) < 3: return pd.Series(dict(n=len(d), days=d["day"].nunique() if len(d) else 0, mean=np.nan, t=np.nan))
        m = d[col].mean()
        g = (d[col] - m).groupby(d["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), days=D, mean=m, t=m / se))
    out = {}
    out["horizons"] = pd.DataFrame({f"u{h}": tpool(cs, f"u{h}") for h in H}).T
    out["by_coin_u5"] = cs.groupby("coin").apply(lambda d: tpool(d, "u5"))
    out["by_window_u5"] = cs.groupby("w").apply(lambda d: tpool(d, "u5"))
    out["by_year_u5"] = cs.groupby("year").apply(lambda d: tpool(d, "u5"))
    cs["fq"] = pd.qcut(cs["f"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_forecast_third"] = cs.groupby("fq").apply(lambda d: tpool(d, "u5"))
    cs["rq"] = pd.qcut(cs["ret5"].rank(method="first"), 3, labels=["deepest", "mid", "shallow"])
    out["by_ret5_third"] = cs.groupby("rq").apply(lambda d: tpool(d, "u5"))
    cs["lq"] = pd.cut(cs["loc"], [0.5, 0.7, 0.85, 1.01], right=False)
    out["by_loc"] = cs.groupby("lq").apply(lambda d: tpool(d, "u5"))
    out["median_u5_and_share_pos"] = pd.Series(dict(median=cs["u5"].median(), share_pos=(cs["u5"] > 0).mean()))
    ip = ab[ab["inprof"]].copy()
    ip["upper"] = ip["loc"] >= 0.5
    ip["neg5"] = ip["ret5"] < 0
    out["inprofile_grid_u5"] = ip.groupby(["upper", "neg5"]).apply(lambda d: tpool(d, "u5"))
    out["inprofile_grid_u2"] = ip.groupby(["upper", "neg5"]).apply(lambda d: tpool(d, "u2"))
    ip["lq"] = pd.cut(ip["loc"], [0, 0.25, 0.5, 0.75, 1.01], right=False)
    out["inprofile_by_loc_u5"] = ip.groupby("lq").apply(lambda d: tpool(d, "u5"))
    out["inprofile_by_loc_u2"] = ip.groupby("lq").apply(lambda d: tpool(d, "u2"))
    return out
