def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hourly = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < 220: continue
            lo12 = lo.shift(1).rolling(12).min(); hi12 = hi.shift(1).rolling(12).max()
            span = hi12 - lo12
            mbr = ((hi - lo) / c).shift(2).rolling(180).mean()
            width = (span / c.shift(1)) / mbr
            mom180 = c / c.shift(180) - 1
            mom36 = c / c.shift(36) - 1
            r1 = c.pct_change()
            vol = r1.rolling(180).std()
            z1 = r1 / vol.shift(1)
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "width": width, "mom180": mom180, "mom36": mom36,
                               "z1": z1, "vol": vol, "fwd": fwd, "fwd6": fwd6,
                               "dn": c < lo12, "up": c > hi12, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "r1n": r1.shift(-1)})
            df["pos"] = np.arange(n)
            hourly.append(df[["coin", "hour", "wd", "r1n"]])
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0)].dropna(subset=["ex", "width", "mom180"])
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "absmean": g["fwd"].abs().mean()})
    out = {}
    # brief claim: width quintile vs absolute forward move
    G["wq"] = G.groupby("coin")["width"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["width_q_all"] = G.groupby("wq").apply(summ)
    # breakdowns / breakouts by mom sign and width tercile
    G["wt"] = G.groupby("coin")["width"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    G["momsign"] = np.sign(G["mom180"])
    out["down_break"] = G[G.dn].groupby(["momsign", "wt"]).apply(summ)
    out["up_break"] = G[G.up].groupby(["momsign", "wt"]).apply(summ)
    # after large 4h bar moves
    G["zb"] = pd.cut(G["z1"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    out["after_z1"] = G.groupby("zb").apply(summ)
    # 6-day momentum quintile
    G["m36q"] = G.groupby("coin")["mom36"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["mom6d_q"] = G.groupby("m36q").apply(summ)
    G["vq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["volq"] = G.groupby("vq").apply(summ)
    Hh = pd.concat(hourly).dropna()
    out["hour_next4h"] = Hh.groupby("hour")["r1n"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["weekday_next4h"] = Hh.groupby("wd")["r1n"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()], ignore_index=True)
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    return out
