def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            absm = r1.abs().rolling(180, min_periods=45).mean()
            past18 = c / c.shift(18) - 1
            past6 = c / c.shift(6) - 1
            fwd = c.shift(-H) / c - 1
            nxt = c.shift(-1) / c - 1
            # streaks
            sign = np.sign(r1.fillna(0)).values
            slen = np.zeros(len(b)); sret = np.zeros(len(b))
            vfade = np.full(len(b), np.nan)
            start = 0
            for i in range(1, len(b)):
                if sign[i] != 0 and sign[i] == sign[i-1]:
                    slen[i] = slen[i-1] + 1
                elif sign[i] != 0:
                    slen[i] = 1; start = i
                else:
                    slen[i] = 0; start = i
                if slen[i] >= 2:
                    vv = v.values[start:i+1]
                    vfade[i] = np.polyfit(np.arange(len(vv)), vv, 1)[0] / (vv.mean() + 1e-12)
                sret[i] = c.values[i] / c.values[start-1] - 1 if start >= 1 else np.nan
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "fwd": fwd, "nxt": nxt, "p18": past18 / (absm * np.sqrt(18)), "p6": past6 / (absm * np.sqrt(6)),
                "vol": absm, "slen": slen * sign, "sret_u": sret / absm, "vfade": vfade,
                "hour": pd.to_datetime(b["timestamp"]).dt.hour, "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"], "fc": b["forecast"]})
            hourly.append(df[["coin", "hour", "nxt", "wd"]])
            recs.append(df[df.pos % H == 0])
        g = pd.concat(recs)
        g["exc"] = g["fwd"] - g["fwd"].mean()
        g["volq"] = pd.qcut(g["vol"], 5, labels=False, duplicates="drop")
        rows.append(g)
    G = pd.concat(rows).dropna(subset=["exc"])
    out = {}
    def summ(gr):
        x = gr["exc"]; n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    G["p18q"] = pd.qcut(G["p18"], 10, labels=False, duplicates="drop")
    out["fwd18 exc by past18 z decile"] = G.groupby("p18q").apply(summ)
    G["p6q"] = pd.qcut(G["p6"], 10, labels=False, duplicates="drop")
    out["fwd18 exc by past6 z decile"] = G.groupby("p6q").apply(summ)
    out["fwd18 exc by vol quintile (per coin)"] = G.groupby("volq").apply(summ)
    G["sl"] = G["slen"].clip(-5, 5)
    out["fwd18 exc by signed streak len"] = G.groupby("sl").apply(summ)
    S = G[G["slen"].abs() >= 2].copy()
    S["side"] = np.where(S["slen"] > 0, "up", "down")
    S["fade"] = np.where(S["vfade"] < 0, "fading", "rising")
    S["mag"] = S.groupby("side")["sret_u"].transform(lambda s: pd.qcut(s.abs(), 3, labels=False, duplicates="drop"))
    out["streak side x volume x size tercile"] = S.groupby(["side", "fade", "mag"]).apply(summ)
    out["fwd18 exc by coin x p18 sign"] = G.assign(ps=np.sign(G.p18)).groupby(["coin", "ps"]).apply(summ)
    Hh = pd.concat(hourly).dropna(subset=["nxt"])
    Hh["exc"] = Hh["nxt"] - Hh.groupby("coin")["nxt"].transform("mean")
    out["next 4h exc by hour"] = Hh.groupby("hour").apply(summ)
    out["next 4h exc by weekday"] = Hh.groupby("wd").apply(summ)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    D["inpos"] = D["book_return"] != 0
    out["book daily by year"] = D.assign(y=pd.to_datetime(D["day"]).dt.year).groupby("y").agg(
        book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    q = D["book_return"].quantile([0.01, 0.99])
    big = D[(D.book_return <= q.iloc[0]) | (D.book_return >= q.iloc[1])]
    out["book tails: coin return same day"] = big.assign(s=np.sign(big.book_return)).groupby("s").agg(
        n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        mean=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()),
        dur_h=("duration_minutes", lambda s: s.mean() / 60))
    return out
