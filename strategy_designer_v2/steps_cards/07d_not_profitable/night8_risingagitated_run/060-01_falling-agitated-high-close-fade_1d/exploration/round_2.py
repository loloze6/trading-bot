def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = pd.concat([w["close"].pct_change() for w in ws.values()]).dropna()
        mu = allr.mean()
        for wn, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            rng = h - l
            cl = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            r1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(r1).rolling(20).std().values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            inprof = (b["regime"] == "unknown").values
            n = len(b)
            for i in range(n - 1):
                rows.append(dict(coin=coin, w=wn, i=i, cl=cl[i], inprof=inprof[i],
                                 rngrel=(rng[i] / c[i]) / vol20[i] if vol20[i] > 0 else np.nan,
                                 day_ret=r1[i], pos=pos[i], prev=prev[i],
                                 nxt=c[i + 1] / c[i] - 1, f1=c[i + 1] / c[i] - 1 - mu))
    df = pd.DataFrame(rows)
    df["grp"] = pd.cut(df["cl"], [-0.01, 1/3, 2/3, 1.01], labels=["low", "mid", "top"])
    out = {}
    # where the book's gross gain comes from: by close-location group of the bar held
    p = df[df.pos.abs() > 0].copy()
    p["gain"] = p.pos * p.nxt
    p["timing"] = p.pos * p.f1
    p["opened"] = (p.prev == 0)
    out["gain_by_grp_in_pos"] = p.groupby(["inprof", "grp"], observed=True).agg(
        n=("gain", "size"), gain=("gain", "mean"), timing=("timing", "mean"), abspos=("pos", lambda x: x.abs().mean()))
    out["gain_opened_vs_carried"] = p.groupby("opened").agg(n=("gain", "size"), gain=("gain", "mean"), timing=("timing", "mean"))
    # traded share of position bars by turnover
    p["turn"] = (p.pos - p.prev).abs()
    out["turnover_per_pos_bar"] = p["turn"].mean()
    # strong case: top close x wide range, in and out of profile
    q = df[df.inprof]["rngrel"].quantile([1/3, 2/3]).values
    df["rq"] = pd.cut(df["rngrel"], [-np.inf, q[0], q[1], np.inf], labels=["narrow", "mid", "wide"])
    res = []
    for prof in [True, False]:
        for g in ["low", "mid", "top"]:
            for r in ["narrow", "mid", "wide"]:
                x = df[(df.inprof == prof) & (df.grp == g) & (df.rq == r)]["f1"].dropna()
                res.append(dict(prof=prof, grp=g, rq=r, n=len(x), mean=x.mean(),
                                t=x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan))
    out["grp_x_range"] = pd.DataFrame(res)
    # graded: in profile, cl*rngrel quintiles
    s = df[df.inprof].dropna(subset=["cl", "rngrel", "f1"]).copy()
    s["score"] = s.cl * s.rngrel
    s["sq"] = pd.qcut(s.score, 5, labels=False)
    out["score_quintiles"] = s.groupby("sq").agg(n=("f1", "size"), mean=("f1", "mean"), sd=("f1", "std"))
    # top & wide in profile by window, and per-day pooled t
    tw = df[df.inprof & (df.grp == "top") & (df.rq == "wide")].dropna(subset=["f1"])
    out["topwide_by_window"] = tw.groupby("w")["f1"].agg(["mean", "count"])
    out["topwide_by_coin"] = tw.groupby("coin")["f1"].agg(["mean", "count"])
    return out
