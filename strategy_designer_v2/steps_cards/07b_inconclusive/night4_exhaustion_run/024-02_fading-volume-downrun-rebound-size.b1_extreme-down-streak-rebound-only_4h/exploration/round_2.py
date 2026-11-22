def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 18
    srows = []
    bet_ratio = []
    for coin, wins in bars.items():
        dr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            dr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(dr); sd = np.std(dr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values.astype(float); n = len(c)
            f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            usual = pd.Series(np.abs(r1)).rolling(180, min_periods=45).mean().values
            L = np.zeros(n, int)
            for i in range(1, n):
                L[i] = L[i-1] + 1 if c[i] < c[i-1] else 0
            fwd = np.r_[c[H:] / c[:-H] - 1, [np.nan]*H]
            prev = np.r_[0, f[:-1]]
            bet = (f >= 2) & (f - prev >= 2)
            for i in np.where(L >= 2)[0]:
                s = i - L[i]
                if np.isnan(usual[i]) or usual[i] == 0 or np.isnan(fwd[i]): continue
                ratio = (1 - c[i] / c[s]) / usual[i]
                vv = v[s+1:i+1]
                slope = np.polyfit(np.arange(len(vv)), vv, 1)[0]
                if bet[i] and slope < 0:
                    bet_ratio.append(ratio)
                if slope >= 0 or ratio <= 4: continue
                srows.append({"coin": coin, "w": w, "year": yr[i], "cell": i // H, "ratio": ratio,
                              "L": L[i], "x": fwd[i] - drift, "s": (fwd[i] - drift) / sd})
    S = pd.DataFrame(srows).sort_values("ratio", ascending=False)
    S = S.groupby(["coin", "w", "cell"]).head(1)  # one case per grid cell, the most extreme
    def summ(g):
        x = g["x"]
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": g["s"].mean()})
    out = {}
    br = pd.Series(bet_ratio)
    out["test_bets_ratio_dist"] = pd.Series({"n": len(br), "median": br.median(), "share>4": (br > 4).mean(),
                                             "share>6": (br > 6).mean()})
    out["fade_ratio>4_all"] = summ(S)
    out["fade_ratio>6_all"] = summ(S[S.ratio > 6])
    lr = stats.linregress(S["ratio"].clip(upper=15), S["x"])
    out["slope_x_on_ratio(>4)"] = pd.Series({"slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "n": len(S)})
    S["rb"] = pd.cut(S.ratio, [4, 5, 6, 8, 10, np.inf])
    out["by_ratio_bin"] = S.groupby("rb", observed=True).apply(summ)
    out[">6_by_coin"] = S[S.ratio > 6].groupby("coin").apply(summ)
    out[">6_by_year"] = S[S.ratio > 6].groupby("year").apply(summ)
    out["by_streaklen"] = S.groupby(S.L.clip(upper=7)).apply(summ)
    return out
