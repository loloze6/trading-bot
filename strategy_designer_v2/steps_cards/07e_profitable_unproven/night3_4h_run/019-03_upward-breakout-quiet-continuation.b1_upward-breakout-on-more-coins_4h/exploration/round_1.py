def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    out = {}
    # 1. book gain per bar: timing vs market
    rows = []
    for c, ws in bars.items():
        rets = []
        for w, b in ws.items():
            r = b["close"].shift(-1) / b["close"] - 1
            rets.append(r.dropna())
        mu = pd.concat(rets).mean()
        for w, b in ws.items():
            r = (b["close"].shift(-1) / b["close"] - 1)
            a = b["postRebalance_current_allocation"].fillna(0)
            g = (a * r).dropna()
            m = (a * mu)[g.index]
            rows.append(dict(coin=c, window=w, gain=g.sum(), market=m.sum(), exposure=(a.abs() > 0).mean(),
                             coin_ret=r.sum(), mean_alloc=a.mean()))
    df = pd.DataFrame(rows)
    pc = df.groupby("coin")[["gain", "market", "exposure", "mean_alloc"]].agg({"gain": "sum", "market": "sum", "exposure": "mean", "mean_alloc": "mean"})
    pc["timing"] = pc["gain"] - pc["market"]
    out["per_coin_gain_sum"] = pc.sort_values("gain")
    pw = df.groupby("window")[["gain", "market", "coin_ret"]].sum()
    pw["timing"] = pw["gain"] - pw["market"]
    out["per_window"] = pw
    out["totals"] = pd.Series(dict(gain=df.gain.sum(), market=df.market.sum(), timing=df.gain.sum() - df.market.sum(), exposure=df.exposure.mean()))
    # 2. trades concentration
    T = []
    for c, ws in trades.items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; T.append(t)
    T = pd.concat(T)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series(dict(n=len(T), mean_net=p.mean(), median_net=p.median(), win=(p > 0).mean(),
                                   sum_net=p.sum(), top10_sum=p.head(10).sum(), top50_sum=p.head(50).sum(),
                                   mean_dur_h=T["duration_minutes"].mean() / 60))
    # 3. breakouts from prices: horizons, narrowness, prior trend
    H = [3, 6, 12, 18, 36, 72]
    cases = {h: [] for h in H}
    for c, ws in bars.items():
        allr = {h: [] for h in H}
        prep = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            hi12 = b["high"].rolling(12).max().shift(1)
            lo12 = b["low"].rolling(12).min().shift(1)
            rng = (b["high"] - b["low"]).rolling(180).mean()
            narrow = rng / (hi12 - lo12)
            brk = (b["close"] > hi12)
            size = (b["close"] - hi12) / b["close"] * 100
            tr30 = b["close"] / b["close"].shift(180) - 1
            tr7 = b["close"] / b["close"].shift(42) - 1
            for h in H:
                fr = b["close"].shift(-h) / b["close"] - 1
                allr[h].append(fr.iloc[::h].dropna())
            prep.append((b, brk, narrow, size, tr30, tr7))
        for h in H:
            s = pd.concat(allr[h]); mu, sd = s.mean(), s.std()
            for (b, brk, narrow, size, tr30, tr7) in prep:
                fr = b["close"].shift(-h) / b["close"] - 1
                cell = np.arange(len(b)) // h
                d = pd.DataFrame(dict(cell=cell, brk=brk, fr=fr, narrow=narrow, size=size, tr30=tr30, tr7=tr7, fc=b["forecast"]))
                d = d[d.brk & d.fr.notna() & d.narrow.notna()]
                d = d.groupby("cell").first()
                d["un"] = d.fr - mu; d["st"] = d.un / sd; d["coin"] = c
                cases[h].append(d)
    rs = []
    for h in H:
        d = pd.concat(cases[h])
        rs.append(dict(h=h, n=len(d), unusual=d.un.mean(), t=d.un.mean() / (d.un.std() / np.sqrt(len(d))), total=d.fr.mean(), strength=d.st.mean()))
    out["breakout_by_horizon"] = pd.DataFrame(rs)
    d = pd.concat(cases[18])
    d["nq"] = pd.qcut(d.narrow.rank(method="first"), 5, labels=False)
    d["tq"] = pd.qcut(d.tr30.rank(method="first"), 5, labels=False)
    d["t7q"] = pd.qcut(d.tr7.rank(method="first"), 5, labels=False)
    def g(col):
        x = d.groupby(col).agg(n=("un", "size"), unusual=("un", "mean"), sd=("un", "std"), total=("fr", "mean"), xv=(col.replace("q","") if False else "un", "count"))
        x["t"] = x.unusual / (x.sd / np.sqrt(x.n)); return x.drop(columns=["xv", "sd"])
    out["h18_by_narrow_quint"] = g("nq")
    out["h18_by_trend30_quint"] = g("tq")
    out["h18_by_trend7_quint"] = g("t7q")
    out["h18_forecast_desc"] = d.fc.describe()
    return out
