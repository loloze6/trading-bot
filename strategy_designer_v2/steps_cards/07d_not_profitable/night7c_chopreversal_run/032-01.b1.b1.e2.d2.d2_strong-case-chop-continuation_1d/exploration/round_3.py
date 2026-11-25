def explore(data):
    import pandas as pd, numpy as np
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(bars.keys())
    def nd(s):
        return pd.to_datetime(s, utc=True).dt.tz_localize(None).dt.normalize()
    def tstat(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # ---- book daily series
    rows = []
    for c in coins:
        for w, d in days[c].items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["coin"] = c; t["win"] = w
            rows.append(t)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = nd(D["day"])
    B = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B["wn"] = B.win.str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna(subset=["book"]).reset_index(drop=True)
    v = (1 + B.book).cumprod().values
    dd = v / np.maximum.accumulate(v) - 1
    B["dd"] = dd
    # ---- bar features
    br = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            cl = b.close
            dr = cl.pct_change()
            b["day"] = nd(b.timestamp)
            b["alloc"] = b.postRebalance_current_allocation.fillna(0)
            b["gain"] = b.alloc * (cl.shift(-1) / cl - 1)
            b["er"] = (cl - cl.shift(30)).abs() / cl.diff().abs().rolling(30).sum()
            b["r30"] = cl / cl.shift(30) - 1
            b["r7"] = cl / cl.shift(7) - 1
            b["r90"] = cl / cl.shift(90) - 1
            b["vol30"] = dr.rolling(30).std()
            b["volratio"] = dr.rolling(7).std() / b["vol30"]
            b["fwd7"] = cl.shift(-7) / cl - 1
            b["fwd14"] = cl.shift(-14) / cl - 1
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["win"] = w
            s = np.sign(b.alloc)
            b["age"] = b.groupby((s != s.shift()).cumsum()).cumcount()
            br.append(b[["day", "gain", "alloc", "forecast", "er", "r30", "r7", "r90", "vol30", "volratio",
                         "fwd7", "fwd14", "pos", "coin", "win", "age"]])
    X = pd.concat(br, ignore_index=True)
    X["side"] = np.sign(X.alloc)
    act = X[X.alloc != 0].copy()
    act["absA"] = act.alloc.abs()
    def tab(df, col, q=4):
        z = df.dropna(subset=[col, "gain"]).copy()
        z["bin"] = pd.qcut(z[col], q, labels=False, duplicates="drop")
        g = z.groupby("bin")
        return pd.DataFrame({"n": g.gain.size(), "mid": g[col].mean(), "gain_mean": g.gain.mean(),
                             "gain_sd": g.gain.std(), "gain_sum": g.gain.sum()})
    try:
        out["active bar gain by side"] = act.groupby("side").gain.agg(["count", "mean", "std", "sum"])
        out["by |alloc|"] = tab(act, "absA")
        out["by vol30"] = tab(act, "vol30")
        out["by vol7/vol30"] = tab(act, "volratio")
        act["r90side"] = act.r90 * act.side
        out["by r90 in side"] = tab(act, "r90side")
        out["by age"] = act.assign(a=act.age.clip(upper=10)).groupby("a").gain.agg(["count", "mean"])
        out["side x year gain sum"] = act.assign(y=act.day.dt.year).groupby(["y", "side"]).gain.sum().unstack()
    except Exception as e:
        out["err1"] = str(e)[:200]
    # ---- falls
    try:
        eps = []; in_dd = False; n = len(B)
        for k in range(n):
            if dd[k] < 0 and not in_dd:
                in_dd = True; st = max(k - 1, 0)
            if in_dd and (dd[k] == 0 or k == n - 1):
                tr = st + int(np.argmin(dd[st:k + 1])); eps.append((dd[tr], st, tr)); in_dd = False
        eps = sorted(eps)[:5]
        rr = []
        for depth, st, tr in eps:
            keys = B.iloc[st + 1:tr + 1][["win", "day"]]
            f = X.merge(keys, on=["win", "day"]); fa = f[f.alloc != 0]
            rr.append({"depth": depth, "days": tr - st, "win": B.win.iloc[tr], "year": B.day.iloc[tr].year,
                       "hold_sum": B.hold.iloc[st + 1:tr + 1].sum(),
                       "long_share": (fa.side > 0).mean(), "long_gain": fa[fa.side > 0].gain.sum() / 6,
                       "short_gain": fa[fa.side < 0].gain.sum() / 6,
                       "absA": fa.alloc.abs().mean(), "vol30": fa.vol30.mean(),
                       "r90side": (fa.r90 * fa.side).mean(), "volratio": fa.volratio.mean()})
        out["5 deepest falls"] = pd.DataFrame(rr)
        out["overall"] = pd.Series({"maxdd": dd.min(), "act_vol30": act.vol30.mean(),
                                    "act_volratio": act.volratio.mean(), "act_absA": act.absA.mean()})
        out["book by year"] = B.assign(y=B.day.dt.year).groupby("y").agg(mean=("book", "mean"), sd=("book", "std"),
                                                                        mindd=("dd", "min"), hold=("hold", "mean"))
    except Exception as e:
        out["err2"] = str(e)[:200]
    # ---- grid cases
    try:
        G = X[X.pos % 7 == 0].dropna(subset=["fwd7"]).copy()
        drift = G.groupby("coin").fwd7.mean()
        G14 = X[X.pos % 14 == 0].dropna(subset=["fwd14"])
        drift14 = G14.groupby("coin").fwd14.mean()
        G["dir"] = np.sign(G.forecast.fillna(0))
        G["u7"] = (G.fwd7 - G.coin.map(drift)) * G.dir
        sig = G[G.dir != 0].copy()
        out["signal u7 by side"] = sig.groupby("dir").u7.apply(tstat).unstack()
        S14 = X[(X.pos % 14 == 0)].dropna(subset=["fwd14"]).copy()
        S14["dir"] = np.sign(S14.forecast.fillna(0)); S14 = S14[S14.dir != 0]
        S14["u14"] = (S14.fwd14 - S14.coin.map(drift14)) * S14.dir
        out["signal u14 by side"] = S14.groupby("dir").u14.apply(tstat).unstack()
        sig["vb"] = pd.qcut(sig.vol30, 3, labels=False)
        out["signal u7 by vol30 tercile"] = sig.groupby("vb").u7.apply(tstat).unstack()
        sig["vr"] = pd.qcut(sig.volratio, 3, labels=False)
        out["signal u7 by vol7/vol30 tercile"] = sig.groupby("vr").u7.apply(tstat).unstack()
        sig["r90s"] = sig.r90 * sig.dir
        sig["rb"] = pd.qcut(sig.r90s, 3, labels=False)
        out["signal u7 by r90-in-side tercile"] = sig.groupby("rb").u7.apply(tstat).unstack()
        sig["fb"] = pd.qcut(sig.forecast.abs(), 3, labels=False, duplicates="drop")
        out["signal u7 by |forecast| tercile"] = sig.groupby("fb").u7.apply(tstat).unstack()
        G2 = G[G.dir == 0].dropna(subset=["r7", "vol30", "r90", "volratio"]).copy()
        G2["d"] = np.sign(G2.r7)
        G2["u7"] = (G2.fwd7 - G2.coin.map(drift)) * G2.d
        G2["r90s"] = G2.r90 * G2.d
        G2["vb"] = np.digitize(G2.vol30, sig.vol30.quantile([1/3, 2/3]).values)
        G2["rb"] = np.digitize(G2.r90s, sig.r90s.quantile([1/3, 2/3]).values)
        G2["vr"] = np.digitize(G2.volratio, sig.volratio.quantile([1/3, 2/3]).values)
        out["no-signal u7 (dir r7) by vol tercile"] = G2.groupby("vb").u7.apply(tstat).unstack()
        out["no-signal u7 (dir r7) by r90 tercile"] = G2.groupby("rb").u7.apply(tstat).unstack()
        out["no-signal u7 (dir r7) by volratio tercile"] = G2.groupby("vr").u7.apply(tstat).unstack()
    except Exception as e:
        out["err3"] = str(e)[:200]
    return out
