def explore(data):
    import pandas as pd, numpy as np
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(bars.keys())
    # ---- book daily series
    rows = []
    for c in coins:
        for w, d in days[c].items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["coin"] = c; t["win"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["day"] = pd.to_datetime(D["day"]).dt.normalize()
    B = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B["wn"] = B.win.str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna(subset=["book"]).reset_index(drop=True)
    v = (1 + B.book).cumprod().values
    peak = np.maximum.accumulate(v); dd = v / peak - 1
    B["dd"] = dd
    # ---- bar features
    br = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b.close
            dr = cl.pct_change()
            b["day"] = pd.to_datetime(b.timestamp, utc=True).dt.tz_localize(None).dt.normalize()
            b["alloc"] = b.postRebalance_current_allocation
            b["gain"] = b.alloc * (cl.shift(-1) / cl - 1)
            b["er"] = (cl - cl.shift(30)).abs() / cl.diff().abs().rolling(30).sum()
            b["r30"] = cl / cl.shift(30) - 1
            b["r7"] = cl / cl.shift(7) - 1
            b["r90"] = cl / cl.shift(90) - 1
            b["vol30"] = dr.rolling(30).std()
            b["vol7"] = dr.rolling(7).std()
            b["volratio"] = b.vol7 / b.vol30
            b["fwd7"] = cl.shift(-7) / cl - 1
            b["fwd14"] = cl.shift(-14) / cl - 1
            b["fwd3"] = cl.shift(-3) / cl - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["win"] = w
            # days since entry into same side
            s = np.sign(b.alloc.fillna(0))
            grp = (s != s.shift()).cumsum()
            b["age"] = b.groupby(grp).cumcount()
            br.append(b[["day", "gain", "alloc", "forecast", "er", "r30", "r7", "r90", "vol30", "volratio",
                         "fwd7", "fwd14", "fwd3", "pos", "coin", "win", "age"]])
    X = pd.concat(br, ignore_index=True)
    X["side"] = np.sign(X.alloc)
    act = X[X.alloc != 0].copy()
    act["absA"] = act.alloc.abs()
    def tab(df, col, q=4):
        z = df.dropna(subset=[col]).copy()
        z["bin"] = pd.qcut(z[col], q, labels=False, duplicates="drop")
        g = z.groupby("bin")
        return pd.DataFrame({"n": g.gain.size(), "mid": g[col].mean(), "gain_mean": g.gain.mean(),
                             "gain_sd": g.gain.std(), "gain_sum": g.gain.sum()})
    out["active bar gain by side"] = act.groupby("side").gain.agg(["count", "mean", "std", "sum"])
    out["by |alloc|"] = tab(act, "absA")
    out["by vol30"] = tab(act, "vol30")
    out["by er"] = tab(act, "er")
    out["by vol7/vol30"] = tab(act, "volratio")
    act["r90side"] = act.r90 * act.side
    out["by r90 in side"] = tab(act, "r90side")
    out["by age (days held)"] = act.assign(a=act.age.clip(upper=14)).groupby("a").gain.agg(["count", "mean"])
    out["side x year"] = act.assign(y=act.day.dt.year).groupby(["y", "side"]).gain.sum().unstack()
    # ---- falls: episodes
    eps = []
    i = 0; n = len(B)
    in_dd = False
    for k in range(n):
        if dd[k] < 0 and not in_dd:
            in_dd = True; st = k - 1 if k > 0 else 0
        if in_dd and (dd[k] == 0 or k == n - 1):
            seg = slice(st, k + 1)
            tr = st + int(np.argmin(dd[seg]))
            eps.append((dd[tr], st, tr))
            in_dd = False
    eps = sorted(eps)[:5]
    er_rows = []
    for depth, st, tr in eps:
        keys = B.iloc[st:tr + 1][["win", "day"]]
        f = X.merge(keys, on=["win", "day"])
        fa = f[f.alloc != 0]
        er_rows.append({"depth": depth, "days": tr - st, "win": B.win.iloc[tr], "year": B.day.iloc[tr].year,
                        "hold_sum": B.hold.iloc[st + 1:tr + 1].sum(),
                        "long_share": (fa.side > 0).mean(), "long_gain": fa[fa.side > 0].gain.sum() / 6,
                        "short_gain": fa[fa.side < 0].gain.sum() / 6, "mean_absA": fa.absA.mean() if len(fa) else np.nan,
                        "mean_vol30": fa.vol30.mean(), "mean_r90side": (fa.r90 * fa.side).mean(),
                        "mean_er": fa.er.mean()})
    out["5 deepest falls"] = pd.DataFrame(er_rows)
    out["overall"] = pd.Series({"maxdd": dd.min(), "act_vol30_mean": act.vol30.mean(), "act_absA_mean": act.absA.mean()})
    # ---- grid cases (positions 0,7,14..) unusual move, signal vs condition-only
    drift = X[X.pos % 7 == 0].groupby("coin").fwd7.mean()
    drift14 = X[X.pos % 14 == 0].groupby("coin").fwd14.mean()
    G = X[(X.pos % 7 == 0)].dropna(subset=["fwd7"]).copy()
    G["dir"] = np.sign(G.forecast)
    G["u7"] = (G.fwd7 - G.coin.map(drift)) * G.dir
    G["u14"] = (G.fwd14 - G.coin.map(drift14)) * G.dir
    sig = G[G.dir != 0].copy()
    def tstat(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["signal cases u7 by side"] = sig.groupby("dir").u7.apply(tstat).unstack()
    out["signal cases u14 by side"] = sig.groupby("dir").u14.apply(tstat).unstack()
    sig["vb"] = pd.qcut(sig.vol30, 3, labels=False)
    out["signal u7 by vol30 tercile"] = sig.groupby("vb").u7.apply(tstat).unstack()
    sig["r90s"] = sig.r90 * sig.dir
    sig["rb"] = pd.qcut(sig.r90s, 3, labels=False)
    out["signal u7 by r90-in-side tercile"] = sig.groupby("rb").u7.apply(tstat).unstack()
    # condition-only (no signal) bars: direction sign(r7), high vol / r90 agreeing
    G2 = G[G.dir == 0].dropna(subset=["r7", "vol30", "r90"]).copy()
    G2["d"] = np.sign(G2.r7)
    G2["u7"] = (G2.fwd7 - G2.coin.map(drift)) * G2.d
    G2["r90s"] = G2.r90 * G2.d
    vcut = sig.vol30.quantile([1/3, 2/3]).values
    rcut = sig.r90s.quantile([1/3, 2/3]).values
    G2["vb"] = np.digitize(G2.vol30, vcut); G2["rb"] = np.digitize(G2.r90s, rcut)
    out["no-signal bars u7 (dir r7) by vol tercile"] = G2.groupby("vb").u7.apply(tstat).unstack()
    out["no-signal bars u7 (dir r7) by r90 tercile"] = G2.groupby("rb").u7.apply(tstat).unstack()
    # book daily return sd by year and daily book by vol regime
    out["book by year"] = B.assign(y=B.day.dt.year).groupby("y").agg(mean=("book", "mean"), sd=("book", "std"),
                                                                    mindd=("dd", "min"), hold=("hold", "mean"))
    return out
