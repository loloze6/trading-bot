def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c].keys()), key=lambda s: int(s[1:]))
    # book daily returns: per window, mean over coins per day
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        if not frames: continue
        df = pd.concat(frames)
        g = df.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
        g["window"] = w
        chain.append(g.dropna())
    ch = pd.concat(chain, ignore_index=True)
    ch["val"] = (1 + ch["book"]).cumprod()
    ch["peak"] = ch["val"].cummax()
    ch["dd"] = ch["val"] / ch["peak"] - 1
    out["max_dd"] = float(ch["dd"].min())
    yrs = len(ch) / 365
    out["yearly_return"] = float(ch["val"].iloc[-1] ** (1 / yrs) - 1)
    # dd by window: worst within-chain dd reached in each window and window book return
    ww = ch.groupby("window").agg(book_ret=("book", lambda x: (1 + x).prod() - 1),
                                  hold_ret=("hold", lambda x: (1 + x).prod() - 1),
                                  min_dd=("dd", "min"), days=("book", "size"))
    ww = ww.reindex([w for w in wins if w in ww.index])
    out["by_window"] = ww.round(4)
    # per-coin per-window book return contribution
    cw = {}
    for c in coins:
        for w in data["days"][c]:
            d = data["days"][c][w]
            cw[(c, w)] = (1 + d["book_return"].dropna()).prod() - 1
    cws = pd.Series(cw).unstack(0)
    cws = cws.reindex([w for w in wins if w in cws.index])
    out["coin_window_book_ret"] = cws.round(3)
    # cases: forecast rises; compute per entry bar condition and 84-bar outcome
    rows = []
    for c in coins:
        allr = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            n = len(cl)
            for i in range(0, n - 84, 84):
                allr.append(cl[i + 84] / cl[i] - 1)
        drift = np.mean(allr)
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            f = b["forecast"].fillna(0).values
            n = len(cl)
            ret180 = pd.Series(cl).pct_change(180).values
            ret42 = pd.Series(cl).pct_change(42).values
            for start in range(0, n, 84):
                end = min(start + 84, n)
                idx = np.where(f[start:end] >= 2)[0]
                if len(idx) == 0: continue
                i = start + idx[0]
                if i + 84 >= n: continue
                r = cl[i + 84] / cl[i] - 1
                # path: worst point over the 84 bars
                mn = cl[i:i + 85].min() / cl[i] - 1
                r12 = cl[i + 12] / cl[i] - 1
                rows.append(dict(coin=c, window=w, f=f[i], r=r, u=r - drift, mn=mn,
                                 r30=ret180[i], r7=ret42[i], r2d=r12))
    cs = pd.DataFrame(rows)
    out["n_cases"] = len(cs)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_u=g["u"].mean(), t=g["u"].mean() / (g["u"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_min=g["mn"].mean(), share_min_lt_-0.15 if False else 0))
    def summ2(g):
        return pd.Series(dict(n=len(g), mean_u=g["u"].mean(),
                              t=g["u"].mean() / (g["u"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_worst=g["mn"].mean(), sd_u=g["u"].std()))
    cs["r30_q"] = pd.qcut(cs["r30"], 5, labels=False)
    out["by_prior30d_quintile"] = cs.groupby("r30_q").apply(summ2).join(cs.groupby("r30_q")["r30"].mean().rename("r30_mean")).round(4)
    cs["r7_q"] = pd.qcut(cs["r7"], 5, labels=False)
    out["by_prior7d_quintile"] = cs.groupby("r7_q").apply(summ2).join(cs.groupby("r7_q")["r7"].mean().rename("r7_mean")).round(4)
    cs["f_q"] = pd.qcut(cs["f"].rank(method="first"), 5, labels=False)
    out["by_forecast_quintile"] = cs.groupby("f_q").apply(summ2).round(4)
    cs["r2d_q"] = pd.qcut(cs["r2d"], 5, labels=False)
    out["by_next2d_quintile(not known)"] = cs.groupby("r2d_q").apply(summ2).round(4)
    out["by_coin"] = cs.groupby("coin").apply(summ2).round(4)
    # book exposure: mean allocation share of time in market
    al = []
    for c in coins:
        for w, b in data["bars"][c].items():
            al.append(b["postRebalance_current_allocation"].fillna(0).values)
    al = np.concatenate(al)
    out["share_bars_long"] = float((al > 0.01).mean())
    out["mean_alloc_when_long"] = float(al[al > 0.01].mean())
    return out
