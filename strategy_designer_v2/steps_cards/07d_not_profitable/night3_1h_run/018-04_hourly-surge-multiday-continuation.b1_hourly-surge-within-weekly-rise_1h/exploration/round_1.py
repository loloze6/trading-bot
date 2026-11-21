import pandas as pd, numpy as np

def explore(data):
    out = {}
    # book daily returns: mean over coins per day within window
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["book_return"])
    eq = (1 + B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    B["dd"] = dd
    i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(eq[:i_tr+1]))
    out["deepest_fall"] = pd.Series({"depth": dd[i_tr], "days": i_tr - i_pk,
        "w_start": B["wn"].iloc[i_pk], "w_end": B["wn"].iloc[i_tr],
        "coin_ret_chain_in_fall": np.prod(1 + B["coin_return"].iloc[i_pk+1:i_tr+1].fillna(0)) - 1,
        "yearly": eq[-1] ** (365 / len(eq)) - 1})
    # per window: book return, coin return, maxdd
    pw = []
    for wn, g in B.groupby("wn"):
        e = (1 + g["book_return"]).cumprod()
        c = (1 + g["coin_return"].fillna(0)).cumprod()
        pw.append({"w": wn, "book": e.iloc[-1] - 1, "coins": c.iloc[-1] - 1,
                   "book_mdd": (e / e.cummax() - 1).min(), "coin_mdd": (c / c.cummax() - 1).min()})
    out["per_window"] = pd.DataFrame(pw).set_index("w").round(3)
    # trades with entry features
    T = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            f = pd.DataFrame({"ts": ts.values})
            f["r24"] = (c / c.shift(24) - 1).values
            f["r168"] = (c / c.shift(168) - 1).values
            f["r720"] = (c / c.shift(720) - 1).values
            hr = c.pct_change()
            f["vol_ratio"] = (hr.rolling(168).std() / hr.rolling(720).std()).values
            f["off_high720"] = (c / c.rolling(720).max() - 1).values
            f["ret_prior_hour"] = (c / c.shift(1) - 1).values
            t = data["trades"][coin][w]
            if len(t) == 0: continue
            t = t.copy()
            t["et"] = pd.to_datetime(t["entry_time"], utc=True)
            # trade entries are at bar close; match to bar whose start <= entry
            m = pd.merge_asof(t.sort_values("et"), f.sort_values("ts"), left_on="et", right_on="ts", direction="backward")
            m["coin"] = coin
            T.append(m)
    T = pd.concat(T)
    T = T[T["side"] == "LONG"]
    out["trades_summary"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
        "median_net": T["net_profit_loss_percent"].median(), "win": (T["net_profit_loss_percent"] > 0).mean(),
        "mean_dur_h": T["duration_minutes"].mean() / 60, "p10": T["net_profit_loss_percent"].quantile(.1)})
    res = {}
    for col in ["r24", "r168", "r720", "vol_ratio", "off_high720", "ret_prior_hour"]:
        x = T.dropna(subset=[col])
        q = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        g = x.groupby(q)
        res[col] = pd.DataFrame({"lo": g[col].min(), "hi": g[col].max(), "n": g.size(),
            "mean_net": g["net_profit_loss_percent"].mean(),
            "share_below_-10": g["net_profit_loss_percent"].apply(lambda s: (s < -10).mean())})
    for k, v in res.items():
        out["q_" + k] = v.round(4)
    out["by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median", "min"]).round(3)
    return out
