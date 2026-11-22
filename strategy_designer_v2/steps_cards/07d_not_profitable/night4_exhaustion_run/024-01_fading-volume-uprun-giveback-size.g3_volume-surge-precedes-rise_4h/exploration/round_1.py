def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book daily returns: mean across coins per day per window
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["w"] = w; dd["coin"] = c
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"]).dropna()
    eq = (1 + B["book"]).cumprod(); dd_ = eq / eq.cummax() - 1
    B["dd"] = dd_.values
    out["deepest fall of chain"] = float(dd_.min())
    yrs = len(B) / 365
    out["yearly return"] = float(eq.iloc[-1] ** (1 / yrs) - 1)
    # per window book return and worst drawdown inside window
    pw = B.groupby("wn").apply(lambda g: pd.Series({
        "book_ret": (1 + g.book).prod() - 1, "hold_ret": (1 + g.hold).prod() - 1,
        "min_dd_in_w": ((1 + g.book).cumprod() / (1 + g.book).cumprod().cummax() - 1).min(),
        "worst_day": g.book.min()}))
    out["per window"] = pw.round(4)
    # worst 5% book days: what holding did
    q = B.book.quantile(0.05)
    out["worst 5% days: mean book, mean hold, n"] = str((round(B[B.book <= q].book.mean(), 4), round(B[B.book <= q].hold.mean(), 4), int((B.book <= q).sum())))
    # cases: entry from flat into forecast>=2, per coin bar level
    cs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values; op = b.open.values; f = b.forecast.fillna(0).values
            vol = b.volume.values
            n = len(b)
            fwd = np.full(n, np.nan); fwd[:n - 18] = cl[18:] / cl[:n - 18] - 1
            r6 = np.full(n, np.nan); r6[6:] = cl[6:] / cl[:-6] - 1
            r18 = np.full(n, np.nan); r18[18:] = cl[18:] / cl[:-18] - 1
            r1 = cl / op - 1
            # trailing 30-day vol of 4h returns
            lr = pd.Series(cl).pct_change()
            sd = lr.rolling(180, min_periods=60).std().values
            grid = np.arange(n) // 18
            seen = set()
            low = 0.0
            for i in range(1, n):
                if f[i] <= 0: low = 0.0; continue
                if f[i] - low >= 2 and grid[i] not in seen:
                    seen.add(grid[i])
                    cs.append(dict(coin=c, w=w, fwd=fwd[i], r1=r1[i] / sd[i] if sd[i] > 0 else np.nan,
                                   r6=r6[i] / (sd[i] * np.sqrt(6)) if sd[i] > 0 else np.nan,
                                   r18=r18[i] / (sd[i] * np.sqrt(18)) if sd[i] > 0 else np.nan, f=f[i]))
                    low = f[i]
                low = min(low, f[i])
    C = pd.DataFrame(cs).dropna(subset=["fwd"])
    # drift per coin
    drift = {}
    for c in coins:
        v = []
        for w, b in bars[c].items():
            cl = b.close.values; idx = np.arange(0, len(cl) - 18, 18)
            v += list(cl[idx + 18] / cl[idx] - 1)
        drift[c] = np.mean(v)
    C["ex"] = C.fwd - C.coin.map(drift)
    out["cases n, mean ex, t"] = str((len(C), round(C.ex.mean(), 5), round(stats.ttest_1samp(C.ex, 0).statistic, 2)))
    def grp(col, k=5):
        g = C.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], k, labels=False, duplicates="drop")
        r = g.groupby("q").agg(n=("ex", "size"), x_mean=(col, "mean"), ex=("ex", "mean"), sd=("ex", "std"), fwd=("fwd", "mean"))
        r["t"] = r.ex / (r.sd / np.sqrt(r.n)); r["lossshare_fwd<-5%"] = g.groupby("q").fwd.apply(lambda s: (s < -0.05).mean())
        return r.drop(columns="sd").round(4)
    out["by surge bar body (z)"] = grp("r1")
    out["by prior 1d return (z)"] = grp("r6")
    out["by prior 3d return (z)"] = grp("r18")
    out["by forecast"] = grp("f", 4)
    out["by coin"] = C.groupby("coin").ex.agg(["size", "mean", "std"]).round(4)
    return out
