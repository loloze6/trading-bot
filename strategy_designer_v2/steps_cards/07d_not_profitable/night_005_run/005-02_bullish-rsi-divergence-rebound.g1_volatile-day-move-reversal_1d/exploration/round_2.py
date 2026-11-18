def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    rows = []
    for c in days:
        for w in days[c]:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d["pos"] = d["dayk"].map(pos)
            d["coin"] = c; d["w"] = w
            d["c20"] = d["close"] / d["close"].shift(20) - 1
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["book_return", "coin_return", "pos"])
    # variants: long-only, short-only contributions (before fees approx)
    D["long_part"] = D["pos"].clip(lower=0) * D["coin_return"]
    D["short_part"] = D["pos"].clip(upper=0) * D["coin_return"]
    def stats_of(r):
        r = r.dropna()
        v = (1 + r).cumprod(); dd = (v / v.cummax() - 1).min()
        ann = (1 + r.mean()) ** 365 - 1
        return pd.Series({"mean": r.mean(), "sharpe": r.mean() / r.std() * np.sqrt(365), "maxdd": dd, "calmar_approx": ann / -dd})
    res = {}
    for c in D.coin.unique():
        X = D[D.coin == c]
        for k in ["book_return", "long_part", "short_part", "coin_return"]:
            res[(c, k)] = stats_of(X[k])
    out["variants"] = pd.DataFrame(res).T
    # short side contribution by 20d trend sign
    D["tr"] = np.sign(D["c20"])
    D["sd"] = np.sign(D["pos"])
    out["contrib_by_side_trend"] = D.groupby(["sd", "tr"]).agg(n=("book_return", "size"), book=("book_return", "mean"),
        coin=("coin_return", "mean"), t=("book_return", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # deepest falls: 60-day rolling book loss episodes: share of loss from shorts vs longs during worst drawdown per coin
    dd_rows = []
    for c in D.coin.unique():
        X = D[D.coin == c].reset_index(drop=True)
        v = (1 + X["book_return"]).cumprod(); peak = v.cummax(); dd = v / peak - 1
        end = dd.idxmin(); start = v[:end + 1].idxmax()
        S = X.loc[start + 1:end]
        dd_rows.append(pd.Series({"coin": c, "days": len(S), "dd": dd.min(), "coin_move": (1 + S.coin_return).prod() - 1,
            "loss_from_shorts": S.short_part.sum(), "loss_from_longs": S.long_part.sum(),
            "share_short_days": (S.pos < 0).mean(), "mean_c20_in_fall": S.c20.mean()}))
    out["worst_dd"] = pd.DataFrame(dd_rows)
    # non-overlapping 3-bar excess return after down vs up days, graded by move size (vol-scaled), in active regime
    cases = []
    for c in bars:
        allr = []
        for w in bars[c]:
            b = bars[c][w]
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 3, 3)
            allr.append(cl[idx + 3] / cl[idx] - 1)
        mu3 = np.concatenate(allr).mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            r1 = b["close"].pct_change()
            z = r1 / r1.abs().rolling(60, min_periods=20).mean().shift(1)
            c20 = b["close"] / b["close"].shift(20) - 1
            cl = b["close"].values
            for i in range(0, len(b) - 3, 3):
                if b.loc[i, "forecast"] != 0 and not np.isnan(z.iloc[i]):
                    cases.append((c, z.iloc[i], c20.iloc[i], cl[i + 3] / cl[i] - 1 - mu3))
    K = pd.DataFrame(cases, columns=["coin", "z", "c20", "ex"]).dropna()
    for nm, sub in [("down", K[K.z < 0]), ("up", K[K.z > 0])]:
        sl = stats.linregress(sub.z, sub.ex)
        out["slope_" + nm] = pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr})
    K["zq"] = pd.qcut(K.z, 6, labels=False)
    out["ex_by_zsext"] = K.groupby("zq").agg(n=("ex", "size"), z=("z", "mean"), ex=("ex", "mean"), t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    U = K[K.z > 0].copy(); U["tr"] = np.sign(U.c20)
    out["up_moves_by_trend"] = U.groupby("tr").agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    return out
