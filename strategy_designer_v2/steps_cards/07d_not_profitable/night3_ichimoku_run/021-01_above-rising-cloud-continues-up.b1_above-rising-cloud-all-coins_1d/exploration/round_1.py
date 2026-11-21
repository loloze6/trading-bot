def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    # ---------- book daily: by window, day ----------
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    # allocation at day's end from bars
    arows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            t = pd.to_datetime(b["timestamp"])
            x = pd.DataFrame({"day": t.dt.floor("D"), "alloc": b["postRebalance_current_allocation"].values,
                              "fc": b["forecast"].values})
            x = x.groupby("day").last().reset_index()
            x["coin"] = c; x["w"] = w
            arows.append(x)
    A = pd.concat(arows)
    D["day"] = pd.to_datetime(D["day"])
    if D["day"].dt.tz is not None and A["day"].dt.tz is None:
        A["day"] = A["day"].dt.tz_localize(D["day"].dt.tz)
    elif D["day"].dt.tz is None and A["day"].dt.tz is not None:
        A["day"] = A["day"].dt.tz_localize(None)
    D = D.merge(A, on=["coin", "w", "day"], how="left")
    D = D.sort_values(["coin", "wn", "day"])
    D["alloc_prev"] = D.groupby(["coin", "w"])["alloc"].shift(1)
    cm = D.groupby("coin")["coin_return"].mean()
    D["mkt_part"] = D["alloc_prev"] * D["coin"].map(cm)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"),
                                     expo=("alloc_prev", lambda s: (s.abs() > 0.01).mean()),
                                     alloc=("alloc_prev", "mean"), mkt=("mkt_part", "mean")).reset_index()
    B = B.sort_values(["wn", "day"]).dropna(subset=["book"])
    out["book_summary"] = pd.Series({
        "book_mean": B.book.mean(), "hold_mean": B.hold.mean(), "mkt_part_mean": B.mkt.mean(),
        "timing_mean": B.book.mean() - B.mkt.mean(), "mean_alloc": B.alloc.mean(), "share_coins_in": B.expo.mean(),
        "book_sharpe": B.book.mean() / B.book.std() * np.sqrt(365),
        "hold_sharpe": B.hold.mean() / B.hold.std() * np.sqrt(365)})
    v = (1 + B.book.fillna(0)).cumprod()
    dd = v / v.cummax() - 1
    i_tr = dd.values.argmin()
    i_pk = v.values[:i_tr + 1].argmax()
    seg = B.iloc[i_pk:i_tr + 1]
    hv = (1 + B.hold.fillna(0)).cumprod()
    out["deepest_fall"] = pd.Series({"fall": dd.min(), "days": len(seg), "windows_spanned": seg.wn.nunique(),
        "book_chain": (1 + seg.book).prod() - 1, "hold_chain": (1 + seg.hold).prod() - 1,
        "mean_alloc_in_fall": seg.alloc.mean(), "share_in_fall": seg.expo.mean(),
        "hold_deepest_fall": (hv / hv.cummax() - 1).min()})
    # top falls by window
    B["v"] = v.values
    bw = B.groupby("wn").agg(book=("book", "mean"), hold=("hold", "mean"), alloc=("alloc", "mean"),
                             expo=("expo", "mean"), n=("book", "size"))
    bw["book_chain"] = B.groupby("wn")["book"].apply(lambda s: (1 + s).prod() - 1)
    bw["hold_chain"] = B.groupby("wn")["hold"].apply(lambda s: (1 + s).prod() - 1)
    out["by_window"] = bw.round(4)
    # ---------- grid cases with features ----------
    cases = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                allr.append(cl[i + H] / cl[i] - 1)
        mu = np.mean(allr) if allr else np.nan
        for w, b in ws.items():
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(cl)
            rv = b["sizing_realised_vol"].values if "sizing_realised_vol" in b else np.full(n, np.nan)
            bir = pd.to_numeric(b.get("debug_info.bars_in_regime", pd.Series(np.nan, index=b.index)), errors="coerce").values
            for i in range(0, n - H, H):
                f = b["forecast"].values[i]
                r = cl[i + H] / cl[i] - 1
                past = cl[i] / cl[i - H] - 1 if i >= H else np.nan
                h26 = hi[max(0, i - H + 1):i + 1].max() if i >= H - 1 else np.nan
                cases.append(dict(coin=c, w=int(w[1:]), fc=f, r=r, ex=r - mu, past=past,
                                  nearhi=cl[i] / h26 - 1 if h26 == h26 else np.nan, vol=rv[i], bir=bir[i],
                                  reg=b["regime"].values[i],
                                  fwdmin=cl[i:i + H + 1].min() / cl[i] - 1))
    C = pd.DataFrame(cases)
    C["in"] = C.fc > 0
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "t": g.ex.mean() / g.ex.std() * np.sqrt(len(g)) if len(g) > 2 else np.nan,
                          "mean_r": g.r.mean(), "share_up": (g.r > 0).mean(), "mean_worst": g.fwdmin.mean()})
    out["in_vs_out"] = C.groupby("in").apply(summ).round(4)
    I = C[C["in"]].copy()
    for col in ["fc", "past", "nearhi", "vol", "bir"]:
        s = I[col]
        if s.notna().sum() > 40:
            I["q"] = pd.qcut(s.rank(method="first"), 4, labels=False)
            t = I.dropna(subset=[col]).groupby("q").apply(summ)
            t["feat_mean"] = I.dropna(subset=[col]).groupby("q")[col].mean()
            out["in_by_" + col] = t.round(4)
    O = C[~C["in"]].copy()
    if O.past.notna().sum() > 40:
        O["q"] = pd.qcut(O.past.rank(method="first"), 4, labels=False)
        t = O.dropna(subset=["past"]).groupby("q").apply(summ); t["feat_mean"] = O.dropna(subset=["past"]).groupby("q")["past"].mean()
        out["out_by_past"] = t.round(4)
    out["in_by_year_window_group"] = I.assign(g=pd.cut(I.w, [0, 6, 12, 18, 24])).groupby("g").apply(summ).round(4)
    # ---------- trades ----------
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = c; tr.append(t)
    T = pd.concat(tr)
    T["days"] = T.duration_minutes / 1440
    out["trades"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(), "median_net": T.net_profit_loss_percent.median(),
                               "win": (T.net_profit_loss_percent > 0).mean(), "mean_days": T.days.mean(),
                               "mean_comm": T.total_commission.mean() if "total_commission" in T else np.nan})
    T["dq"] = pd.cut(T.days, [0, 13, 26, 27, 40, 80, 1000])
    out["trades_by_days"] = T.groupby("dq")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
