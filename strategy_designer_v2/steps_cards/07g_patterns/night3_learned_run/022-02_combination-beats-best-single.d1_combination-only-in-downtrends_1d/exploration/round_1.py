def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []; daily = []
    for coin in bars:
        # coin drift over all windows (5-bar, non-overlapping)
        allr5 = []; allr1 = []
        for w, df in bars[coin].items():
            c = df["close"].reset_index(drop=True)
            idx = np.arange(0, len(c) - 5, 5)
            allr5 += list((c.shift(-5) / c - 1).iloc[idx].dropna())
            allr1 += list((c.shift(-1) / c - 1).dropna())
        d5 = np.mean(allr5); d1 = np.mean(allr1); sd5 = np.std(allr5, ddof=1)
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "w": w,
                "fwd5": c.shift(-5) / c - 1 - d5,
                "fwd5z": (c.shift(-5) / c - 1 - d5) / sd5,
                "fwd1": c.shift(-1) / c - 1 - d1,
                "past1": r1, "past5": c / c.shift(5) - 1, "past20": c / c.shift(20) - 1,
                "vol20": r1.rolling(20).std(),
                "range": (df["high"] - df["low"]) / c,
                "fc": df["forecast"], "alloc": df["postRebalance_current_allocation"],
                "regime": df["regime"],
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(df["timestamp"]).dt.year,
                "grid": (np.arange(len(df)) % 5 == 0),
            })
            f["near_hi"] = c / c.rolling(30).max() - 1
            rows.append(f)
        for w, dd in days[coin].items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w
            x["yr"] = pd.to_datetime(dd["day"]).dt.year
            daily.append(x)
    B = pd.concat(rows, ignore_index=True)
    G = B[B["grid"]].copy()
    def tab(col, target="fwd5z", q=5, sub=G):
        s = sub.dropna(subset=[col, target]).copy()
        s["q"] = s.groupby("coin")[col].transform(lambda v: pd.qcut(v.rank(method="first"), q, labels=False))
        g = s.groupby("q")[target]
        out = pd.DataFrame({"mean": g.mean(), "n": g.size(),
                            "t": g.mean() / (g.std() / np.sqrt(g.size()))})
        slope = stats.spearmanr(s[col], s[target])
        out.loc["rho", "mean"] = slope.correlation; out.loc["rho", "t"] = slope.pvalue
        return out
    res = {}
    res["regime_share"] = B["regime"].value_counts(normalize=True)
    act = G[G["fc"].fillna(0) != 0]
    res["fc_quint_active"] = tab("fc", sub=act)
    res["past1_quint"] = tab("past1")
    res["past5_quint"] = tab("past5")
    res["past20_quint"] = tab("past20")
    res["vol20_quint_absfwd"] = tab("vol20", target="fwd5z")
    res["nearhi_quint"] = tab("near_hi")
    res["range_quint"] = tab("range")
    # weekday on all bars, 1-day
    wdg = B.dropna(subset=["fwd1"]).groupby("wd")["fwd1"]
    res["weekday_fwd1"] = pd.DataFrame({"mean": wdg.mean(), "n": wdg.size(), "t": wdg.mean()/(wdg.std()/np.sqrt(wdg.size()))})
    D = pd.concat(daily, ignore_index=True).dropna()
    yg = D.groupby("yr")
    res["book_by_year"] = pd.DataFrame({"book": yg["book_return"].mean(), "coin": yg["coin_return"].mean(), "n": yg.size()})
    cg = D.groupby("coin")
    res["book_by_coin"] = pd.DataFrame({"book": cg["book_return"].mean(), "coin": cg["coin_return"].mean(),
                                        "sharpe": cg["book_return"].mean()/cg["book_return"].std()*np.sqrt(365)})
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()], ignore_index=True)
    tg = T.groupby("side")["net_profit_loss_percent"]
    res["trades_by_side"] = pd.DataFrame({"mean": tg.mean(), "median": tg.median(), "n": tg.size(),
                                          "t": tg.mean()/(tg.std()/np.sqrt(tg.size()))})
    # active share by sign
    res["alloc_sign_share"] = np.sign(B["alloc"].fillna(0)).value_counts(normalize=True)
    return res
