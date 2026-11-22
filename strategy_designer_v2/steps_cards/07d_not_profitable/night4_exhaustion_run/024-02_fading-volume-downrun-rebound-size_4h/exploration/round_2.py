def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(bars[coins[0]].keys(), key=lambda w: int(w[1:]))
    # bar-level book gain by 30-day return state of the coin
    rows = []
    for c in coins:
        for w in wins:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change().shift(-1)
            pos = b["postRebalance_current_allocation"].fillna(0)
            ret30 = cl.pct_change(180)
            rows.append(pd.DataFrame(dict(g=pos * r1, pos=pos, ret30=ret30, r=r1, win=w)))
    bb = pd.concat(rows).dropna()
    bb["s30"] = pd.qcut(bb["ret30"], 4, labels=False)
    out["bar_gain_by_ret30_quartile"] = bb.groupby("s30").agg(
        lo=("ret30", "min"), hi=("ret30", "max"), mean_pos=("pos", "mean"),
        gain_per_bar=("g", "mean"), coin_per_bar=("r", "mean"),
        share_in=("pos", lambda x: (x > 0).mean())).round(6)
    out["bar_gain_total_by_ret30_quartile_sum"] = bb.groupby("s30")["g"].sum().round(3)
    # cases: ret30 sign x forecast tier
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
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            ret30 = pd.Series(cl).pct_change(180).values
            n = len(cl)
            for s in range(0, n, 18):
                hits = np.where(f[s:min(s + 18, n)] >= 2)[0]
                if len(hits) == 0: continue
                t = s + hits[0]
                if t + 18 >= n: continue
                fwd = cl[t + 18] / cl[t] - 1
                rows.append(dict(f=f[t], un=fwd - drift, fwd=fwd, up=ret30[t] > 0))
    cs = pd.DataFrame(rows)
    cs["ft"] = pd.cut(cs["f"], [0, 10, 17.7, 20.1], labels=["low", "mid", "high"])
    g = cs.groupby(["up", "ft"]).agg(n=("un", "size"), un=("un", "mean"), sd=("un", "std"), fwd=("fwd", "mean"))
    g["t"] = g["un"] / (g["sd"] / np.sqrt(g["n"]))
    out["cases_ret30sign_x_forecast"] = g.drop(columns="sd").round(4)
    # book daily return split by whether coin's 30-day return was positive at day's start
    drows = []
    for c in coins:
        for w in wins:
            d = days[c][w].copy().reset_index(drop=True)
            d["r30"] = d["close"].pct_change(30).shift(1)
            d["win"] = w
            drows.append(d)
    dd = pd.concat(drows).dropna(subset=["book_return", "r30"])
    dd["up"] = dd["r30"] > 0
    out["book_daily_by_ret30_sign"] = dd.groupby("up").agg(
        n=("book_return", "size"), book=("book_return", "mean"), sd=("book_return", "std"),
        coin=("coin_return", "mean")).round(5)
    return out
