def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; dayrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            b["prevret"] = b["dayret"].shift(1)
            b["r3"] = b["close"] / b["close"].shift(3) - 1
            b["r60"] = b["close"] / b["close"].shift(60) - 1
            b["vol20"] = b["dayret"].rolling(20).std()
            b["vol60"] = b["dayret"].rolling(60).std()
            b["vr"] = b["vol20"] / b["vol60"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["fc"] = b["forecast"]
            b["prevfc"] = b["fc"].shift(1)
            b["gain"] = b["pos"] * b["ret1"]
            b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            dayrows.append(d[["day","win","coin","book_return","coin_return"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["ret1"].mean()
    B["ex1"] = B["ret1"] - B["coin"].map(mu)
    D = pd.concat(dayrows, ignore_index=True)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index().dropna()
    bk["wi"] = bk["win"].str[1:].astype(int); bk = bk.sort_values(["wi","day"]).reset_index(drop=True)
    eq = (1 + bk["book_return"]).cumprod(); bk["dd"] = eq / eq.cummax() - 1
    # worst 5% book days: what was held the bar before
    B["gainday"] = B["gain"]
    worst = bk.nsmallest(40, "book_return")
    out["worst40_book_days"] = pd.Series({"mean book": worst.book_return.mean(), "mean coin": worst.coin_return.mean(),
        "share of total loss days sum": worst.book_return.sum() / bk.loc[bk.book_return<0,"book_return"].sum()})
    S = B[B.fc > 0].dropna(subset=["ex1"]).copy()
    # consecutive falls: prev day also a fall (signal yesterday)
    S["prev_sig"] = np.where(S["prevfc"] > 0, "prev fall day", "first fall day")
    out["by_prev_sig"] = S.groupby("prev_sig").agg(ex1=("ex1","mean"), gain=("gain","mean"), pos=("pos","mean"), n=("ex1","size"),
        sd=("ex1","std"))
    S["r3q"] = pd.qcut(S["r3"], 5)
    out["sig_by_r3"] = S.groupby("r3q").agg(ex1=("ex1","mean"), gain=("gain","mean"), n=("ex1","size"))
    # strong signals only
    T = S[S.fc >= 11.7].copy()
    T["vq"] = pd.qcut(T["vol20"], 3)
    out["strong_by_vol20"] = T.groupby("vq").agg(ex1=("ex1","mean"), gain=("gain","mean"), pos=("pos","mean"), n=("ex1","size"), sd=("ex1","std"))
    T["vrq"] = pd.qcut(T["vr"], 3)
    out["strong_by_vr"] = T.groupby("vrq").agg(ex1=("ex1","mean"), gain=("gain","mean"), pos=("pos","mean"), n=("ex1","size"))
    # condition alone: high vol20 without signal
    N = B[(B.fc <= 0)].dropna(subset=["ex1","vol20"]).copy()
    cuts = pd.qcut(S["vol20"].dropna(), 3, retbins=True)[1]
    cuts[0] = 0; cuts[-1] = 1
    N["vq"] = pd.cut(N["vol20"], cuts); S["vq"] = pd.cut(S["vol20"], cuts)
    out["vol_no_signal"] = N.groupby("vq").agg(ex1=("ex1","mean"), n=("ex1","size"))
    out["vol_signal"] = S.groupby("vq").agg(ex1=("ex1","mean"), gain=("gain","mean"), n=("ex1","size"))
    # t for top vol tercile signal
    top = S[S.vq == S.vq.cat.categories[-1]]
    dm = top.groupby("day")["ex1"].mean()
    out["top_vol_t"] = pd.Series({"mean": dm.mean(), "t_days": dm.mean()/(dm.std()/np.sqrt(len(dm))), "days": len(dm)})
    # 60-day trend profile
    S2 = S.dropna(subset=["r60"]).copy()
    S2["trend"] = pd.cut(S2["r60"], [-5, -0.1, 0.1, 50], labels=["falling","choppy","rising"])
    out["sig_by_trend60"] = S2.groupby("trend").agg(ex1=("ex1","mean"), gain=("gain","mean"), n=("ex1","size"))
    N2 = N.dropna(subset=["r60"]).copy()
    N2["trend"] = pd.cut(N2["r60"], [-5, -0.1, 0.1, 50], labels=["falling","choppy","rising"])
    out["nosig_by_trend60"] = N2.groupby("trend").agg(ex1=("ex1","mean"), n=("ex1","size"))
    # drawdown periods: active gain within book dd < -15%
    bk["indd"] = bk["dd"] < -0.15
    mp = bk.set_index(["win","day"])["indd"]
    S["indd"] = [mp.get((w, d), np.nan) for w, d in zip(S["win"], S["day"])]
    out["sig_in_dd"] = S.groupby("indd").agg(ex1=("ex1","mean"), gain=("gain","mean"), vol20=("vol20","mean"), pos=("pos","mean"), n=("ex1","size"))
    # sizing: gain per pos vs fc bucket strong vs weak
    S["fcb"] = pd.cut(S["fc"], [0, 5.44, 11.7, 20.1])
    out["gain_by_fcb"] = S.groupby("fcb").agg(gain=("gain","mean"), gainsum=("gain","sum"), ex1=("ex1","mean"), sd_gain=("gain","std"), n=("gain","size"))
    return out
