def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wn = lambda s: int(s[1:])
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = wn(w)
            rows.append(dd)
    D = pd.concat(rows)
    book = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    book = book.sort_values(["w", "day"]).dropna(subset=["br"]).reset_index(drop=True)
    v = (1 + book["br"]).cumprod().values
    peak = np.maximum.accumulate(v)
    book["dd"] = v / peak - 1
    # drawdown episodes
    ep = []; start = None
    for i in range(len(book)):
        if book.dd.iloc[i] < 0 and start is None: start = i
        if book.dd.iloc[i] == 0 and start is not None:
            seg = book.iloc[start:i]; ep.append((start, i, seg.dd.min(), seg.w.iloc[0], len(seg))); start = None
    if start is not None:
        seg = book.iloc[start:]; ep.append((start, len(book), seg.dd.min(), seg.w.iloc[0], len(seg)))
    E = pd.DataFrame(ep, columns=["s", "e", "depth", "w", "len"]).sort_values("depth").head(6)
    out["dd_episodes"] = E[["depth", "w", "len"]].reset_index(drop=True)
    # cases
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            sd30 = r.rolling(30).std()
            prevrun = np.zeros(len(b), int); cnt = 0
            for i in range(len(b)):
                if r.iloc[i] < 0: cnt += 1
                else: prevrun[i] = cnt; cnt = 0
            df = pd.DataFrame({"coin": c, "w": wn(w), "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "n1": cl.shift(-1) / cl - 1, "n2": cl.shift(-2) / cl - 1, "n3": cl.shift(-3) / cl - 1,
                               "up": r, "upz": r / sd30, "sd30": sd30,
                               "vr": r.rolling(10).std() / r.rolling(60).std(),
                               "ret60": cl / cl.shift(60) - 1, "ret5": cl / cl.shift(5) - 1,
                               "run": prevrun})
            df["sig"] = (df.up > 0) & (df.run > 0) & (df.ret60 < -0.10)
            cs.append(df)
    C = pd.concat(cs).reset_index(drop=True)
    for h in ["n1", "n2", "n3"]:
        C["u" + h] = -(C[h] - C.coin.map(C.groupby("coin")[h].mean()))
    K = C[(C.fc < 0) & C.n1.notna()].copy()
    K["pnl"] = K.alloc * K.n1
    # cases on the days of the deepest episodes
    bd = book.copy()
    for k, rw in E.head(3).reset_index(drop=True).iterrows():
        seg = bd.iloc[int(rw.s):int(rw.e)]
        keys = set(zip(seg.w, seg.day))
        # case bar day -> loss appears next day
        Ki = K[[((ww, dd + pd.Timedelta(days=1)) in keys) for ww, dd in zip(K.w, K.day)]]
        out[f"ep{k}_cases"] = pd.Series({"n": len(Ki), "pnl_sum": Ki.pnl.sum(), "n1": Ki.n1.mean(),
                                         "vr": Ki.vr.mean(), "ret5": Ki.ret5.mean(), "run": Ki.run.mean(),
                                         "upz": Ki.upz.mean(), "alloc": Ki.alloc.mean(), "ret60": Ki.ret60.mean(),
                                         "coins_per_day": Ki.groupby("day").size().mean()})
    # cases per day vs pnl
    pd_ = K.groupby("day").agg(k=("pnl", "size"), pnl=("pnl", "sum"), un=("un1", "mean"))
    pd_["kq"] = pd_.k.clip(upper=4)
    out["by_cases_per_day"] = pd_.groupby("kq").agg(days=("pnl", "size"), pnl=("pnl", "mean"),
                                                    worst=("pnl", "min"), un=("un", "mean"))
    # horizons
    out["horizons"] = pd.DataFrame({h: [K["u" + h].mean(), K["u" + h].mean() / K["u" + h].std() * np.sqrt(K["u" + h].notna().sum()), K["u"+h].quantile(0.05)] for h in ["n1", "n2", "n3"]}, index=["un", "t", "q05"])
    # condition-alone checks: ret5 low, in falling markets
    F = C[(C.ret60 < -0.10) & C.n1.notna()].copy()
    F["r5lo"] = F.ret5 < -0.076
    out["ret5_alone_vs_both"] = F.groupby(["r5lo", "sig"]).agg(n=("un1", "size"), un1=("un1", "mean"),
                                                               t=("un1", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    F["vrhi"] = F.vr > 1.167
    out["vr_alone_vs_both"] = F.groupby(["vrhi", "sig"]).agg(n=("un1", "size"), un1=("un1", "mean"),
                                                             t=("un1", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # risk-adjusted by vr and ret5 quartiles
    for col in ["vr", "ret5", "upz"]:
        K["_q"] = pd.qcut(K[col], 4, duplicates="drop")
        out["ratio_" + col] = K.groupby("_q").agg(n=("pnl", "size"), pnl=("pnl", "mean"), sd=("pnl", "std"),
                                                  q01=("pnl", lambda x: x.quantile(0.01)), un=("un1", "mean"))
    # upz x ret5
    K["upbig"] = K.upz > 1.0
    K["r5lo"] = K.ret5 < -0.076
    out["upz_x_ret5"] = K.groupby(["r5lo", "upbig"]).agg(n=("pnl", "size"), pnl=("pnl", "mean"),
                                                         q05=("pnl", lambda x: x.quantile(0.05)), un=("un1", "mean"))
    return out
