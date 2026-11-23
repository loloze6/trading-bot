def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    wins = sorted({w for c in days for w in days[c]}, key=lambda s: int(s[1:]))
    # book daily
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["w"] = w; dd["coin"] = c
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("coin", "count")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna(subset=["br"])
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1 + B["br"]).cumprod(); peak = v.cummax(); dd_ = v / peak - 1
    B["dd"] = dd_.values
    # drawdown episodes
    i_trough = dd_.values.argmin()
    i_peak = v.values[:i_trough + 1].argmax()
    ep = B.iloc[i_peak:i_trough + 1]
    out = {}
    out["deepest_fall"] = pd.Series({"depth": dd_.min(), "days": len(ep), "windows": ",".join(sorted(ep.w.unique(), key=lambda s:int(s[1:]))),
                                     "years": ",".join(map(str, sorted(ep.year.unique()))),
                                     "coin_mean_ret_in_fall": ep.cr.mean(), "book_sum_in_fall": ep.br.sum()})
    # per window book stats
    g = B.groupby("w")
    pw = pd.DataFrame({"book_sum": g.br.sum(), "coin_sum": g.cr.sum(), "min_dd": g.dd.min(), "ncoins": g.n.mean()})
    pw = pw.loc[sorted(pw.index, key=lambda s:int(s[1:]))]
    out["per_window"] = pw
    out["per_year"] = B.groupby("year").agg(book_mean=("br","mean"), book_sd=("br","std"), coin_mean=("cr","mean"), ndays=("br","count"))
    # Sunday cases
    cases = []
    for c in bars:
        drift_parts = []
        for w, b in bars[c].items():
            cl = b["close"].values
            drift_parts.append(cl[2::2][:len(cl[0::2])-0][:len(cl[2::2])] / cl[0::2][:len(cl[2::2])] - 1)
        drift = np.nanmean(np.concatenate(drift_parts)) if drift_parts else 0
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]; r1 = cl.pct_change()
            vr = r1.rolling(20).std() / r1.rolling(60).std()
            f2 = cl.shift(-2) / cl - 1
            r20 = cl / cl.shift(20) - 1
            r5 = cl / cl.shift(5) - 1
            volu = b["volume"] / b["volume"].rolling(30).mean()
            alloc = b["postRebalance_current_allocation"]
            df = pd.DataFrame({"coin": c, "w": w, "wd": ts.dt.weekday, "year": ts.dt.year, "r1": r1, "vr": vr, "f2": f2 - drift,
                               "r20": r20, "r5": r5, "volu": volu, "fc": b["forecast"], "alloc": alloc,
                               "absr": r1.abs() / r1.rolling(60).std()})
            cases.append(df)
    C = pd.concat(cases).dropna(subset=["f2", "r1"])
    C["dirret"] = -np.sign(C["r1"]) * C["f2"]
    S = C[(C.wd == 6) & (C.fc != 0)].copy()
    S["side"] = np.where(S.fc > 0, "long(after down Sun)", "short(after up Sun)")
    def summ(x):
        return pd.Series({"n": len(x), "mean_dir": x.dirret.mean(), "t": x.dirret.mean() / (x.dirret.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["sun_by_side"] = S.groupby("side").apply(summ)
    S["vrq"] = pd.qcut(S.vr, 5, labels=False, duplicates="drop")
    out["sun_by_volratio_q"] = S.groupby("vrq").apply(summ)
    S["mq"] = pd.qcut(S.absr, 5, labels=False, duplicates="drop")
    out["sun_by_movesize_q"] = S.groupby("mq").apply(summ)
    # trend agreement: sunday move with or against 20d trend
    S["with_trend"] = np.sign(S.r1) == np.sign(S.r20 - S.r1)
    out["sun_by_with20dtrend_side"] = S.groupby(["with_trend", "side"]).apply(summ)
    out["sun_by_year"] = S.groupby("year").apply(summ)
    # weekday comparison: all other days, same reversal bet
    W = C[(C.wd != 6)].copy()
    W = W.iloc[::2]
    W["vrq"] = pd.qcut(W.vr, 5, labels=False, duplicates="drop")
    out["weekday_rev_by_vrq"] = W.groupby("vrq").apply(summ)
    # book in fall: by side holding
    return out
