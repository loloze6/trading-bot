def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            n = len(b)
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            rng = pd.Series(h - l)
            ratio = (rng.rolling(6).mean() / rng.rolling(180).mean()).values
            cs = pd.Series(c)
            r6 = (cs / cs.shift(6) - 1).values
            r42 = (cs / cs.shift(42) - 1).values
            r180 = (cs / cs.shift(180) - 1).values
            vol = pd.Series(b["volume"].values)
            vr = (vol.rolling(6).mean() / vol.rolling(180).mean()).values
            for t in range(n):
                if prev[t] <= 1e-9 and alloc[t] > 1e-9:
                    def fr(k):
                        return c[t + k] / c[t] - 1 if t + k < n else np.nan
                    j = t
                    while j + 1 < n and alloc[j + 1] > 1e-9:
                        j += 1
                    hold = c[min(j + 1, n - 1)] / c[t] - 1
                    path = c[t:min(t + 85, n)] / c[t] - 1
                    rows.append(dict(coin=coin, w=w, alloc=alloc[t], ratio=ratio[t], r6=r6[t],
                                     r42=r42[t], r180=r180[t], vr=vr[t],
                                     f6=fr(6), f18=fr(18), f42=fr(42), f84=fr(84),
                                     mae=path.min(), hold=hold, holdbars=j - t + 1,
                                     year=pd.Timestamp(b["timestamp"].iloc[t]).year))
    e = pd.DataFrame(rows)
    out["n_entries_by_coin"] = e.groupby("coin").agg(n=("f84", "size"), f84=("f84", "mean"),
                                                     hold=("hold", "mean"), mae=("mae", "mean"),
                                                     alloc=("alloc", "mean"), bars=("holdbars", "mean"))
    out["entries_by_year"] = e.groupby("year").agg(n=("f84", "size"), f84=("f84", "mean"), hold=("hold", "mean"))
    out["path_mean"] = e[["f6", "f18", "f42", "f84", "mae", "hold"]].describe().T
    for col in ["r6", "r42", "r180", "ratio", "vr", "f6", "f18"]:
        x = e[[col, "hold"]].dropna()
        x["q"] = pd.qcut(x[col], 3, labels=False, duplicates="drop")
        out["hold_by_tercile_" + col] = x.groupby("q").agg(n=("hold", "size"), lo=(col, "min"),
                                                         hi=(col, "max"), hold=("hold", "mean"),
                                                         med=("hold", "median"))
    # book exposure and daily chain
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            dd.append(d)
    D = pd.concat(dd)
    D["wn"] = D["w"].str[1:].astype(int)
    bk = D.groupby(["wn", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean")).dropna().reset_index()
    bk = bk.sort_values(["wn", "day"])
    v = (1 + bk["b"]).cumprod(); peak = v.cummax(); ddn = v / peak - 1
    bk["dd"] = ddn.values
    out["book_daily"] = pd.Series(dict(mean=bk["b"].mean(), sd=bk["b"].std(), maxdd=ddn.min(),
                                       days=len(bk), coin_mean=bk["c"].mean(),
                                       share_days_nonzero=(bk["b"].abs() > 1e-9).mean()))
    # worst days and per-window book return
    out["book_by_window"] = bk.groupby("wn").agg(sum_b=("b", "sum"), sum_c=("c", "sum"), mindd=("dd", "min")).round(4)
    i_trough = ddn.values.argmin(); i_peak = peak.values[:i_trough + 1]
    pk = int(np.where(v.values[:i_trough + 1] == peak.values[i_trough])[0][0])
    seg = bk.iloc[pk:i_trough + 1]
    out["deepest_fall"] = pd.Series(dict(start_wn=seg["wn"].iloc[0], end_wn=seg["wn"].iloc[-1], days=len(seg),
                                         book=(1 + seg["b"]).prod() - 1, coins=(1 + seg["c"]).prod() - 1))
    return out
