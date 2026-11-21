def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            dfs.append(d.set_index("day")[["book_return", "coin_return"]].add_suffix("_" + c))
        m = pd.concat(dfs, axis=1)
        br = m[[x for x in m.columns if x.startswith("book_return")]].mean(axis=1)
        cr = m[[x for x in m.columns if x.startswith("coin_return")]].mean(axis=1)
        rows.append(pd.DataFrame({"w": w, "b": br.values, "c": cr.values}))
    B = pd.concat(rows, ignore_index=True).dropna()
    eq = (1 + B["b"]).cumprod()
    dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    out["deepest_fall"] = float(dd.min())
    # drawdown episode by window
    trough = dd.idxmin()
    peak = eq[:trough].idxmax()
    out["fall_windows"] = B.loc[peak:trough].groupby("w").agg(book=("b", lambda x: (1 + x).prod() - 1), coins=("c", lambda x: (1 + x).prod() - 1), n=("b", "size"))
    pw = B.groupby("w").agg(book=("b", lambda x: (1 + x).prod() - 1), coins=("c", lambda x: (1 + x).prod() - 1), mindd=("dd", "min"))
    out["per_window"] = pw.reindex(wins)
    # trades: entries from bars with features
    recs = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            sma50 = cl.rolling(50, min_periods=20).mean()
            r20p = cl / cl.shift(20) - 1
            r60p = cl / cl.shift(60) - 1
            vol = np.log(cl).diff().rolling(20, min_periods=10).std()
            hi90 = cl.rolling(90, min_periods=20).max()
            pos = b["postRebalance_current_allocation"].fillna(0)
            prev = pos.shift(1).fillna(0)
            ent = b.index[(prev <= 1e-9) & (pos > 1e-9)]
            for i in ent:
                j = min(i + 20, len(b) - 1)
                # forward with mae
                seg = cl.iloc[i:j + 1] / cl.iloc[i] - 1
                recs.append(dict(c=c, w=w, ma=cl[i] / sma50[i] - 1 if sma50[i] == sma50[i] else np.nan,
                                 r20p=r20p[i], r60p=r60p[i], vol=vol[i], nearhi=cl[i] / hi90[i] - 1,
                                 fwd=seg.iloc[-1], mae=seg.min(), alloc=pos[i], fc=b["forecast"][i]))
    T = pd.DataFrame(recs)
    out["n_entries"] = len(T)
    out["fwd_stats"] = T[["fwd", "mae"]].describe()
    for col in ["ma", "r20p", "r60p", "vol", "nearhi", "fc"]:
        q = pd.qcut(T[col], 4, duplicates="drop")
        out["by_" + col] = T.groupby(q, observed=True).agg(n=("fwd", "size"), fwd=("fwd", "mean"), mae=("mae", "mean"), lossshare=("fwd", lambda x: (x < -0.1).mean()))
    out["by_coin"] = T.groupby("c").agg(n=("fwd", "size"), fwd=("fwd", "mean"), mae=("mae", "mean"))
    return out
