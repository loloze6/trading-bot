def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # build book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    wn = lambda s: int(s[1:])
    book = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    book["wi"] = book["w"].map(wn)
    book = book.sort_values(["wi", "day"]).dropna(subset=["br"])
    v = (1 + book["br"]).cumprod().values
    peak = np.maximum.accumulate(v)
    ddn = v / peak - 1
    book["dd"] = ddn
    out["book_overall"] = pd.Series({"mean": book.br.mean(), "std": book.br.std(), "maxdd": ddn.min(),
                                     "days": len(book), "sharpe": book.br.mean() / book.br.std() * np.sqrt(365)})
    # per window
    pw = book.groupby("wi").apply(lambda g: pd.Series({"ret": (1 + g.br).prod() - 1, "coin": (1 + g.cr).prod() - 1,
                                                       "worstday": g.br.min(), "days": len(g)}))
    out["per_window"] = pw
    # worst book days distribution
    out["worst_book_days"] = book.nsmallest(15, "br")[["wi", "br", "cr"]].reset_index(drop=True)
    # case-level
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            r = cl.pct_change()
            nxt = cl.shift(-1) / cl - 1
            sd30 = r.rolling(30).std()
            sd10 = r.rolling(10).std()
            sd60 = r.rolling(60).std()
            ret60 = cl / cl.shift(60) - 1
            ret5 = cl / cl.shift(5) - 1
            ret20 = cl / cl.shift(20) - 1
            # run length
            down = (r < 0).astype(int)
            runlen = np.zeros(len(b), int)
            cnt = 0
            prevrun = np.zeros(len(b), int)
            for i in range(len(b)):
                if r.iloc[i] < 0:
                    cnt += 1
                else:
                    prevrun[i] = cnt
                    cnt = 0
            df = pd.DataFrame({"coin": c, "w": wn(w), "pos": np.arange(len(b)),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "nxt": nxt, "up": r, "upz": r / sd30, "sd30": sd30,
                               "vr": sd10 / sd60, "ret60": ret60, "ret5": ret5, "ret20": ret20,
                               "run": prevrun, "rd": b.get("debug_info.components.run_depth.last_history_value"),
                               "hi": b["high"] / cl - 1})
            cs.append(df)
    C = pd.concat(cs)
    mu = C.groupby("coin")["nxt"].mean()
    C["mu"] = C.coin.map(mu)
    C["un"] = -(C.nxt - C.mu)
    C["tot"] = -C.nxt
    K = C[(C.fc < 0) & C.nxt.notna()].copy()
    K["pnl"] = K.alloc * K.nxt
    out["cases_n"] = len(K)
    def g(col, q=4):
        K["_q"] = pd.qcut(K[col], q, duplicates="drop")
        return K.groupby("_q").agg(n=("un", "size"), un=("un", "mean"), tot=("tot", "mean"),
                                   pnl=("pnl", "mean"), pnl_worst5=("pnl", lambda x: x.quantile(0.05)),
                                   alloc=("alloc", "mean"))
    for col in ["vr", "upz", "run", "ret60", "ret5", "ret20", "sd30", "rd"]:
        out["by_" + col] = g(col)
    out["by_year_window"] = K.groupby("w").agg(n=("un", "size"), un=("un", "mean"), pnl=("pnl", "mean"))
    # worst case losses: features
    W = K.nsmallest(40, "pnl")
    out["worst40_vs_all"] = pd.DataFrame({"worst40": W[["nxt", "up", "upz", "vr", "run", "ret60", "ret5", "alloc", "sd30"]].mean(),
                                          "all": K[["nxt", "up", "upz", "vr", "run", "ret60", "ret5", "alloc", "sd30"]].mean()})
    # pnl contribution of top 5% next-day rises
    out["pnl_sum_share_worst10pct"] = K.pnl[K.pnl < K.pnl.quantile(0.1)].sum() / K.pnl.sum()
    return out
