def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([b["close"].pct_change().dropna() for b in wins.values()])
        mu = allr.mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"]
            b["r1"] = c.pct_change()
            b["fwd"] = c.shift(-1) / c - 1
            b["z"] = b["r1"] / b["r1"].rolling(20).std()
            b["ret20"] = c / c.shift(20) - 1
            b["dd20"] = c / c.rolling(20).max() - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["pos"] = b["postRebalance_current_allocation"]
            b["prev"] = b["previous_allocation"]
            b["gain"] = b["pos"] * b["fwd"]
            b["ex"] = b["fwd"] - mu
            # bars since the last bar with forecast > 0
            f = b["forecast"].fillna(0).values
            since = np.full(len(b), np.nan); last = -999
            for i in range(len(b)):
                if f[i] > 0: last = i
                since[i] = i - last if last >= 0 else np.nan
            b["since"] = since
            b["coin"] = coin; b["win"] = w; b["mu"] = mu
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    tstat = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    held = B[B["pos"] > 0.001].dropna(subset=["fwd"])
    sb = pd.cut(held["since"], [-1, 0, 1, 2, 4, 1000], labels=["0", "1", "2", "3-4", "5+"])
    out["held_by_bars_since_signal"] = held.groupby(sb).agg(n=("gain", "size"), pos=("pos", "mean"),
        gain=("gain", "mean"), ex=("ex", "mean"), t_ex=("ex", tstat))
    out["share_of_pos_bars_after_signal_bar"] = float((held["since"] > 0).mean())
    out["pos_decay"] = B.groupby(pd.cut(B["since"], [-1, 0, 1, 2, 4, 1000]))["pos"].mean()
    F = B[B["z"] < -1].dropna(subset=["fwd", "dd20", "ret20"]).copy()
    F["q_dd20"] = pd.qcut(F["dd20"], 5)
    out["falls_by_dd20"] = F.groupby("q_dd20").agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tstat))
    F["q_ret20"] = pd.qcut(F["ret20"], 5)
    out["falls_by_ret20_q5"] = F.groupby("q_ret20").agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tstat))
    F["dd_in_vol"] = F["dd20"] / (F["vol20"] * np.sqrt(20))
    F["q_ddv"] = pd.qcut(F["dd_in_vol"], 5)
    out["falls_by_dd20_in_vol"] = F.groupby("q_ddv").agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tstat))
    # signal-bar only (forecast>=1) by dd20 tercile
    S = B[B["forecast"] >= 1].dropna(subset=["fwd", "dd20"]).copy()
    S["q"] = pd.qcut(S["dd20"], 3, labels=["deep", "mid", "near_high"])
    out["signal_bars_by_dd20"] = S.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tstat), gain=("gain", "mean"))
    # book drawdown per coin chained
    dd = []
    for coin, ws in data["days"].items():
        r = pd.concat([d["book_return"].dropna() for d in ws.values()])
        v = (1 + r).cumprod(); dd.append((coin, float((v / v.cummax() - 1).min()), float(v.iloc[-1])))
    out["book_dd_per_coin"] = pd.DataFrame(dd, columns=["coin", "maxdd", "final"])
    return out
