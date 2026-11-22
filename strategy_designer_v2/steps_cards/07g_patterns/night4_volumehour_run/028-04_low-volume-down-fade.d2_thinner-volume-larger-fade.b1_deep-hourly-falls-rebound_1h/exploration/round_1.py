def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    hrs = []
    drift = {}
    for coin, wins in data["bars"].items():
        allf = {3: [], 6: [], 12: [], 24: []}
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            for h in allf:
                f = c.shift(-h) / c - 1
                allf[h].append(f.iloc[::h].dropna())
        drift[coin] = {h: pd.concat(v).mean() for h, v in allf.items()}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            s = r1 / r1.abs().rolling(720, min_periods=120).mean()
            vr = v / v.rolling(720, min_periods=120).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            d = pd.DataFrame({"coin": coin, "w": w, "s": s, "vr": vr, "r1": r1,
                              "hour": ts.dt.hour, "wd": ts.dt.weekday, "pos": np.arange(len(b))})
            for h in (3, 6, 12, 24):
                d[f"f{h}"] = c.shift(-h) / c - 1 - drift[coin][h]
            d["absr_prev24"] = r1.abs().rolling(24).mean() / r1.abs().rolling(720, min_periods=120).mean()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["sb"] = pd.cut(D["s"], [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
    D["vb"] = pd.cut(D["vr"], [0, 1, 2, 4, np.inf])
    def stat(g, col):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    for h in (3, 6):
        G = D[D["pos"] % h == 0]
        out[f"fwd{h}_by_move_vol"] = G.groupby(["sb", "vb"], observed=True).apply(lambda g: stat(g, f"f{h}")).round(2)
    G = D[D["pos"] % 24 == 0]
    out["fwd24_by_move"] = G.groupby("sb", observed=True).apply(lambda g: stat(g, "f24")).round(2)
    G1 = D.copy()
    G1["r1n"] = D.groupby(["coin", "w"])["r1"].shift(-1)
    out["next1h_by_hour"] = G1.groupby("hour").apply(lambda g: stat(g, "r1n")).round(2)
    out["next1h_by_weekday"] = G1.groupby("wd").apply(lambda g: stat(g, "r1n")).round(2)
    G = D[D["pos"] % 6 == 0].copy()
    G["volq"] = pd.qcut(G["absr_prev24"], 5, labels=False, duplicates="drop")
    G["sign24"] = np.sign(D.loc[G.index, "s"])
    out["fwd6_by_recentvol_quint"] = G.groupby("volq").apply(lambda g: stat(g, "f6")).round(2)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(d.assign(coin=coin, w=w))
    B = pd.concat(br)
    out["book_daily_by_coin"] = B.groupby("coin").apply(lambda g: pd.Series({
        "mean_bp": g.book_return.mean() * 1e4, "coin_bp": g.coin_return.mean() * 1e4,
        "corr": g.book_return.corr(g.coin_return)})).round(3)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["ef_b"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entryforecast"] = T.groupby("ef_b", observed=True).agg(
        n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur=("duration_minutes", "mean")).round(3)
    return out
