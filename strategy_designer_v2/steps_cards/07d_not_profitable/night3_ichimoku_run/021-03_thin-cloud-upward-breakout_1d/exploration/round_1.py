def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns, combined across coins by window/day
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    # invested share
    inv = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"].fillna(0)
            inv.append({"coin": c, "w": w, "inv": (a.abs() > 1e-6).mean(), "alloc": a.abs().mean()})
    I = pd.DataFrame(inv)
    out["invested_by_coin"] = I.groupby("coin")[["inv", "alloc"]].mean()
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    v = (1 + B["br"]).cumprod(); dd = v / v.cummax() - 1
    B["dd"] = dd.values
    out["book_mean_sd"] = pd.Series({"mean": B.br.mean(), "sd": B.br.std(), "maxdd": dd.min(), "n": len(B)})
    out["by_window"] = B.groupby("wn").agg(book=("br", "mean"), coin=("cr", "mean"), mindd=("dd", "min")).round(5)
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["by_year"] = B.groupby("year").agg(book=("br", "mean"), coin=("cr", "mean"), n=("br", "size"))
    # trades with features
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            b = data["bars"][c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            for _, r in t.iterrows():
                et = pd.to_datetime(r["entry_time"])
                i = ts.searchsorted(et)
                if i >= len(b): continue
                cl = b["close"]
                def pr(k):
                    return cl.iloc[i] / cl.iloc[i - k] - 1 if i - k >= 0 else np.nan
                lr = np.log(cl).diff()
                T.append({"coin": c, "w": w, "net": r["net_profit_loss_percent"], "gross": r["profit_loss_percent"],
                          "dur": r["duration_minutes"] / 1440, "r7": pr(7), "r14": pr(14), "r28": pr(28),
                          "vol": b["sizing_realised_vol"].iloc[i], "prox": b["debug_info.components.thin_cloud.last_history_value"].iloc[i],
                          "fc": r["entry_forecast"], "alloc": b["postRebalance_current_allocation"].iloc[i],
                          "year": et.year, "wd_from_end": len(b) - i})
    T = pd.DataFrame(T)
    out["trades_summary"] = T[["net", "gross", "dur", "alloc", "r7", "r14", "r28", "vol", "prox"]].describe().round(4)
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net", "size"), net=("net", "mean"), win=("net", lambda x: (x > 0).mean()), dur=("dur", "mean"))
    q = {}
    for f in ["r7", "r14", "r28", "vol", "prox", "fc", "dur"]:
        s = T.dropna(subset=[f, "net"])
        if len(s) < 20: continue
        g = pd.qcut(s[f].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        m = s.groupby(g)["net"].agg(["mean", "count"])
        rho = stats.spearmanr(s[f], s["net"])
        q[f] = {"lo": m.loc["lo", "mean"], "mid": m.loc["mid", "mean"], "hi": m.loc["hi", "mean"], "n": len(s), "rho": rho[0], "p": rho[1]}
    out["net_by_tercile"] = pd.DataFrame(q).T.round(4)
    out["by_year_trades"] = T.groupby("year")["net"].agg(["mean", "count"])
    # deepest drawdown episodes: book chain dd segments
    B["indd"] = B["dd"] < -0.1
    out["dd_days_share"] = pd.Series({"dd<10%": B.indd.mean(), "dd<20%": (B.dd < -0.2).mean()})
    out["worst_windows_dd"] = B.groupby("wn")["br"].apply(lambda x: ((1 + x).cumprod() / (1 + x).cumprod().cummax() - 1).min()).sort_values().head(6)
    return out
