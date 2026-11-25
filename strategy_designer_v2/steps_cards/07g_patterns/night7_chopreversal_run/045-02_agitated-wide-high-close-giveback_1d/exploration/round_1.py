def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data.get("bars", {}) or {}
    days = data.get("days", {}) or {}
    trades = data.get("trades", {}) or {}
    inv = []
    for c in bars:
        for w in bars[c]:
            df = bars[c][w]
            inv.append({"coin": c, "window": w, "rows": len(df), "ncols": df.shape[1],
                        "has_forecast": int("forecast" in df.columns),
                        "trades": len(trades.get(c, {}).get(w, [])) if trades.get(c, {}).get(w) is not None else 0})
    out["inventory"] = pd.DataFrame(inv) if inv else "no bars"
    if not inv:
        out["days_inventory"] = str({c: list(days[c].keys()) for c in days})
        return out
    # columns of first table
    c0 = list(bars)[0]; w0 = list(bars[c0])[0]
    out["columns"] = ", ".join(map(str, bars[c0][w0].columns[:40]))
    # pattern: close location x range multiple vs next-day return, by agitation recomputed
    rows = []
    for c in bars:
        for w in bars[c]:
            df = bars[c][w].copy()
            if not {"high","low","close"}.issubset(df.columns) or len(df) < 60:
                continue
            df = df.reset_index(drop=True)
            rng = (df["high"] - df["low"])
            loc = (df["close"] - df["low"]) / rng.replace(0, np.nan)
            mult = rng / rng.rolling(30, min_periods=20).mean()
            r = df["close"].pct_change()
            vol30 = r.rolling(30, min_periods=20).std()
            pct = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            nxt = df["close"].shift(-1) / df["close"] - 1
            ret5 = df["close"] / df["close"].shift(5) - 1
            ts = pd.to_datetime(df["timestamp"]) if "timestamp" in df.columns else pd.Series(pd.NaT, index=df.index)
            d = pd.DataFrame({"coin": c, "window": w, "loc": loc, "mult": mult, "r": r, "nxt": nxt,
                              "pct": pct, "ret5": ret5, "wd": ts.dt.weekday,
                              "fc": df["forecast"] if "forecast" in df.columns else np.nan,
                              "alloc": df["postRebalance_current_allocation"] if "postRebalance_current_allocation" in df.columns else np.nan,
                              "regime": df["regime"] if "regime" in df.columns else np.nan})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    mu = A.groupby("coin")["nxt"].transform("mean")
    A["ex"] = A["nxt"] - mu
    A["sig"] = (2 * A["loc"] - 1) * A["mult"]
    A["agit"] = np.where(A["pct"] > 0.5, "agitated", np.where(A["pct"].notna(), "calm", "na"))
    B = A.dropna(subset=["loc", "mult", "ex"])
    def tab(g):
        return pd.Series({"n": len(g), "mean_ex_%": g["ex"].mean() * 100,
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    B = B.assign(locq=pd.qcut(B["loc"], 5, labels=False), multq=pd.qcut(B["mult"], 3, labels=False))
    out["loc_quintile_by_agit"] = B.groupby(["agit", "locq"]).apply(tab).reset_index()
    out["loc_x_width_agitated"] = B[B.agit == "agitated"].groupby(["multq", "locq"]).apply(tab).reset_index()
    out["corr_sig_ex_by_agit"] = B.groupby("agit").apply(lambda g: pd.Series({"n": len(g), "spearman": stats.spearmanr(g["sig"], g["ex"])[0], "p": stats.spearmanr(g["sig"], g["ex"])[1]})).reset_index()
    out["corr_sig_ex_by_coin_agitated"] = B[B.agit == "agitated"].groupby("coin").apply(lambda g: pd.Series({"n": len(g), "spearman": stats.spearmanr(g["sig"], g["ex"])[0], "p": stats.spearmanr(g["sig"], g["ex"])[1]})).reset_index()
    # day return quintile -> next day (reversal after large moves)
    B["rq"] = pd.qcut(B["r"], 5, labels=False)
    out["ret_quintile_next"] = B.groupby(["agit", "rq"]).apply(tab).reset_index()
    out["weekday_next"] = B.groupby("wd").apply(tab).reset_index()
    out["mult_tercile_next_raw"] = B.groupby(["agit", "multq"]).apply(tab).reset_index()
    # forecast & book
    if A["fc"].notna().any():
        F = A.dropna(subset=["fc", "ex"])
        F = F[F["fc"] != 0]
        if len(F):
            F = F.assign(tg=F["fc"] / 10 * F["ex"])
            out["forecast_share_nonzero"] = len(F) / max(1, A["fc"].notna().sum())
            out["timing_gain_t"] = F["tg"].mean() / (F["tg"].std() / np.sqrt(len(F)))
            out["fc_quintile_next"] = F.assign(fq=pd.qcut(F["fc"], 5, labels=False, duplicates="drop")).groupby("fq").apply(lambda g: pd.Series({"n": len(g), "fc_mean": g["fc"].mean(), "mean_ex_%": g["ex"].mean()*100})).reset_index()
    # book
    br = []
    for c in days:
        for w in days[c]:
            d = days[c][w]
            br.append(d[["book_return", "coin_return"]].assign(coin=c, window=w))
    if br:
        D = pd.concat(br).dropna()
        out["book_by_window"] = D.groupby("window").agg(n=("book_return", "size"), book_mean_pct=("book_return", lambda x: x.mean()*100), coin_mean_pct=("coin_return", lambda x: x.mean()*100)).reset_index()
        out["book_by_coin"] = D.groupby("coin").agg(book_mean_pct=("book_return", lambda x: x.mean()*100), sd=("book_return", "std")).reset_index()
    return out
