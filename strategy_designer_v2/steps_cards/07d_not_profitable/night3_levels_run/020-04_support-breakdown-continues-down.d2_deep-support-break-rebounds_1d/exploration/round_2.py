def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 5
    rows = []
    for coin, ws in data["bars"].items():
        g = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            g += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(g); usual = np.std(g)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            raw = b["debug_info.components.support_break.last_history_value"]
            r1 = c / c.shift(1) - 1
            r5 = c / c.shift(5) - 1
            dd = c / c.rolling(60, min_periods=10).max() - 1
            alloc = b["postRebalance_current_allocation"].fillna(0)
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                fr = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, raw=raw.iloc[i], r1=r1.iloc[i], r5=r5.iloc[i],
                                 dd=dd.iloc[i], al=alloc.iloc[i], fr=fr, un=fr - drift, st=(fr - drift) / usual))
    df = pd.DataFrame(rows)
    def summ(g):
        n = len(g)
        return pd.Series(dict(n=n, un=g.un.mean(), t=g.un.mean() / (g.un.std() / np.sqrt(n)) if n > 2 else np.nan,
                              tot=g.fr.mean(), st=g.st.mean()))
    sit = df[df.raw > 0].copy()
    sit["rd"] = pd.qcut(sit.raw.rank(method="first"), 10, labels=False)
    out["raw_deciles"] = sit.groupby("rd").apply(summ)
    top = sit[sit.rd >= 8].copy()
    top["r5q"] = pd.qcut(top.r5, 3, labels=False)
    out["top_raw_by_r5"] = top.groupby("r5q").apply(summ)
    out["top_raw_by_coin"] = top.groupby("coin").apply(summ)
    out["top_raw_by_window_sign"] = pd.Series(dict(windows=top.groupby("w").un.mean().shape[0],
        pos=(top.groupby("w").un.mean() > 0).mean()))
    nos = df[df.raw == 0].copy()
    nos["ddq"] = pd.qcut(nos.dd, 3, labels=False)
    out["nosupport_by_dd"] = nos.groupby("ddq").apply(summ)
    # book falls: deepest drawdowns of the averaged book
    dl = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dl.append(pd.DataFrame(dict(w=w, day=d["day"].values, br=d["book_return"].values, cr=d["coin_return"].values)))
    D = pd.concat(dl).groupby(["w", "day"]).mean().reset_index()
    D["wn"] = D.w.str[1:].astype(int)
    D = D.sort_values(["wn", "day"])
    eq = (1 + D.br.fillna(0)).cumprod().values
    peak = np.maximum.accumulate(eq)
    ddb = eq / peak - 1
    D["ddb"] = ddb
    out["book_dd_by_window"] = D.groupby("wn").agg(book=("br", "mean"), coin=("cr", "mean"), mindd=("ddb", "min")).round(4)
    out["deepest_book_dd"] = float(ddb.min())
    # book gain split: in-situation vs out
    out["alloc_by_raw_state"] = pd.Series(dict(alloc_raw_pos=sit.al.mean(), alloc_raw0=nos.al.mean()))
    return out
