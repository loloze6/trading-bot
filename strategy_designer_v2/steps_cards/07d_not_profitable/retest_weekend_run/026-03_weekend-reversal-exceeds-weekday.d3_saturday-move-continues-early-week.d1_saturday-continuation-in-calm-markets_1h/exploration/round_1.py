def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # portfolio daily returns
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    P = P.dropna(subset=["b"])
    eq = (1 + P["b"]).cumprod(); peak = eq.cummax(); dd = eq / peak - 1
    P["dd"] = dd.values; P["eq"] = eq.values
    P["year"] = pd.to_datetime(P["day"]).dt.year
    i = P["dd"].idxmin()
    trough = P.loc[i]
    pk_i = P.loc[:i, "eq"].idxmax()
    out["deepest fall"] = pd.Series({"depth": trough["dd"], "peak_w": P.loc[pk_i, "wn"], "trough_w": trough["wn"],
                                     "peak_year": P.loc[pk_i, "year"], "trough_year": trough["year"],
                                     "days": (P.index.get_loc(i) - P.index.get_loc(pk_i))})
    out["by year"] = P.groupby("year").agg(n=("b", "size"), mean_b=("b", "mean"), sum_b=("b", "sum"), min_b=("b", "min"), mean_h=("h", "mean"))
    out["by window"] = P.groupby("wn").agg(sum_b=("b", "sum"), min_dd=("dd", "min"), sum_h=("h", "sum"))
    # trades with features
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values
            r = np.log(cl[1:] / cl[:-1]); r = np.concatenate([[np.nan], r])
            vol720 = pd.Series(r).rolling(720, min_periods=300).std().values
            vol168 = pd.Series(r).rolling(168, min_periods=100).std().values
            idx = pd.Series(np.arange(len(b)), index=ts)
            for _, tr in t.iterrows():
                et = pd.to_datetime(tr["entry_time"])
                j = idx.index.searchsorted(et, side="right") - 1
                if j < 48: continue
                sgn = 1 if tr["side"] == "LONG" else -1
                sat = cl[j-24] / cl[j-48] - 1; sun = cl[j] / cl[j-24] - 1
                prev7 = cl[j] / cl[max(j-168, 0)] - 1
                fut = cl[j+1:min(j+49, len(cl))]
                mae = (np.min(sgn * (fut / cl[j] - 1)) if len(fut) else np.nan)
                T.append(dict(coin=c, wn=int(w[1:]), year=et.year, side=tr["side"], net=tr["net_profit_loss_percent"],
                              gross=tr["profit_loss_percent"], f=abs(tr["entry_forecast"]),
                              sat_z=abs(sat) / (vol720[j-24] * np.sqrt(24)) if vol720[j-24] > 0 else np.nan,
                              sun_dir=sgn * sun, prev7_dir=sgn * prev7,
                              vshort=vol168[j] / vol720[j], mae=mae, alloc=abs(b["postRebalance_current_allocation"].iloc[j])))
    T = pd.DataFrame(T)
    out["n trades"] = len(T)
    out["by side"] = T.groupby("side").agg(n=("net", "size"), mean=("net", "mean"), sum=("net", "sum"))
    out["by coin"] = T.groupby("coin").agg(n=("net", "size"), mean=("net", "mean"), sum=("net", "sum"), alloc=("alloc", "mean"))
    T["fq"] = pd.qcut(T["f"], 5, labels=False, duplicates="drop")
    out["by |forecast| quintile"] = T.groupby("fq").agg(n=("net", "size"), mean=("net", "mean"), f=("f", "mean"), mae=("mae", "mean"))
    T["sunq"] = pd.qcut(T["sun_dir"], 5, labels=False)
    out["by sunday move in dir quintile"] = T.groupby("sunq").agg(n=("net", "size"), mean=("net", "mean"), sun=("sun_dir", "mean"))
    T["p7q"] = pd.qcut(T["prev7_dir"], 5, labels=False)
    out["by prior 7d in dir quintile"] = T.groupby("p7q").agg(n=("net", "size"), mean=("net", "mean"), p7=("prev7_dir", "mean"))
    T["vsq"] = pd.qcut(T["vshort"], 5, labels=False)
    out["by 7d/30d vol quintile"] = T.groupby("vsq").agg(n=("net", "size"), mean=("net", "mean"), vs=("vshort", "mean"), mae=("mae", "mean"))
    out["mae quantiles"] = T["mae"].quantile([0.05, 0.1, 0.25, 0.5])
    # stop simulation not exact; worst trades share
    srt = T.sort_values("net")
    out["worst 5% trades sum vs total"] = pd.Series({"worst5": srt["net"].head(int(len(T)*0.05)).sum(), "total": T["net"].sum(), "pos": T.loc[T.net > 0, "net"].sum()})
    trough_w = int(trough["wn"]); pk_w = int(P.loc[pk_i, "wn"])
    inDD = T[(T.wn >= pk_w) & (T.wn <= trough_w)]
    out["trades in deepest-fall windows"] = inDD.groupby(["coin", "side"]).agg(n=("net", "size"), sum=("net", "sum"), sun=("sun_dir", "mean"), vs=("vshort", "mean"))
    return out
