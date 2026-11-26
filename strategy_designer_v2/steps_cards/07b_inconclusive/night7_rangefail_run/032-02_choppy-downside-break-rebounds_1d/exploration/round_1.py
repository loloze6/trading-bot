def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H_list = [1, 3, 5, 10, 20]
    recs = []
    # drift per coin per horizon: non-overlapping grid returns, all windows
    drift = {}
    for coin, wins in bars.items():
        for H in H_list:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rr += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = np.mean(rr) if rr else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; lo = df["low"]; hi = df["high"]
            prior_low = lo.shift(1).rolling(20).min()
            prior_high = hi.shift(1).rolling(20).max()
            depth = (c / prior_low - 1) * 100
            up = (c / prior_high - 1) * 100
            tr = (c / c.shift(60) - 1) * 100
            prof = np.where(tr > 10, "rising", np.where(tr < -10, "falling", "choppy"))
            prof = pd.Series(prof).where(tr.notna(), None)
            day = pd.to_datetime(df["timestamp"]).dt.floor("D")
            n = len(df)
            for i in range(n):
                if not (depth.iloc[i] < 0 or up.iloc[i] > 0):
                    continue
                rec = dict(coin=coin, w=w, i=i, day=day.iloc[i], depth=depth.iloc[i], up=up.iloc[i],
                           prof=prof.iloc[i], regime=df["regime"].iloc[i], year=day.iloc[i].year)
                for H in H_list:
                    if i + H < n:
                        rec[f"u{H}"] = c.iloc[i + H] / c.iloc[i] - 1 - drift[(coin, H)]
                        rec[f"g{H}"] = (i % H == 0)
                    else:
                        rec[f"u{H}"] = np.nan; rec[f"g{H}"] = False
                recs.append(rec)
    R = pd.DataFrame(recs)
    down = R[R.depth < 0].copy()
    upb = R[R.up > 0].copy()

    def summ(d, H, side=1):
        d = d[d[f"g{H}"] & d[f"u{H}"].notna()]
        if len(d) < 3:
            return pd.Series(dict(n=len(d), days=0, mean=np.nan, t=np.nan))
        x = side * d[f"u{H}"]
        g = (x - x.mean()).groupby(d["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series(dict(n=len(d), days=G, mean=x.mean(), t=x.mean() / se if se > 0 else np.nan))

    out = {}
    # by profile and horizon, downside breaks, long
    rows = {}
    for p in ["choppy", "rising", "falling"]:
        for H in H_list:
            rows[(p, H)] = summ(down[down.prof == p], H)
    out["down breaks long, by trend & H"] = pd.DataFrame(rows).T
    # regime-based choppy (the book's situation)
    rows = {}
    for H in H_list:
        rows[H] = summ(down[down.regime == "mean_reversion"], H)
    out["book situation (regime MR) by H"] = pd.DataFrame(rows).T
    # depth terciles in choppy, H=5 & 10, using all bars (not just grid) for more cases
    ch = down[down.prof == "choppy"].copy()
    ch["q"] = pd.qcut(ch.depth, 3, labels=["deep", "mid", "shallow"])
    rows = {}
    for q in ["deep", "mid", "shallow"]:
        for H in [1, 5, 10]:
            rows[(q, H)] = summ(ch[ch.q == q], H)
    out["choppy down by depth tercile"] = pd.DataFrame(rows).T
    rows = {}
    for coin in ch.coin.unique():
        rows[coin] = summ(ch[ch.coin == coin], 5)
    out["choppy down by coin H5"] = pd.DataFrame(rows).T
    rows = {}
    for w in sorted(ch.w.unique(), key=lambda s: int(s[1:])):
        rows[w] = summ(ch[ch.w == w], 5)
    out["choppy down by window H5"] = pd.DataFrame(rows).T
    # upside breaks, short (mirror), by trend
    rows = {}
    for p in ["choppy", "rising", "falling"]:
        for H in [1, 5, 10]:
            rows[(p, H)] = summ(upb[upb.prof == p], H, side=-1)
    out["up breaks short, by trend & H"] = pd.DataFrame(rows).T
    # overlapping-sample correlation depth vs u5 in choppy
    d5 = ch[ch.u5.notna()]
    out["choppy down: spearman(-depth, u5) all bars"] = str(stats.spearmanr(-d5.depth, d5.u5))
    out["choppy down count all bars"] = len(ch)
    return out
