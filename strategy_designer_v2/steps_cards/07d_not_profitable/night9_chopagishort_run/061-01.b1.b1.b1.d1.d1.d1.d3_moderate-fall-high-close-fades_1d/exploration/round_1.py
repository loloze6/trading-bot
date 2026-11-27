def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    allret = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).astype(float)
            loc = ((c - b["low"]) / rng.replace(0, np.nan))
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            inprof = b["regime"].isin(["mean_reversion", "unknown"])
            idx = np.arange(0, len(b), H)
            for i in idx:
                if pd.isna(fwd.iloc[i]):
                    continue
                allret.append((coin, fwd.iloc[i]))
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i], fwd=fwd.iloc[i],
                                 loc=loc.iloc[i], r5=r5.iloc[i], r20=r20.iloc[i], r60=r60.iloc[i],
                                 prof=bool(inprof.iloc[i]), reg=b["regime"].iloc[i],
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    df["un"] = -(df["fwd"] - df["coin"].map(drift))  # short direction
    df["day"] = pd.to_datetime(df["ts"]).dt.floor("D")

    def summ(m):
        s = df[m]
        if len(s) < 3:
            return pd.Series(dict(n=len(s), mean=np.nan, t=np.nan, days=0))
        g = s.groupby("day")["un"].sum()
        nd = len(g)
        mu = s["un"].mean()
        se = np.sqrt((g - g.mean() * 0 - s.groupby("day")["un"].size() * mu).pow(2).sum()) / len(s)
        return pd.Series(dict(n=len(s), mean=mu, t=mu / se if se > 0 else np.nan, days=nd))

    P = df["prof"]; hi = df["loc"] >= 0.5; neg5 = df["r5"] < 0
    band = df["r20"].between(-0.20, -0.10)
    fall20 = df["r20"] < 0
    out = {}
    cases = {
        "tested: prof&hi&neg5&band": P & hi & neg5 & band,
        "prof only": P,
        "prof&hi": P & hi,
        "prof&lo": P & ~hi,
        "prof&hi&neg5": P & hi & neg5,
        "prof&hi&r20<0": P & hi & fall20,
        "prof&hi&neg5&r20<0": P & hi & neg5 & fall20,
        "prof&hi&neg5&r20<-20": P & hi & neg5 & (df["r20"] < -0.20),
        "prof&hi&neg5&r20 0..-10": P & hi & neg5 & df["r20"].between(-0.10, 0),
        "prof&neg5&band (any loc)": P & neg5 & band,
        "prof&lo&neg5&band": P & ~hi & neg5 & band,
        "prof&loc>=.75": P & (df["loc"] >= 0.75),
        "prof&loc>=.75&neg5": P & (df["loc"] >= 0.75) & neg5,
        "noprof&hi&neg5&band": ~P & hi & neg5 & band,
        "noprof&hi&neg5": ~P & hi & neg5,
        "all hi&neg5&r20<0": hi & neg5 & fall20,
        "noprof&hi&neg5&r20<0": ~P & hi & neg5 & fall20,
        "choppy(r60) any agit & hi&neg5&r20<0": df["r60"].between(-0.1, 0.1) & hi & neg5 & fall20,
        "falling(r60) & hi&neg5&r20<0": (df["r60"] < -0.1) & hi & neg5 & fall20,
        "rising(r60) & hi&neg5&r20<0": (df["r60"] > 0.1) & hi & neg5 & fall20,
    }
    out["cases"] = pd.DataFrame({k: summ(m) for k, m in cases.items()}).T
    # gradedness in broad case prof&neg5&r20<0 by loc quartile
    m = P & neg5 & fall20
    s = df[m].copy()
    s["q"] = pd.cut(s["loc"], [0, .25, .5, .75, 1.0001], include_lowest=True)
    out["prof&neg5&r20<0 by loc"] = s.groupby("q")["un"].agg(["count", "mean"])
    m2 = hi & neg5 & fall20
    s2 = df[m2].copy()
    s2["q"] = pd.cut(s2["loc"], [0.5, .75, 1.0001], include_lowest=True)
    out["all-profile hi&neg5&r20<0 by loc,prof"] = s2.groupby(["prof", "q"])["un"].agg(["count", "mean"])
    out["tested by year"] = df[cases["tested: prof&hi&neg5&band"]].groupby("year")["un"].agg(["count", "mean"])
    out["broad prof&hi&neg5&r20<0 by year"] = df[cases["prof&hi&neg5&r20<0"]].groupby("year")["un"].agg(["count", "mean"])
    out["share in profile"] = float(P.mean())
    # book: trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tt["w"] = w; tr.append(tt)
    if tr:
        T = pd.concat(tr)
        out["trades"] = pd.Series(dict(n=len(T), mean_net=T["net_profit_loss_percent"].mean(),
                                       win=(T["net_profit_loss_percent"] > 0).mean(),
                                       med_dur_days=T["duration_minutes"].median() / 1440,
                                       worst=T["net_profit_loss_percent"].min(),
                                       best=T["net_profit_loss_percent"].max()))
    # book allocation size
    al = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            a = b["postRebalance_current_allocation"].abs()
            al.append(a[a > 0])
    al = pd.concat(al)
    out["abs alloc when held"] = al.describe()
    return out
