def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            for H in (5, 10, 20):
                b[f"fwd{H}"] = c.shift(-H) / c - 1
            b["past20"] = c / c.shift(20) - 1
            b["past60"] = c / c.shift(60) - 1
            b["inprof"] = (b["regime"] == "unknown")
            b["coin"] = coin
            b["pos"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["alloc"] = b["postRebalance_current_allocation"]
            b["next_ret"] = c.shift(-1) / c - 1
            b["gain"] = b["alloc"] * b["next_ret"]
            rows.append(b[["coin", "win" if "win" in b else "pos", "pos", "year", "fwd5", "fwd10", "fwd20",
                           "forecast", "inprof", "past20", "past60", "alloc", "gain"]].assign(win=w))
    A = pd.concat(rows, ignore_index=True)

    def grid(H):
        g = A[(A["pos"] % H == 0) & A[f"fwd{H}"].notna()].copy()
        g["ex"] = g[f"fwd{H}"] - g["coin"].map(g.groupby("coin")[f"fwd{H}"].mean())
        return g[g["inprof"]]

    def summ(df, by):
        return df.groupby(by, observed=True).agg(
            n=("ex", "size"), mean_ex=("ex", "mean"),
            t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    for H in (5, 10, 20):
        P = grid(H)
        P["fb"] = pd.cut(P["forecast"], [-21, -15, -2, -0.01, 0.01], labels=["strong<-15", "-15..-2", "-2..0", "0"])
        out[f"h{H}_by_strength"] = summ(P, "fb")

    P = grid(5)
    P["fb"] = pd.cut(P["forecast"], [-21, -15, -2, -0.01, 0.01], labels=["strong", "mid", "weak", "zero"])
    out["past20_edges"] = pd.Series(P["past20"].quantile([1/3, 2/3]).values, index=["q33", "q67"])
    P["p20"] = pd.cut(P["past20"], [-9, -0.25, -0.15, -0.05, 0.0, 9],
                      labels=["<-25%", "-25..-15", "-15..-5", "-5..0", ">0"])
    out["p20_x_strength"] = summ(P, ["p20", "fb"])
    P["p60"] = pd.cut(P["past60"], [-9, -0.4, -0.25, -0.1], labels=["<-40%", "-40..-25", "-25..-10"])
    out["p60_x_strength"] = summ(P, ["p60", "fb"])
    out["strong_x_year"] = summ(P[P["fb"] == "strong"], "year")

    # book bars: gain by forecast strength (daily, all bars)
    I = A[A["alloc"].abs() > 1e-9].copy()
    I["fb"] = pd.cut(I["forecast"], [-21, -15, -10, -5, -2, -0.01, 0.01, 21],
                     labels=["<-15", "-15..-10", "-10..-5", "-5..-2", "-2..0", "0", ">0"])
    out["held_bars_gain_by_forecast"] = I.groupby("fb", observed=True).agg(
        n=("gain", "size"), mean_gain=("gain", "mean"), mean_abs_alloc=("alloc", lambda x: x.abs().mean()))
    I["p20"] = pd.cut(I["past20"], [-9, -0.25, -0.15, -0.05, 0.0, 9],
                      labels=["<-25%", "-25..-15", "-15..-5", "-5..0", ">0"])
    out["held_bars_gain_by_past20"] = I.groupby("p20", observed=True).agg(n=("gain", "size"), mean_gain=("gain", "mean"))

    T = pd.concat([t.assign(coin=c, win=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    T["eb"] = pd.cut(T["entry_forecast"], [-21, -15, -10, -5, -2, -0.01, 21])
    out["trades_by_entry_forecast"] = T.groupby("eb", observed=True).agg(
        n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
        med_days=("duration_minutes", lambda x: (x / 1440).median()))
    out["trades_short_dur_side"] = T[T["duration_minutes"] / 1440 <= 5.5].groupby("side").agg(
        n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
        mean_entry_fc=("entry_forecast", "mean"))
    return out
