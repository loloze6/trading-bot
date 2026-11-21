def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # ---- book daily returns, by window/day; market part vs timing
    rows = []
    bar_rows = []
    for c, wd in bars.items():
        # coin mean daily return over all windows
        dr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu_d = dr.mean()
        for w, b in wd.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["day"] = b["ts"].dt.floor("D")
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["alloc"] = b["postRebalance_current_allocation"].fillna(0)
            b["coin"] = c; b["win"] = w
            bar_rows.append(b[["coin", "win", "ts", "day", "close", "high", "alloc", "ret1", "forecast"]])
            d = days[c][w].copy()
            d["day"] = pd.to_datetime(d["day"], utc=True).dt.floor("D")
            pos = b.groupby("day")["alloc"].mean()
            d["pos"] = d["day"].map(pos).fillna(0)
            d["mkt"] = d["pos"].shift(1).fillna(0) * mu_d
            d["coin"] = c; d["win"] = w
            d["year"] = d["day"].dt.year
            # coin trailing 30-day return as market state
            d["st30"] = d["close"] / d["close"].shift(30) - 1
            rows.append(d)
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    bk = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    out["book_split"] = pd.Series({"book_mean": bk.book.mean(), "mkt_part": bk.mkt.mean(),
                                   "timing": bk.book.mean() - bk.mkt.mean(), "hold_mean": bk.hold.mean(),
                                   "book_sharpe": bk.book.mean() / bk.book.std() * np.sqrt(365), "ndays": len(bk)})
    # per coin contribution (share of book mean)
    nd = len(bk)
    pc = D.groupby("coin").agg(sum_ret=("book_return", "sum"), sum_mkt=("mkt", "sum"), days=("book_return", "size"))
    # contribution to book mean: each day's coin return / ncoins that day
    ncoin = D.groupby(["win", "day"])["coin"].transform("size")
    D["contrib"] = D["book_return"] / ncoin
    D["contrib_mkt"] = D["mkt"] / ncoin
    pc["contrib"] = D.groupby("coin")["contrib"].sum() / nd
    pc["contrib_mkt"] = D.groupby("coin")["contrib_mkt"].sum() / nd
    out["per_coin"] = pc[["days", "contrib", "contrib_mkt"]].sort_values("contrib")
    pw = pd.DataFrame({"contrib": D.groupby("win")["contrib"].sum() / nd,
                       "contrib_mkt": D.groupby("win")["contrib_mkt"].sum() / nd,
                       "hold": D.groupby("win")["coin_return"].mean()})
    out["per_window"] = pw
    out["per_year"] = pd.DataFrame({"contrib": D.groupby("year")["contrib"].sum() / nd,
                                    "contrib_mkt": D.groupby("year")["contrib_mkt"].sum() / nd})
    # market state: coin trailing 30d return quintile, book return per coin-day
    D2 = D.dropna(subset=["st30"]).copy()
    D2["stq"] = pd.qcut(D2["st30"], 5, labels=False)
    out["by_state30"] = D2.groupby("stq").agg(st30=("st30", "mean"), contrib=("contrib", "sum"),
                                              coin_ret=("coin_return", "mean"), pos=("pos", "mean"),
                                              bookret=("book_return", "mean"))
    out["by_state30"]["contrib"] /= nd
    # ---- trades concentration
    T = pd.concat([t.assign(coin=c) for c, wd in data["trades"].items() for w, t in wd.items() if len(t)])
    pl = T["net_profit_loss_percent"].dropna().sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(pl), "mean": pl.mean(), "median": pl.median(), "win_share": (pl > 0).mean(),
                               "top10_share_of_sum": pl.head(10).sum() / pl.sum(),
                               "top5pct_share": pl.head(max(1, len(pl) // 20)).sum() / pl.sum(),
                               "dur_days_med": T["duration_minutes"].median() / 1440})
    # ---- horizons: breakout bars, unusual move by h
    B = pd.concat(bar_rows)
    res = []
    for h in [3, 6, 18, 36, 72, 144]:
        cases = []
        for (c, w), b in B.groupby(["coin", "win"], sort=False):
            b = b.reset_index(drop=True)
            brk = b["close"] > b["high"].shift(1).rolling(12).max()
            fwd = b["close"].shift(-h) / b["close"] - 1
            r42 = b["close"] / b["close"].shift(42) - 1
            nonov = fwd.iloc[::h]
            g = pd.DataFrame({"brk": brk, "fwd": fwd, "r42": r42, "cell": np.arange(len(b)) // h, "c": c})
            g = g[g.brk & g.fwd.notna()].groupby("cell").first()
            cases.append((c, g, nonov.dropna()))
        # drift per coin from all windows
        allc = {}
        for c, g, n in cases:
            allc.setdefault(c, []).append(n)
        drift = {c: pd.concat(v).mean() for c, v in allc.items()}
        sd = {c: pd.concat(v).std() for c, v in allc.items()}
        G = pd.concat([g.assign(u=g.fwd - drift[c], s=(g.fwd - drift[c]) / sd[c], c=c) for c, g, n in cases])
        t = G.u.mean() / (G.u.std() / np.sqrt(len(G)))
        G2 = G.dropna(subset=["r42"])
        sl = stats.linregress(G2.r42, G2.u)
        res.append({"h_days": h / 6, "n": len(G), "unusual": G.u.mean(), "t": t, "total": G.fwd.mean(),
                    "strength": G.s.mean(), "slope_t_r42": sl.slope / sl.stderr,
                    "u_top_r42_tercile": G2[G2.r42 > G2.r42.quantile(2 / 3)].u.mean(),
                    "u_low_r42_tercile": G2[G2.r42 < G2.r42.quantile(1 / 3)].u.mean()})
        if h == 72:
            G2 = G2.copy(); G2["q"] = pd.qcut(G2.r42, 5, labels=False)
            out["h72_by_r42_quintile"] = G2.groupby("q").agg(r42=("r42", "mean"), u=("u", "mean"), n=("u", "size"),
                                                             t=("u", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["horizons_breakout"] = pd.DataFrame(res)
    return out
