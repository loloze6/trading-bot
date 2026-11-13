import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # bar-level: book return per bar vs allocation, forecast, vol, run-up size, days in trade
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["coin"] = c; b["win"] = w
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            v = b["postRebalance_total_value"]
            b["book1"] = v.shift(-1) / v - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            lr = np.log(b["close"]).diff()
            b["vol20"] = lr.rolling(20).std()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            inpos = (b["alloc"].abs() > 1e-6)
            grp = (inpos != inpos.shift()).cumsum()
            b["age"] = inpos.groupby(grp).cumcount()
            b["inpos"] = inpos
            b["dd"] = v / v.cummax() - 1
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["year"] = pd.to_datetime(B["timestamp"]).dt.year
    P = B[B.inpos].dropna(subset=["book1"])
    out["alloc_desc_inpos"] = P["alloc"].describe()
    P = P.copy()
    P["vq"] = P.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["low", "mid", "high"]))
    g = P.groupby("vq").book1
    out["inpos_by_vol"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "sd": g.std(),
        "sharpe_ann": g.mean() / g.std() * np.sqrt(365), "worst": g.min(), "alloc": P.groupby("vq").alloc.mean()})
    P["ab"] = pd.cut(P.age, [-1, 2, 5, 10, 20, 40, 10000])
    g = P.groupby("ab").book1
    out["inpos_by_age"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "sd": g.std(),
        "t": g.mean() / (g.std() / np.sqrt(g.size())), "coin_r": P.groupby("ab").r1.mean()})
    P["r20b"] = pd.qcut(P.ret20, 4)
    g = P.groupby("r20b").book1
    out["inpos_by_ret20"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "sd": g.std(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    P["r60b"] = pd.qcut(P.ret60, 4)
    g = P.groupby("r60b").book1
    out["inpos_by_ret60"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "sd": g.std(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    # losses: share of total loss on worst days, and where
    neg = P[P.book1 < 0]
    out["neg_day_sum_by_vol"] = neg.groupby("vq").book1.sum() / neg.book1.sum()
    out["neg_day_sum_by_age"] = neg.groupby("ab").book1.sum() / neg.book1.sum()
    # trades: MFE giveback
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t) == 0: continue
            b = data["bars"][c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            for _, x in t.iterrows():
                et, xt = pd.to_datetime(x.entry_time), pd.to_datetime(x.exit_time)
                seg = b[(b.ts >= et) & (b.ts <= xt)]
                if len(seg) == 0: continue
                mfe = seg.high.max() / x.entry_price - 1
                mae = seg.low.min() / x.entry_price - 1
                tr.append({"coin": c, "gross": x.profit_loss_percent, "mfe": mfe * 100, "mae": mae * 100,
                           "days": x.duration_minutes / 1440, "ef": x.entry_forecast,
                           "xf": x.exit_forecast, "side": x.side})
    T = pd.DataFrame(tr)
    T["giveback"] = T.mfe - T.gross
    out["trade_side"] = T.groupby("side").gross.agg(["size", "mean"])
    T["db"] = pd.cut(T.days, [0, 2, 5, 10, 20, 1000])
    out["trade_excursion_by_dur"] = T.groupby("db")[["gross", "mfe", "mae", "giveback"]].mean()
    out["exit_fc_zero_share"] = float((T.xf < 0.5).mean())
    T["xb"] = pd.cut(T.xf, [-0.01, 0.5, 5, 15, 20.01])
    out["trade_by_exit_fc"] = T.groupby("xb").agg(n=("gross", "size"), gross=("gross", "mean"),
                                                   give=("giveback", "mean"))
    # concentration
    s = T.gross.sort_values(ascending=False)
    out["top10_share_of_sum"] = float(s.head(10).sum() / s.sum())
    out["sum_without_top10"] = float(s.iloc[10:].sum())
    # non-overlapping fwd 5 by vol tercile within fc>=10
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f5 = b["close"].shift(-5) / b["close"] - 1
            lr = np.log(b["close"]).diff()
            vol = lr.rolling(20).std()
            r20 = b["close"] / b["close"].shift(20) - 1
            idx = np.arange(0, len(b), 5)
            rows.append(pd.DataFrame({"fc": b.forecast.values[idx], "f5": f5.values[idx],
                                      "vol": vol.values[idx], "r20": r20.values[idx], "coin": c}))
    S = pd.concat(rows).dropna(subset=["f5"])
    S["ex"] = S.f5 - S.groupby("coin").f5.transform("mean")
    S["vq"] = S.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=["low", "mid", "high"]))
    A = S[S.fc >= 10]
    g = A.groupby("vq").ex
    out["fc10_fwd5_by_vol"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "sd": g.std(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    A = A.copy(); A["r20b"] = pd.qcut(A.r20, 3)
    g = A.groupby("r20b").ex
    out["fc10_fwd5_by_r20"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    return out
