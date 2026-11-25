def explore(data):
    import pandas as pd, numpy as np
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns
    rows = []
    for c in coins:
        for w, d in days[c].items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["coin"] = c; t["win"] = w
            rows.append(t)
    D = pd.concat(rows)
    B = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B["wn"] = B.win.str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna(subset=["book"])
    v = (1 + B.book).cumprod().values
    peak = np.maximum.accumulate(v); dd = v / peak - 1
    B["dd"] = dd
    i = int(np.argmin(dd)); pk = int(np.argmax(v[:i + 1]))
    out["deepest fall"] = pd.Series({"depth": dd[i], "days_peak_to_trough": i - pk,
                                     "win_peak": B.win.iloc[pk], "win_trough": B.win.iloc[i]})
    # per window stats
    g = B.groupby("win")
    pw = pd.DataFrame({"book_sum": g.book.sum(), "hold_sum": g.hold.sum(),
                       "book_sd": g.book.std(), "n": g.book.size()})
    def mdd(x):
        vv = (1 + x).cumprod(); return (vv / vv.cummax() - 1).min()
    pw["mdd_in_win"] = g.book.apply(mdd)
    pw["wn"] = [int(s[1:]) for s in pw.index]
    out["per window"] = pw.sort_values("wn").drop(columns="wn")
    # bar-level gains with conditions
    br = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b.close
            r1 = cl.shift(-1) / cl - 1
            a = b.postRebalance_current_allocation
            b["gain"] = a * r1
            b["alloc"] = a
            dr = cl.pct_change()
            b["er"] = (cl - cl.shift(30)).abs() / dr.abs().rolling(30).sum().mul(1).where(False, (cl.diff().abs()).rolling(30).sum())
            b["r30"] = cl / cl.shift(30) - 1
            b["r7"] = cl / cl.shift(7) - 1
            b["vol30"] = dr.rolling(30).std()
            b["fwd7"] = cl.shift(-7) / cl - 1
            b["coin"] = c; b["win"] = w
            br.append(b[["gain", "alloc", "forecast", "er", "r30", "r7", "vol30", "fwd7", "coin", "win", "regime"]])
    X = pd.concat(br)
    X["side"] = np.sign(X.alloc)
    out["gain by side"] = X.groupby("side").gain.agg(["count", "mean", "sum"])
    act = X[X.alloc != 0].copy()
    act["absA"] = act.alloc.abs()
    act["Abin"] = pd.qcut(act.absA, 4, labels=False, duplicates="drop")
    out["gain by |alloc| quartile"] = act.groupby("Abin").agg(n=("gain", "size"), meanA=("absA", "mean"),
                                                             gain=("gain", "mean"), gsd=("gain", "std"))
    act["volbin"] = pd.qcut(act.vol30, 4, labels=False)
    out["gain by vol30 quartile"] = act.groupby("volbin").agg(n=("gain", "size"), vol=("vol30", "mean"),
                                                             gain=("gain", "mean"), gsd=("gain", "std"))
    act["r30abs"] = act.r30.abs()
    act["r30bin"] = pd.qcut(act.r30abs, 4, labels=False)
    out["gain by |r30| quartile"] = act.groupby("r30bin").agg(n=("gain", "size"), r30=("r30abs", "mean"),
                                                              gain=("gain", "mean"), gsd=("gain", "std"))
    out["gain by side x coin"] = act.groupby(["coin", "side"]).gain.mean().unstack()
    # trough period: what was held
    pkday, trday = B.day.iloc[pk], B.day.iloc[i]
    wset = set(B.win.iloc[pk:i + 1])
    fall = D[D.win.isin(wset)].copy()
    fall = fall.merge(B[["win", "day"]].iloc[pk:i + 1], on=["win", "day"])
    out["fall: per coin book_sum, coin_sum"] = fall.groupby("coin")[["book_return", "coin_return"]].sum()
    fx = X[X.win.isin(wset)]
    out["fall windows: side share"] = fx.groupby("win").side.value_counts(normalize=True).unstack()
    return out
