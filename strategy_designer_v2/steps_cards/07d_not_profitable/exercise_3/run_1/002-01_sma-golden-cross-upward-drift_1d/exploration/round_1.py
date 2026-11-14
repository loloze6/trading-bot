import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # book daily, pooled across coins by (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P = P.dropna()
    def sh(x): return x.mean() / x.std() * np.sqrt(365)
    def mdd(x):
        v = (1 + x).cumprod(); return (v / v.cummax() - 1).min()
    out["book_vs_hold"] = pd.DataFrame({
        "sharpe": [sh(P.book_return), sh(P.coin_return)],
        "mean": [P.book_return.mean(), P.coin_return.mean()],
        "maxdd": [mdd(P.book_return), mdd(P.coin_return)]}, index=["book", "hold"])
    out["by_window"] = P.groupby("wn").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                                           hold=("coin_return", lambda x: (1 + x).prod() - 1),
                                           n=("book_return", "size"))
    # per coin book
    out["by_coin"] = D.dropna().groupby("coin").agg(book_sh=("book_return", sh), hold_sh=("coin_return", sh),
                                                    book_m=("book_return", "mean"), hold_m=("coin_return", "mean"))
    # non-overlapping 10-bar blocks with conditions
    B = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            raw = b.get("debug_info.components.sma_cross.last_history_value")
            r20 = cl / cl.shift(20) - 1
            r5 = cl / cl.shift(5) - 1
            vol = cl.pct_change().rolling(20).std()
            dspread = raw - raw.shift(10) if raw is not None else np.nan
            for i in range(0, len(b) - 10, 10):
                B.append(dict(coin=c, wn=int(w[1:]), f=b.forecast[i], raw=raw[i] if raw is not None else np.nan,
                              r20=r20[i], r5=r5[i], vol=vol[i], ds=dspread[i] if raw is not None else np.nan,
                              fwd=cl[i + 10] / cl[i] - 1))
    B = pd.DataFrame(B)
    B["ex"] = B.fwd - B.groupby("coin").fwd.transform("mean")
    on = B[B.f > 0].copy()
    on["fb"] = pd.cut(on.f, [0, 5, 10, 15, 20.01])
    out["fwd_by_forecast"] = on.groupby("fb", observed=True).ex.agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["flat_ex"] = pd.Series({"mean": B[B.f == 0].ex.mean(), "n": (B.f == 0).sum()})
    for col in ["raw", "r20", "r5", "vol", "ds"]:
        q = on.dropna(subset=[col])
        q["qb"] = pd.qcut(q[col], 4, labels=False, duplicates="drop")
        out[f"on_by_{col}_q"] = q.groupby("qb").agg(lo=(col, "min"), hi=(col, "max"), ex=("ex", "mean"),
                                                   fwd=("fwd", "mean"), n=("ex", "size"),
                                                   t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # trades
    T = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.Series({"n": len(T), "mean_gross": T.profit_loss_percent.mean(),
                               "mean_net": T.net_profit_loss_percent.mean(),
                               "mean_comm": T.total_commission.mean(),
                               "dur_days_med": T.duration_minutes.median() / 1440})
    return out
