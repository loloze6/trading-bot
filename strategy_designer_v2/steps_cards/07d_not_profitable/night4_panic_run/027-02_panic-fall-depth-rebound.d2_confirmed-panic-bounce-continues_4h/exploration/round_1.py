import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # book daily returns: per window, per day, mean over coins
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    v = (1 + B["book_return"]).cumprod()
    peak = v.cummax(); dd = v / peak - 1
    B["dd"] = dd.values
    trough = dd.idxmin()
    pk = v.loc[:trough].idxmax()
    out["maxdd"] = float(dd.min())
    out["dd_peak_trough_window"] = f"peak w{pk[0]} trough w{trough[0]}"
    # top drawdown episodes per window (min dd within each window)
    out["dd_min_by_window"] = B.groupby(level=0)["dd"].min().round(3)
    # per window book and coin total return
    pw = B.groupby(level=0).agg(book=("book_return", lambda x: (1+x).prod()-1),
                               coin=("coin_return", lambda x: (1+x).prod()-1))
    out["window_returns"] = pw.round(3)
    # per coin contribution between peak and trough
    seg = D.set_index(["wn", "day"]).sort_index()
    seg = seg.loc[pk:trough]
    out["dd_coin_sum_returns"] = seg.groupby("coin")[["book_return", "coin_return"]].sum().round(3)
    # trades by side
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T)
    T["fbin"] = pd.cut(T["entry_forecast"], [-21, -5, -2, 0, 2, 5, 21])
    out["trades_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum", "min"]).round(3)
    out["trades_fbin"] = T.groupby("fbin")["net_profit_loss_percent"].agg(["count", "mean", "sum"]).round(3)
    out["trades_coin_side"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["count", "mean", "sum"]).round(2)
    # allocation exposure: share of bars long/short, mean abs allocation
    al = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"]
            r = b["close"].shift(-1) / b["close"] - 1
            # prior 30-day return at bar (180 bars)
            p30 = b["close"] / b["close"].shift(180) - 1
            vol = b["close"].pct_change().rolling(180).std()
            al.append(pd.DataFrame({"a": a, "g": a * r, "p30": p30, "vol": vol, "coin": c}))
    A = pd.concat(al).dropna()
    A["side"] = np.sign(A["a"])
    out["exposure"] = A.groupby("side").agg(n=("a", "size"), mean_abs=("a", lambda x: x.abs().mean()), gain_sum=("g", "sum"), gain_mean=("g", "mean"))
    inpos = A[A["side"] != 0].copy()
    inpos["p30q"] = pd.qcut(inpos["p30"], 5, labels=False)
    inpos["volq"] = pd.qcut(inpos["vol"], 5, labels=False)
    out["gain_by_prior30d_quint"] = inpos.groupby(["p30q", "side"])["g"].agg(["count", "mean", "sum"])
    out["gain_by_vol_quint"] = inpos.groupby(["volq", "side"])["g"].agg(["count", "mean", "sum"])
    return out
