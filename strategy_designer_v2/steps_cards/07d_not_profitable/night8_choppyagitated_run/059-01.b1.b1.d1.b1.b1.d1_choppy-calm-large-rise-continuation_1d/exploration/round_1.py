def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    # ---- book daily returns (mean over coins per day), chained by window
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna()
    B["v"] = (1 + B["br"]).cumprod()
    B["peak"] = B["v"].cummax()
    B["dd"] = B["v"] / B["peak"] - 1
    byw = B.groupby("w").agg(book_mean=("br", "mean"), coin_mean=("cr", "mean"), n=("br", "size"),
                             book_sum=("br", "sum"), coin_sum=("cr", "sum"), worst_dd=("dd", "min"))
    byw["sharpe_book"] = B.groupby("w")["br"].apply(lambda x: x.mean() / x.std() * np.sqrt(365) if x.std() > 0 else np.nan)
    byw["sharpe_coin"] = B.groupby("w")["cr"].apply(lambda x: x.mean() / x.std() * np.sqrt(365))
    out["by_window"] = byw.round(4)
    # deepest fall episodes
    B = B.reset_index(drop=True)
    i_tr = B["dd"].idxmin()
    i_pk = B.loc[:i_tr, "v"].idxmax()
    out["deepest_fall"] = pd.DataFrame({"depth": [B.loc[i_tr, "dd"]], "days": [i_tr - i_pk],
        "window_start": [B.loc[i_pk, "w"]], "window_trough": [B.loc[i_tr, "w"]],
        "coin_mean_sum_during": [B.loc[i_pk:i_tr, "cr"].sum()], "book_sum_during": [B.loc[i_pk:i_tr, "br"].sum()]})
    fall_days = set(zip(B.loc[i_pk:i_tr, "w"], B.loc[i_pk:i_tr, "day"]))
    D["infall"] = [(w, d) in fall_days for w, d in zip(D["w"], D["day"])]
    out["fall_contrib_by_coin"] = D[D["infall"]].groupby("coin")["book_return"].sum().round(4)
    # ---- trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            tt = t.copy(); tt["coin"] = c; tt["w"] = w; T.append(tt)
    T = pd.concat(T)
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["trades_by_fc_tercile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
        mean_days=("duration_minutes", lambda x: x.mean() / 1440), mean_fc=("entry_forecast", "mean")).round(3)
    out["trades_by_window"] = T.groupby("w").agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), sum_net=("net_profit_loss_percent", "sum")).round(2)
    # ---- grid features per coin-window
    G = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float); n = len(cl)
            s = pd.Series(cl)
            r7 = s / s.shift(7) - 1
            mabs = r7.abs().rolling(30).mean()
            sr = r7 / mabs
            r60 = s / s.shift(60) - 1
            hi30 = s.rolling(30).max()
            dret = s.pct_change()
            vol30 = dret.rolling(30).std()
            for p in range(0, n - 14, 14):
                f = {"coin": c, "w": w, "fc": b["forecast"].iloc[p], "reg": b["regime"].iloc[p],
                     "sr": sr.iloc[p], "r7": r7.iloc[p], "r60": r60.iloc[p],
                     "near_hi": cl[p] / hi30.iloc[p] if not np.isnan(hi30.iloc[p]) else np.nan,
                     "f7": cl[p + 7] / cl[p] - 1, "f14": cl[p + 14] / cl[p] - 1,
                     "f28": cl[p + 28] / cl[p] - 1 if p + 28 < n else np.nan,
                     "ts": b["timestamp"].iloc[p]}
                G.append(f)
    G = pd.DataFrame(G)
    drift14 = G["f14"].mean(); drift28 = G["f28"].mean(); drift7 = G["f7"].mean()
    out["drift"] = pd.Series({"d7": drift7, "d14": drift14, "d28": drift28, "n": len(G)}).round(4)
    def summ(x, col="f14", d=None):
        d = drift14 if d is None else d
        e = x[col].dropna() - d
        return pd.Series({"n": len(e), "mean_ex": e.mean(), "t": e.mean() / (e.std() / np.sqrt(len(e))) if len(e) > 2 else np.nan})
    inprof = G[G["reg"] == "unknown"]
    grp = {"profile_all": inprof, "profile_sig": inprof[inprof["fc"] > 0],
           "profile_nosig_rise": inprof[(inprof["fc"] <= 0) & (inprof["sr"] > 0)],
           "profile_fall": inprof[inprof["sr"] <= 0], "outside_rise": G[(G["reg"] != "unknown") & (G["sr"] > 0)]}
    res = {}
    for k, v in grp.items():
        for col, dd in [("f7", drift7), ("f14", drift14), ("f28", drift28)]:
            s_ = summ(v, col, dd); res[(k, col)] = s_
    out["groups_horizons"] = pd.DataFrame(res).T.round(4)
    sig = inprof[inprof["fc"] > 0].copy()
    if len(sig) > 6:
        sig["q"] = pd.qcut(sig["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
        out["sig_by_fc_tercile"] = sig.groupby("q").apply(lambda x: pd.concat([summ(x), summ(x, "f28", drift28).add_prefix("28_"),
            pd.Series({"sr": x["sr"].mean(), "near_hi": x["near_hi"].mean(), "r60": x["r60"].mean()})])).round(4)
        sig["trendhalf"] = np.where(sig["r60"] > 0, "r60>0", "r60<=0")
        sig["hi"] = np.where(sig["near_hi"] >= 0.97, "near30hi", "below")
        out["sig_by_r60sign"] = sig.groupby("trendhalf").apply(summ).round(4)
        out["sig_by_near_high"] = sig.groupby("hi").apply(summ).round(4)
        out["sig_by_window"] = sig.groupby("w").apply(summ).round(4)
        out["sig_by_coin"] = sig.groupby("coin").apply(summ).round(4)
    # conditions alone in profile without signal
    ns = inprof[inprof["fc"] <= 0].copy()
    ns["hi"] = np.where(ns["near_hi"] >= 0.97, "near30hi", "below")
    ns["trendhalf"] = np.where(ns["r60"] > 0, "r60>0", "r60<=0")
    out["nosig_by_near_high"] = ns.groupby("hi").apply(summ).round(4)
    out["nosig_by_r60sign"] = ns.groupby("trendhalf").apply(summ).round(4)
    return out
