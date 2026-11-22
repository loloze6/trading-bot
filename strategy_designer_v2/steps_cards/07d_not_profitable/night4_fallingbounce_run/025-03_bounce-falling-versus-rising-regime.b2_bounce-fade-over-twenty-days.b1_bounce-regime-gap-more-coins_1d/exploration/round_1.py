def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    barrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").copy()
            b["ret_next"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret_next"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"] = coin; b["window"] = w
            b["r90"] = b["close"] / b["close"].shift(90) - 1
            b["r20"] = b["close"] / b["close"].shift(20) - 1
            barrows.append(b[["coin","window","day","pos","gain","ret_next","regime","forecast","r20"]])
            d = data["days"][coin][w].copy()
            d["coin"] = coin; d["window"] = w
            rows.append(d[["coin","window","day","book_return","coin_return"]])
    D = pd.concat(rows); B = pd.concat(barrows)
    B["side"] = np.where(B["pos"] > 0, "long", np.where(B["pos"] < 0, "short", "flat"))
    port = D.groupby(["window","day"])[["book_return","coin_return"]].mean().dropna()
    port["wn"] = port.index.get_level_values(0).str[1:].astype(int)
    port = port.reset_index().sort_values(["wn","day"])
    for c in ["book_return","coin_return"]:
        x = port[c]
        out_sh = x.mean()/x.std()*np.sqrt(365)
        out["sharpe_"+c] = round(out_sh,3)
    eq = (1+port["book_return"]).cumprod()
    dd = eq/eq.cummax()-1
    port["dd"] = dd.values
    out["max_dd_book"] = round(dd.min(),4)
    heq = (1+port["coin_return"]).cumprod(); out["max_dd_hold"] = round((heq/heq.cummax()-1).min(),4)
    # per window
    pw = port.groupby("window").agg(n=("book_return","size"), book=("book_return","sum"), hold=("coin_return","sum"),
        wn=("wn","first"), mindd=("dd","min")).sort_values("wn")
    out["per_window_sum_returns"] = pw.round(4)
    # gain by side and regime per bar
    g = B.dropna(subset=["gain"])
    out["gain_by_side"] = g.groupby("side").agg(bars=("gain","size"), mean_gain=("gain","mean"), sum_gain=("gain","sum"),
        mean_coin_ret=("ret_next","mean")).round(5)
    # per window per side sum gain (avg per coin)
    pws = g.groupby(["window","side"])["gain"].sum().unstack().fillna(0)
    pws["wn"] = pws.index.str[1:].astype(int)
    out["window_side_gain_sum"] = pws.sort_values("wn").round(3)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"]=coin; t["window"]=w; T.append(t)
    T = pd.concat(T)
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"),
        mean_net=("net_profit_loss_percent","mean"), median_net=("net_profit_loss_percent","median"),
        win=("net_profit_loss_percent", lambda s:(s>0).mean()), sum_net=("net_profit_loss_percent","sum"),
        dur_days=("duration_minutes", lambda s: s.mean()/1440)).round(3)
    # short trades graded by prior 20d return at entry: use bars r20 at entry
    return out
