def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index().sort_values(["wn", "day"])
    eq = (1 + B["book_return"]).cumprod()
    dd_ = eq / eq.cummax() - 1
    B["dd"] = dd_.values
    out["max_dd"] = float(dd_.min())
    # per-window book vs hold and worst drawdown within window
    g = B.groupby("wn")
    pw = pd.DataFrame({
        "book_sum": g["book_return"].sum(),
        "hold_sum": g["coin_return"].sum(),
        "book_minday": g["book_return"].min(),
        "dd_end": g["dd"].min(),
    })
    out["per_window"] = pw.round(4)
    # trades with context
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            b = data["bars"][c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            r = np.log(cl)
            ret1 = np.abs(np.diff(r, prepend=np.nan))
            vol30 = pd.Series(ret1).rolling(180, min_periods=60).mean().values
            vol30_long = pd.Series(ret1).rolling(1080, min_periods=180).mean().values
            for _, x in t.iterrows():
                et = pd.to_datetime(x["entry_time"])
                i = ts.searchsorted(et, side="right") - 1
                if i < 0: continue
                p30 = cl[i] / cl[max(0, i - 180)] - 1 if i >= 180 else np.nan
                p7 = cl[i] / cl[i - 42] - 1 if i >= 42 else np.nan
                tr.append(dict(coin=c, wn=int(w[1:]), net=x["net_profit_loss_percent"],
                               dur=x["duration_minutes"] / 1440, p30=p30, p7=p7,
                               volratio=vol30[i] / vol30_long[i] if vol30_long[i] > 0 else np.nan,
                               ef=x["entry_forecast"]))
    T = pd.DataFrame(tr)
    out["n_trades"] = len(T)
    out["trade_net_summary"] = T["net"].describe().round(3)
    def grp(col, q=5):
        s = T.dropna(subset=[col]).copy()
        s["q"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        a = s.groupby("q").agg(n=("net", "size"), lo=(col, "min"), hi=(col, "max"),
                               mean_net=("net", "mean"), med=("net", "median"),
                               worst=("net", "min"), share_neg=("net", lambda v: (v < 0).mean()))
        return a.round(3)
    out["by_prior30d"] = grp("p30")
    out["by_prior7d"] = grp("p7")
    out["by_volratio"] = grp("volratio")
    out["by_entryforecast"] = grp("ef")
    out["by_duration"] = grp("dur")
    out["by_coin"] = T.groupby("coin")["net"].agg(["size", "mean", "min"]).round(3)
    # worst 20 trades contexts aggregated
    w20 = T.nsmallest(40, "net")
    out["worst40_context"] = pd.Series({"mean_net": w20["net"].mean(), "mean_p30": w20["p30"].mean(),
        "mean_p7": w20["p7"].mean(), "mean_volratio": w20["volratio"].mean(), "mean_dur": w20["dur"].mean(),
        "all_p30": T["p30"].mean(), "all_p7": T["p7"].mean(), "all_volratio": T["volratio"].mean(),
        "all_dur": T["dur"].mean()}).round(3)
    # days in deepest drawdown stretch: book vs hold
    B["deep"] = B["dd"] < B["dd"].quantile(0.1)
    out["deep_dd_days"] = B.groupby("deep")[["book_return", "coin_return"]].mean().round(5)
    return out
