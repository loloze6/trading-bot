def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 12, 18, 36]
    rows = []      # bet cases (as the test)
    srows = []     # recomputed streak bars
    drift = {}
    for coin, wins in bars.items():
        # normal drift per horizon
        dr = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                dr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(dr[h]) for h in H}
        sd18 = np.std(dr[18])
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values.astype(float)
            n = len(c)
            f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            usual = pd.Series(np.abs(r1)).rolling(180, min_periods=45).mean().values
            # streaks
            L = np.zeros(n, int)
            for i in range(1, n):
                L[i] = L[i-1] + 1 if c[i] < c[i-1] else 0
            fwd = {h: np.r_[c[h:] / c[:-h] - 1, [np.nan]*h] for h in H}
            # test bets
            prev = np.r_[0, f[:-1]]
            bet = (f >= 2) & (f - prev >= 2)
            cell = np.arange(n) // 18
            seen = set()
            for i in np.where(bet)[0]:
                if cell[i] in seen or i + 18 >= n: continue
                seen.add(cell[i])
                d = {"coin": coin, "w": w, "year": yr[i], "f": f[i], "L": L[i]}
                for h in H:
                    d[f"x{h}"] = fwd[h][i] - drift[coin][h] if i + h < n else np.nan
                d["s18"] = d["x18"] / sd18
                rows.append(d)
            # recomputed streaks
            for i in np.where(L >= 2)[0]:
                s = i - L[i]
                if np.isnan(usual[i]) or usual[i] == 0: continue
                ratio = (1 - c[i] / c[s]) / usual[i]
                vv = v[s+1:i+1]; x = np.arange(len(vv))
                slope = np.polyfit(x, vv, 1)[0] if len(vv) >= 2 else 0
                d = {"coin": coin, "w": w, "i": i, "cell18": i // 18, "ratio": ratio,
                     "fade": slope < 0, "L": L[i]}
                for h in H:
                    d[f"x{h}"] = fwd[h][i] - drift[coin][h] if i + h < n else np.nan
                srows.append(d)
    B = pd.DataFrame(rows)
    S = pd.DataFrame(srows)
    def summ(g, col="x18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["bets_by_horizon"] = pd.DataFrame({h: summ(B, f"x{h}") for h in H}).T
    out["bets_by_coin"] = B.groupby("coin").apply(summ)
    out["bets_by_year"] = B.groupby("year").apply(summ)
    B["fq"] = pd.qcut(B["f"].rank(method="first"), 5, labels=False)
    out["bets_by_forecast_quintile"] = B.groupby("fq").apply(lambda g: pd.concat([summ(g), pd.Series({"fmean": g.f.mean(), "Lmean": g.L.mean()})]))
    out["bets_by_streaklen"] = B.groupby(B.L.clip(upper=6)).apply(summ)
    # recomputed: first bar per cell per group
    S["rb"] = pd.cut(S["ratio"], [-np.inf, 2, 4, 6, 8, np.inf])
    S1 = S.sort_values("i").groupby(["coin", "w", "cell18", "rb", "fade"], observed=True).head(1)
    res = {}
    for (rb, fd), g in S1.groupby(["rb", "fade"], observed=True):
        for h in [6, 18, 36]:
            s = summ(g, f"x{h}")
            res[(str(rb), fd, h)] = s
    out["recomp_ratio_fade_h"] = pd.DataFrame(res).T
    return out
