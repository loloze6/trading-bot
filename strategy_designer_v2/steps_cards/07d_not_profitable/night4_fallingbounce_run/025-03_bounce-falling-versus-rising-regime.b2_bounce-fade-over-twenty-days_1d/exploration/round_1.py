def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily returns per window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"])
    def sh(x):
        x = x.dropna()
        return x.mean() / x.std() * np.sqrt(365) if x.std() > 0 else np.nan
    perw = B.groupby("wn").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                               book_sh=("book_return", sh), coin_sh=("coin_return", sh),
                               year=("day", lambda s: pd.to_datetime(s).dt.year.mode()[0]))
    loo = []
    for w in perw.index:
        x = B[B.wn != w]
        loo.append((w, sh(x.book_return), sh(x.coin_return)))
    perw["loo_book_sh"] = [l[1] for l in loo]
    perw["loo_coin_sh"] = [l[2] for l in loo]
    out["per window"] = perw
    # chained drawdown
    v = (1 + B.book_return.fillna(0)).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd.values
    out["max dd"] = float(dd.min())
    out["dd by window (min)"] = B.groupby("wn")["dd"].min()
    # bar gains by side and regime, per coin
    g = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            r = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"]
            x = pd.DataFrame({"gain": a * r, "a": a, "r": r, "regime": b["regime"], "coin": c,
                              "wn": int(w[1:])})
            x["side"] = np.sign(a)
            g.append(x)
    G = pd.concat(g).dropna()
    out["gain by side"] = G.groupby("side").agg(n=("gain", "size"), sum_gain=("gain", "sum"),
                                                mean_gain=("gain", "mean"), mean_r=("r", "mean"), mean_abs_a=("a", lambda s: s.abs().mean()))
    out["gain by coin and side"] = G[G.side != 0].groupby(["coin", "side"])["gain"].sum().unstack()
    out["gain by window and side"] = G[G.side != 0].groupby(["wn", "side"])["gain"].sum().unstack()
    out["share of bars by side"] = G.side.value_counts(normalize=True)
    # trades
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T)
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
                                                  mean_net=("net_profit_loss_percent", "mean"),
                                                  median_net=("net_profit_loss_percent", "median"),
                                                  win=("net_profit_loss_percent", lambda s: (s > 0).mean()),
                                                  mean_days=("duration_minutes", lambda s: s.mean() / 1440))
    return out
