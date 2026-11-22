def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day")[["book_return", "coin_return"]].mean().sort_index().dropna()
        g["win"] = w
        chain.append(g)
    ch = pd.concat(chain)
    eq = (1 + ch["book_return"]).cumprod()
    dd = eq / eq.cummax() - 1
    ch["dd"] = dd.values
    pw = ch.groupby("win").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                               coin=("coin_return", lambda x: (1 + x).prod() - 1),
                               ndays=("book_return", "size"))
    pw["min_dd_in_chain"] = ch.groupby("win")["dd"].min()
    out["per_window"] = pw.reindex(wins).round(4)
    out["max_dd"] = float(dd.min())
    out["yearly"] = float(eq.iloc[-1] ** (365 / len(eq)) - 1)
    rows = []
    for c in coins:
        allret = []
        for w in wins:
            cl = bars[c][w]["close"].values
            idx = np.arange(0, len(cl) - 18, 18)
            allret += list(cl[idx + 18] / cl[idx] - 1)
        drift = np.mean(allret)
        for w in wins:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"].values
            f = b["forecast"].fillna(0).values
            s1 = pd.Series(cl)
            r1 = s1.pct_change()
            ret30 = s1.pct_change(180).values
            ret7 = s1.pct_change(42).values
            volr = (r1.rolling(30).std() / r1.rolling(180).std()).values
            n = len(cl)
            for s in range(0, n, 18):
                e = min(s + 18, n)
                hits = np.where(f[s:e] >= 2)[0]
                if len(hits) == 0:
                    continue
                t = s + hits[0]
                if t + 18 >= n:
                    continue
                fwd = cl[t + 18] / cl[t] - 1
                rows.append(dict(f=f[t], fwd=fwd, un=fwd - drift,
                                 ret30=ret30[t], ret7=ret7[t], volr=volr[t]))
    cs = pd.DataFrame(rows)
    out["n_cases"] = len(cs)

    def grp(col, q=4):
        x = cs.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        g = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("un", "size"),
                               un=("un", "mean"), sd=("un", "std"), fwd=("fwd", "mean"),
                               q10=("fwd", lambda v: v.quantile(0.1)))
        g["t"] = g["un"] / (g["sd"] / np.sqrt(g["n"]))
        return g.drop(columns="sd").round(4)

    out["by_ret30"] = grp("ret30")
    out["by_ret7"] = grp("ret7")
    out["by_volratio"] = grp("volr")
    out["by_forecast"] = grp("f")
    ch2 = ch.copy()
    ch2["bucket"] = pd.qcut(ch2["coin_return"], 5, labels=False)
    out["book_by_coin_day_quintile"] = ch2.groupby("bucket").agg(
        coin=("coin_return", "mean"), book=("book_return", "mean"),
        n=("book_return", "size")).round(5)
    return out
