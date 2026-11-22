def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hrows = []
    for coin, wins in data["bars"].items():
        # coin drift and usual move from non-overlapping 18-bar returns over all windows
        r18_all = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            r18_all.extend(list(c[idx + H] / c[idx] - 1))
        r18_all = np.array(r18_all)
        if len(r18_all) < 10:
            continue
        drift = r18_all.mean(); usual = r18_all.std()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(r1).fillna(0).values
            n = len(c)
            L = np.zeros(n); start = np.zeros(n, dtype=int)
            for i in range(n):
                if i > 0 and sgn[i] != 0 and sgn[i] == sgn[i-1]:
                    L[i] = L[i-1] + sgn[i]; start[i] = start[i-1]
                else:
                    L[i] = sgn[i]; start[i] = i - 1 if i > 0 else 0
            cv = c.values; vv = v.values
            usual1 = r1.abs().rolling(180, min_periods=60).mean().values
            vmean = v.rolling(180, min_periods=60).mean().values
            ts = pd.to_datetime(df["timestamp"])
            # hourly next-bar
            nxt = (c.shift(-1) / c - 1).values
            for i in range(n - 1):
                if not np.isnan(nxt[i]):
                    hrows.append((coin, ts.iloc[i].hour, nxt[i], r1.values[i] / usual1[i] if usual1[i] > 0 else np.nan))
            for i in range(0, n - H, H):
                if i < 1 or np.isnan(usual1[i]):
                    continue
                s = start[i]
                gain = cv[i] / cv[s] - 1
                ratio = gain / usual1[i]
                seg = vv[s+1:i+1]
                if len(seg) >= 2:
                    half = len(seg) // 2
                    fade = np.log((seg[-half:].mean() + 1e-12) / (seg[:len(seg)-half].mean() + 1e-12))
                else:
                    fade = np.nan
                vrel = np.log((vv[i] + 1e-12) / (vmean[i] + 1e-12)) if vmean[i] > 0 else np.nan
                p6 = cv[i] / cv[i-6] - 1 if i >= 6 else np.nan
                p18 = cv[i] / cv[i-18] - 1 if i >= 18 else np.nan
                p180 = cv[i] / cv[i-180] - 1 if i >= 180 else np.nan
                rng = (df["high"].values[i] - df["low"].values[i]) / cv[i]
                fr = cv[i + H] / cv[i] - 1
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 L=L[i], ratio=ratio, fade=fade, vrel=vrel,
                                 p6u=p6 / (usual1[i] * np.sqrt(6)) if not np.isnan(p6) else np.nan,
                                 p18u=p18 / (usual1[i] * np.sqrt(18)) if not np.isnan(p18) else np.nan,
                                 p180=p180, volu=usual1[i], rng=rng / usual1[i],
                                 un=fr - drift, st=(fr - drift) / usual))
    G = pd.DataFrame(rows)
    # vol level rank within coin
    G["volrank"] = G.groupby("coin")["volu"].rank(pct=True)
    def summ(g):
        x = g["un"].dropna()
        return pd.Series({"n": len(x), "mean_un%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "strength": g["st"].mean()})
    out = {}
    G["Lb"] = G["L"].clip(-6, 6)
    out["by_streak_len"] = G.groupby("Lb").apply(summ)
    for col in ["p6u", "p18u", "p180", "vrel", "rng", "volrank"]:
        q = pd.qcut(G[col], 5, labels=False, duplicates="drop")
        out["by_" + col + "_quint"] = G.groupby(q).apply(summ)
    up = G[(G.L >= 3)].copy(); dn = G[(G.L <= -3)].copy()
    for nm, d in [("up3", up), ("dn3", dn)]:
        d["rq"] = pd.qcut(d["ratio"].abs(), 3, labels=False, duplicates="drop")
        d["fq"] = (d["fade"] < d["fade"].median()).map({True: "fading", False: "rising"})
        out[nm + "_ratio_x_fade"] = d.groupby(["rq", "fq"]).apply(summ)
    out["by_weekday"] = G.groupby("wd").apply(summ)
    out["by_year"] = G.groupby("year").apply(summ)
    Hd = pd.DataFrame(hrows, columns=["coin", "hour", "nxt", "r1u"])
    def s1(g):
        x = g["nxt"]; return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["nextbar_by_hour"] = Hd.groupby("hour").apply(s1)
    Hd["q"] = pd.qcut(Hd["r1u"], 10, labels=False, duplicates="drop")
    out["nextbar_by_bar_move_decile"] = Hd.groupby("q").apply(s1)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["day"] = pd.to_datetime(D["day"])
    B = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    B["wd"] = B.index.get_level_values("day").weekday
    B["yr"] = B.index.get_level_values("day").year
    out["book_by_year"] = B.groupby("yr").agg(n=("book_return", "size"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), book_sd=("book_return", "std"))
    B["cq"] = pd.qcut(B["coin_return"], 10, labels=False)
    out["book_by_coin_day_decile"] = B.groupby("cq")[["book_return", "coin_return"]].mean()
    bq = B["book_return"]
    top = B[bq >= bq.quantile(0.98)]; bot = B[bq <= bq.quantile(0.02)]
    out["book_extremes"] = pd.DataFrame({"n": [len(top), len(bot)], "book": [top.book_return.mean(), bot.book_return.mean()], "coin": [top.coin_return.mean(), bot.coin_return.mean()]}, index=["top2%", "bot2%"])
    return out
