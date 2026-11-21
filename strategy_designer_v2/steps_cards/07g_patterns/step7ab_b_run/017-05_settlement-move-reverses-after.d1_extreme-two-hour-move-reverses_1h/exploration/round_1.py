def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows_h = []; rows_rev = []; rows_wd = []; rows_vol = []; rows_set = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # hour of day: 1h return of bar ending at hour (bar start hour)
            hr = ts.dt.hour.values
            vm = pd.Series(v).rolling(168, min_periods=48).median().shift(1).values
            fwd1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            rows_h.append(pd.DataFrame({"coin": coin, "hour": hr, "fwd1": fwd1,
                                        "vrat": v / vm}))
            # 24h grid: past 24h move scaled, forward 24h and 72h returns
            n = len(c)
            lr = pd.Series(np.log(c)).diff()
            vol24 = lr.rolling(480, min_periods=200).std().values * np.sqrt(24)
            for i in range(24, n - 72, 24):
                past = c[i] / c[i - 24] - 1
                f24 = c[i + 24] / c[i] - 1
                f72 = c[i + 72] / c[i] - 1 if i + 72 < n else np.nan
                rows_rev.append((coin, w, past / vol24[i] if vol24[i] > 0 else np.nan,
                                 f24, f72, vol24[i], ts.iloc[i].hour))
            # settlement windows: return of hours 5-8, 13-16, 21-24 vs trend of prior 24h
            df = pd.DataFrame({"ts": ts, "c": c})
            for i in range(28, n - 4, 4):
                h = ts.iloc[i].hour
                pre = c[i] / c[i - 4] - 1   # 4h ending at bar i start-of-bar close
                trend = c[i - 4] / c[i - 28] - 1
                post = c[i + 4] / c[i] - 1
                rows_set.append((coin, h, np.sign(trend), pre, post))
    H = pd.concat(rows_h)
    g = H.groupby("hour")["fwd1"]
    out["next1h_by_hour_bps"] = pd.DataFrame({"mean_bps": g.mean() * 1e4,
        "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count(),
        "vol_ratio_med": H.groupby("hour")["vrat"].median()}).round(2)
    R = pd.DataFrame(rows_rev, columns=["coin", "w", "z", "f24", "f72", "vol", "hour"]).dropna()
    # demean per coin
    for col in ["f24", "f72"]:
        R[col + "_u"] = R[col] - R.groupby("coin")[col].transform("mean")
    R["zq"] = pd.qcut(R["z"], 10, labels=False)
    gq = R.groupby("zq")
    out["past24h_z_decile_fwd"] = pd.DataFrame({"z_mean": gq["z"].mean(),
        "f24u_bps": gq["f24_u"].mean() * 1e4,
        "t24": gq["f24_u"].mean() / (gq["f24_u"].std() / np.sqrt(gq["f24_u"].count())),
        "f72u_bps": gq["f72_u"].mean() * 1e4,
        "t72": gq["f72_u"].mean() / (gq["f72_u"].std() / np.sqrt(gq["f72_u"].count())),
        "n": gq["z"].count()}).round(2)
    R["vq"] = R.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False))
    gv = R.groupby("vq")
    out["vol_quintile_fwd"] = pd.DataFrame({"f24u_bps": gv["f24_u"].mean() * 1e4,
        "t24": gv["f24_u"].mean() / (gv["f24_u"].std() / np.sqrt(gv["f24_u"].count())),
        "f72u_bps": gv["f72_u"].mean() * 1e4, "n": gv["f24_u"].count()}).round(2)
    out["corr_z_f72u_by_coin"] = R.groupby("coin").apply(lambda d: stats.spearmanr(d["z"], d["f72_u"])[0]).round(3)
    S = pd.DataFrame(rows_set, columns=["coin", "hour", "tr", "pre", "post"])
    S = S[S.tr != 0]
    S["pre_ag"] = -S.tr * S.pre; S["post_with"] = S.tr * S.post
    gs = S.groupby("hour")
    out["4h_block_vs_trend_bps"] = pd.DataFrame({
        "pre_against_bps": gs["pre_ag"].mean() * 1e4,
        "t_pre": gs["pre_ag"].mean() / (gs["pre_ag"].std() / np.sqrt(gs["pre_ag"].count())),
        "post_with_bps": gs["post_with"].mean() * 1e4,
        "t_post": gs["post_with"].mean() / (gs["post_with"].std() / np.sqrt(gs["post_with"].count())),
        "n": gs["pre"].count()}).round(2)
    # days: weekday, book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    gw = D.groupby("wd")
    out["weekday_bps"] = pd.DataFrame({"coin_bps": gw["coin_return"].mean() * 1e4,
        "t_coin": gw["coin_return"].mean() / (gw["coin_return"].std() / np.sqrt(gw["coin_return"].count())),
        "book_bps": gw["book_return"].mean() * 1e4, "n": gw["coin_return"].count()}).round(2)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year_bps"] = (D.groupby("year")[["book_return", "coin_return"]].mean() * 1e4).round(2)
    out["book_by_coin_bps"] = (D.groupby("coin")[["book_return", "coin_return"]].mean() * 1e4).round(2)
    return out
