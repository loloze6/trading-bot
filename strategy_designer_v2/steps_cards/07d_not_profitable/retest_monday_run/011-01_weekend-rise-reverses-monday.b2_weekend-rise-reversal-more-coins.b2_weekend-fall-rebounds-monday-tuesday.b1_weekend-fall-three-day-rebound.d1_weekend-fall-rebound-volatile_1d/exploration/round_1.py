def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns, per window, mean over coins
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna().reset_index().sort_values(["wn", "day"])
    val = (1 + B["book"]).cumprod().values
    peak = np.maximum.accumulate(val)
    dd = val / peak - 1
    B["dd"] = dd
    i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(val[:i_tr + 1]))
    out["deepest fall"] = pd.Series({"depth": dd[i_tr], "days peak->trough": i_tr - i_pk,
                                     "windows from": B["wn"].iloc[i_pk], "windows to": B["wn"].iloc[i_tr],
                                     "hold return in fall": (1 + B["hold"].iloc[i_pk:i_tr + 1]).prod() - 1})
    W = B.groupby("wn").apply(lambda g: pd.Series({"book": (1 + g.book).prod() - 1, "hold": (1 + g.hold).prod() - 1,
                                                    "book_maxdd": ((1 + g.book).cumprod() / (1 + g.book).cumprod().cummax() - 1).min(),
                                                    "days": len(g)}))
    out["per window"] = W
    # ---- cases
    cs = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 3, 3)
            allr += list(cl[idx + 3] / cl[idx] - 1)
        mu = np.mean(allr)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]
            r1 = cl.pct_change()
            f3 = cl.shift(-3) / cl - 1
            r20 = cl / cl.shift(20) - 1
            r60 = cl / cl.shift(60) - 1
            sma50 = cl / cl.rolling(50).mean() - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            r2 = cl / cl.shift(2) - 1
            alloc = b["postRebalance_current_allocation"]
            sun = (ts.dt.dayofweek == 6)
            for i in np.where(sun & f3.notna())[0]:
                cs.append(dict(coin=c, wn=int(w[1:]), fc=b["forecast"].iloc[i], r1=r1.iloc[i], r2=r2.iloc[i], f3=f3.iloc[i],
                               ex=f3.iloc[i] - mu, r20=r20.iloc[i], r60=r60.iloc[i], sma=sma50.iloc[i],
                               vr=vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan, alloc=alloc.iloc[i]))
    C = pd.DataFrame(cs)
    S = C[C.fc > 0].copy()
    S["pnl"] = S.alloc * S.f3
    def g(df, col, q=3):
        df = df.dropna(subset=[col]).copy()
        df["b"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        return df.groupby("b").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"), f3=("f3", "mean"), ex=("ex", "mean"),
                                   t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))), pnl=("pnl", "mean"),
                                   p5=("f3", lambda x: x.quantile(0.05)), worst=("f3", "min"))
    out["signal cases by forecast"] = g(S, "fc")
    out["signal by prior 20d ret"] = g(S, "r20")
    out["signal by price vs 50d mean"] = g(S, "sma")
    out["signal by 20/60 vol ratio"] = g(S, "vr")
    out["signal by Sunday ret"] = g(S, "r1")
    # condition without signal: Sundays not falling
    N = C[C.fc <= 0].copy(); N["pnl"] = 0
    out["no-signal Sundays by price vs 50d"] = g(N, "sma")
    out["no-signal Sundays by prior 20d"] = g(N, "r20")
    # contributions of signal pnl by window
    out["signal pnl by window"] = S.groupby("wn").agg(n=("pnl", "size"), pnl_sum=("pnl", "sum"), f3=("f3", "mean"), r20=("r20", "mean"))
    out["alloc summary"] = S["alloc"].describe()
    return out
