def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    dayrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            rng = (b["high"] - b["low"]) / b["close"]
            b["rngmult"] = rng / rng.shift(1).rolling(14).mean()
            b["r20"] = b["close"] / b["close"].shift(20) - 1
            b["r5"] = b["close"] / b["close"].shift(5) - 1
            b["vol20"] = b["dayret"].rolling(20).std()
            b["pos"] = b["postRebalance_current_allocation"]
            b["fc"] = b["forecast"]
            b["gain"] = b["pos"] * b["ret1"]
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","year","ret1","dayret","rngmult","r20","r5","vol20","pos","fc","gain"]])
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dayrows.append(d[["day","win","coin","book_return","coin_return"]])
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(dayrows, ignore_index=True)
    mu = B.groupby("coin")["ret1"].mean()
    B["ex1"] = B["ret1"] - B["coin"].map(mu)
    # holding persistence
    out["pos_state"] = pd.Series({
        "share pos>0": (B.pos > 0.001).mean(),
        "share fc>0": (B.fc > 0).mean(),
        "share pos>0 & fc==0": ((B.pos > 0.001) & (B.fc <= 0)).mean(),
        "mean pos when fc>0": B.loc[B.fc > 0, "pos"].mean(),
        "mean pos when fc==0 & pos>0": B.loc[(B.fc <= 0) & (B.pos > 0.001), "pos"].mean(),
        "gain mean fc>0": B.loc[B.fc > 0, "gain"].mean(),
        "gain mean fc==0 pos>0": B.loc[(B.fc <= 0) & (B.pos > 0.001), "gain"].mean(),
        "ex1 mean fc>0": B.loc[B.fc > 0, "ex1"].mean(),
        "ex1 mean fc==0 pos>0": B.loc[(B.fc <= 0) & (B.pos > 0.001), "ex1"].mean(),
    })
    # book daily: mean across coins per (win, day)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index().dropna()
    wo = {f"w{i}": i for i in range(1, 40)}
    bk["wi"] = bk["win"].map(wo); bk = bk.sort_values(["wi","day"]).reset_index(drop=True)
    eq = (1 + bk["book_return"]).cumprod(); dd = eq / eq.cummax() - 1
    ceq = (1 + bk["coin_return"]).cumprod(); cdd = ceq / ceq.cummax() - 1
    bk["dd"] = dd
    out["book_summary"] = pd.Series({"maxdd": dd.min(), "hold maxdd": cdd.min(),
        "yearly": eq.iloc[-1] ** (365 / len(bk)) - 1, "hold yearly": ceq.iloc[-1] ** (365/len(bk)) - 1,
        "days": len(bk)})
    out["book_by_window"] = bk.groupby("win").agg(book_sum=("book_return","sum"), coin_sum=("coin_return","sum"),
        min_dd=("dd","min"), n=("book_return","size")).sort_values("min_dd")
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("year").agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"), n=("book_return","size"))
    # correlation of book with coin daily
    out["book_coin_corr"] = float(bk[["book_return","coin_return"]].corr().iloc[0,1])
    # worst book days vs coin
    q = bk["coin_return"].quantile([0.1, 0.9])
    bk["cstate"] = pd.cut(bk["coin_return"], [-1, q.iloc[0], q.iloc[1], 5], labels=["coin worst10","mid","coin best10"])
    out["book_by_coin_day"] = bk.groupby("cstate")["book_return"].agg(["mean","sum","count"])
    # gain on active bars by r20 (trend) and by rngmult, and by depth
    A = B[B.pos > 0.001].dropna(subset=["ret1"]).copy()
    A["r20q"] = pd.qcut(A["r20"], 5)
    out["active_by_r20"] = A.groupby("r20q").agg(gain=("gain","mean"), ex1=("ex1","mean"), n=("gain","size"), pos=("pos","mean"))
    F = B[B.fc > 0].dropna(subset=["ret1"]).copy()
    F["fq"] = pd.qcut(F["fc"], 5, duplicates="drop")
    out["signal_by_fc"] = F.groupby("fq").agg(ex1=("ex1","mean"), ret1=("ret1","mean"), n=("ex1","size"), pos=("pos","mean"))
    F["r20q"] = pd.qcut(F["r20"], 5)
    out["signal_by_r20"] = F.groupby("r20q").agg(ex1=("ex1","mean"), ret1=("ret1","mean"), n=("ex1","size"))
    F["vq"] = pd.qcut(F["vol20"], 3)
    out["signal_by_vol20"] = F.groupby("vq").agg(ex1=("ex1","mean"), ret1=("ret1","mean"), gain=("gain","mean"), n=("ex1","size"))
    # non-signal bars in same r20 bins (condition alone)
    N = B[(B.fc <= 0)].dropna(subset=["ret1","r20"]).copy()
    N["r20q"] = pd.cut(N["r20"], F["r20q"].cat.categories)
    out["nosignal_by_r20"] = N.groupby("r20q").agg(ex1=("ex1","mean"), n=("ex1","size"))
    out["by_coin"] = B.groupby("coin").agg(gain=("gain","mean"), sig_ex1=("ex1", lambda s: s[B.loc[s.index,"fc"]>0].mean()))
    return out
