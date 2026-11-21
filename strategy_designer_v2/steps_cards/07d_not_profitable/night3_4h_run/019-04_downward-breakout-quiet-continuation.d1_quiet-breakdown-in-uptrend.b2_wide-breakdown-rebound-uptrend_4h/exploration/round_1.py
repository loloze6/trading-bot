def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily, mean over coins per day, chained by window order
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    eq = (1 + B["book_return"]).cumprod()
    dd_ = eq / eq.cummax() - 1
    B["dd"] = dd_.values
    out["window_book"] = B.groupby("wn").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                              worst_dd=("dd", "min"), n=("book_return", "size"))
    # per-case analysis from bars
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; lo = b["low"].values; hi = b["high"].values
            n = len(b)
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            lowmin = pd.Series(lo).shift(1).rolling(12).min().values
            himax = pd.Series(hi).shift(1).rolling(12).max().values
            rng = pd.Series(hi - lo).rolling(180).mean().values
            r30 = cl / pd.Series(cl).shift(180).values - 1
            r7 = cl / pd.Series(cl).shift(42).values - 1
            r1 = cl / pd.Series(cl).shift(6).values - 1
            vol = pd.Series(np.log(cl)).diff().rolling(42).std().values
            vol180 = pd.Series(np.log(cl)).diff().rolling(180).std().values
            for t in range(n - 18):
                if prev[t] <= 1e-9 and alloc[t] > 1e-9:
                    cases.append(dict(coin=c, wn=int(w[1:]), fwd=cl[t + 18] / cl[t] - 1,
                                      depth=(cl[t] / lowmin[t] - 1),
                                      width=(himax[t] - lowmin[t]) / rng[t] if rng[t] else np.nan,
                                      r30=r30[t], r7=r7[t], r1=r1[t], volratio=vol[t] / vol180[t],
                                      alloc=alloc[t],
                                      hour=pd.Timestamp(b["timestamp"].iloc[t]).hour,
                                      year=pd.Timestamp(b["timestamp"].iloc[t]).year))
    C = pd.DataFrame(cases)
    # drift per coin: non-overlapping 18-bar grid
    drift = {}
    for c, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 18, 18)
            rr += list(cl[idx + 18] / cl[idx] - 1)
        drift[c] = np.mean(rr)
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    out["n_entries"] = len(C)
    out["overall"] = pd.Series({"fwd": C.fwd.mean(), "ex": C.ex.mean(), "t": stats.ttest_1samp(C.ex, 0)[0]})
    def grp(col, q=5):
        g = pd.qcut(C[col], q, duplicates="drop")
        r = C.groupby(g).agg(n=("ex", "size"), fwd=("fwd", "mean"), ex=("ex", "mean"),
                             sd=("ex", "std"), hit=("fwd", lambda x: (x > 0).mean()))
        r["t"] = r.ex / (r.sd / np.sqrt(r.n))
        r.index = r.index.astype(str)
        return r
    for col in ["depth", "width", "r30", "r7", "r1", "volratio"]:
        out["by_" + col] = grp(col)
    out["by_coin"] = C.groupby("coin").agg(n=("ex", "size"), fwd=("fwd", "mean"), ex=("ex", "mean"))
    out["by_year"] = C.groupby("year").agg(n=("ex", "size"), fwd=("fwd", "mean"), ex=("ex", "mean"))
    out["by_window"] = C.groupby("wn").agg(n=("ex", "size"), fwd=("fwd", "mean"), ex=("ex", "mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
                               "mean_gross": T.profit_loss_percent.mean(),
                               "med_dur_h": T.duration_minutes.median() / 60,
                               "hit": (T.net_profit_loss_percent > 0).mean()})
    return out
