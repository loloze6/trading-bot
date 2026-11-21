import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    H = 5
    rows = []
    for coin, wins in bars.items():
        allg = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["forecast"].astype(float),
                "ret_past5": c / c.shift(5) - 1,
                "ret_past20": c / c.shift(20) - 1,
                "vol20": r1.rolling(20).std(),
                "pos20": (c - b["low"].rolling(20).min()) / (b["high"].rolling(20).max() - b["low"].rolling(20).min()),
                "brk20": c / b["high"].shift(1).rolling(20).max() - 1,
                "brk20lo": c / b["low"].shift(1).rolling(20).min() - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd5": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "pos": b["postRebalance_current_allocation"].astype(float),
            })
            f["grid5"] = (np.arange(len(f)) % H == 0)
            f["grid10"] = (np.arange(len(f)) % 10 == 0)
            allg.append(f)
        df = pd.concat(allg, ignore_index=True)
        g = df[df.grid5 & df.fwd5.notna()]
        df["ex5"] = df.fwd5 - g.fwd5.mean()
        g10 = df[df.grid10 & df.fwd10.notna()]
        df["ex10"] = df.fwd10 - g10.fwd10.mean()
        df["ex1"] = df.fwd1 - df.fwd1.mean()
        df["usual5"] = g.fwd5.std()
        rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.grid5 & D.ex5.notna()].copy()
    G["str5"] = G.ex5 / G.usual5

    out = {}
    def bucket(col, q=5, target="ex5", frame=None):
        fr = (G if frame is None else frame).dropna(subset=[col, target]).copy()
        fr["b"] = fr.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = fr.groupby("b")[target].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        sl = stats.linregress(fr.groupby("coin")[col].transform(lambda s: (s - s.mean()) / s.std()), fr[target])
        t["slope_per_z"] = sl.slope; t["slope_t"] = sl.slope / sl.stderr
        return t.round(4)

    nz = G[G.fc != 0]
    out["fc_nonzero_quint_ex5"] = bucket("fc", 5, frame=nz)
    out["zero_vs_nonzero_ex5"] = G.groupby(G.fc != 0)["ex5"].agg(["mean", "count"]).round(4)
    out["past5_quint_ex5"] = bucket("ret_past5")
    out["past20_quint_ex5"] = bucket("ret_past20")
    out["vol20_quint_ex5"] = bucket("vol20")
    out["pos20_quint_ex5"] = bucket("pos20")
    out["brk20_quint_ex5"] = bucket("brk20")
    G10 = D[D.grid10 & D.ex10.notna()]
    out["past20_quint_ex10"] = bucket("ret_past20", target="ex10", frame=G10)
    out["brk20lo_quint_ex5"] = bucket("brk20lo")
    wd = D.dropna(subset=["ex1"]).groupby("wd")["ex1"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_ex1"] = wd.round(5)
    out["by_coin_ex5_short_corr"] = G.groupby("coin").apply(lambda x: pd.Series({
        "n_nz": (x.fc != 0).sum(), "corr_fc_ex5": x[["fc", "ex5"]].corr().iloc[0, 1],
        "mean_pos": x.pos.mean()})).round(4)
    # book
    br = []
    for coin, wins in days.items():
        for w, d in wins.items():
            br.append(d.assign(coin=coin, win=w))
    B = pd.concat(br, ignore_index=True)
    B["day"] = pd.to_datetime(B["day"])
    daily = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_daily"] = pd.Series({"mean_book": daily.book_return.mean(), "mean_coin": daily.coin_return.mean(),
                                   "corr": daily.corr().iloc[0, 1], "n_days": len(daily)}).round(5)
    out["book_by_window_mean"] = daily.groupby("win")[["book_return", "coin_return"]].mean().round(5).T
    T = pd.concat([t.assign(coin=c) for c, ws in trades.items() for w, t in ws.items() if len(t)], ignore_index=True)
    out["trades"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["mean", "count"]).round(3)
    return out
