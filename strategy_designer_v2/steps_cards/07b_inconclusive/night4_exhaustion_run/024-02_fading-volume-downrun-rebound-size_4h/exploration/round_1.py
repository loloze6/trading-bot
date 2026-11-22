def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 12, 18]
    rows = []      # cases from the backtest's forecast
    allrows = []   # all down-streak bars recomputed from prices, on an 18-bar grid
    drift = {}
    for coin in bars:
        # normal drift and usual move per horizon over all windows, non-overlapping
        d = {}
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs)
            d[h] = (np.nanmean(rs), np.nanstd(rs))
        drift[coin] = d
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            raw = df.get("debug_info.components.streak_loss.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            # past 30-day return
            r180 = np.full(n, np.nan)
            r180[180:] = c[180:] / c[:-180] - 1
            # recompute down streak, loss in usual moves, volume slope
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            absr = pd.Series(np.abs(ret1)).rolling(180, min_periods=45).mean().values
            slen = np.zeros(n, int); slope = np.full(n, np.nan); sloss = np.full(n, np.nan)
            L = 0
            for i in range(1, n):
                L = L + 1 if c[i] < c[i - 1] else 0
                slen[i] = L
                if L >= 2:
                    vv = v[i - L + 1:i + 1]; x = np.arange(L)
                    slope[i] = np.polyfit(x, vv, 1)[0]
                    sloss[i] = (c[i - L] - c[i]) / c[i - L] / absr[i] if absr[i] > 0 else np.nan
            # cases from forecast
            lo = 0.0; used = set()
            for i in range(n):
                if f[i] <= 0:
                    lo = 0.0; continue
                if f[i] - lo >= 2:
                    cell = i // 18
                    lo = f[i]
                    if cell not in used and i + 18 < n:
                        used.add(cell)
                        rec = dict(coin=coin, w=w, yr=yr[i], f=f[i], raw=raw[i], r180=r180[i],
                                   slen=slen[i], sloss=sloss[i])
                        for h in H:
                            rec["u%d" % h] = c[i + h] / c[i] - 1 - drift[coin][h][0]
                            rec["s%d" % h] = rec["u%d" % h] / drift[coin][h][1]
                        rows.append(rec)
                else:
                    lo = min(lo, f[i])
            # all down streaks: first streak bar per 18-grid cell
            used2 = set()
            for i in range(n - 18):
                if slen[i] >= 2 and not np.isnan(sloss[i]):
                    cell = i // 18
                    if cell in used2: continue
                    used2.add(cell)
                    allrows.append(dict(coin=coin, fade=slope[i] < 0, sloss=sloss[i], slen=slen[i],
                                        u18=c[i + 18] / c[i] - 1 - drift[coin][18][0],
                                        u6=c[i + 6] / c[i] - 1 - drift[coin][6][0]))
    C = pd.DataFrame(rows); A = pd.DataFrame(allrows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["overall_by_h"] = pd.DataFrame({h: summ(C, "u%d" % h) for h in H}).T
    out["strength_by_h"] = C[["s6", "s12", "s18"]].mean()
    out["by_coin"] = C.groupby("coin").apply(summ)
    out["by_year"] = C.groupby("yr").apply(summ)
    C["fq"] = pd.qcut(C["f"].rank(method="first"), 5, labels=False)
    out["by_forecast_q"] = C.groupby("fq").apply(summ)
    C["lq"] = pd.qcut(C["sloss"].rank(method="first"), 5, labels=False)
    out["by_relloss_q"] = C.groupby("lq").apply(lambda g: pd.concat([summ(g), pd.Series({"sloss": g.sloss.mean()})]))
    out["by_slen"] = C.assign(sl=C.slen.clip(upper=6)).groupby("sl").apply(summ)
    C["trend"] = np.where(C.r180 > 0, "up30d", "down30d")
    out["by_30d_trend"] = C.groupby("trend").apply(summ)
    out["by_trend_x_lossq_top"] = C[C.lq == 4].groupby("trend").apply(summ)
    A["lq"] = pd.qcut(A["sloss"].rank(method="first"), 5, labels=False)
    out["all_streaks_fade_x_lossq"] = A.groupby(["lq", "fade"]).apply(summ)
    out["all_streaks_fade_x_lossq_6"] = A.groupby(["lq", "fade"]).apply(lambda g: summ(g, "u6"))
    return out
