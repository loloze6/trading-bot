def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c]}, key=lambda s: int(s[1:]))
    # ---- book daily chain
    chain = []
    for w in wins:
        cols = {}
        for c in coins:
            if w in days[c]:
                d = days[c][w].set_index("day")["book_return"]
                cols[c] = d
        df = pd.DataFrame(cols)
        r = df.mean(axis=1).dropna()
        for v in r.values:
            chain.append((w, v))
    ch = pd.DataFrame(chain, columns=["w", "r"])
    eq = (1 + ch.r).cumprod()
    dd = eq / eq.cummax() - 1
    ch["dd"] = dd.values
    ch["eq"] = eq.values
    # deepest fall: trough and peak
    t = dd.idxmin(); p = eq[:t + 1].idxmax()
    deep = {"depth": float(dd.min()), "peak_window": ch.w[p], "trough_window": ch.w[t], "days_peak_to_trough": int(t - p)}
    # per window book stats
    pw = ch.groupby("w").agg(mean=("r", "mean"), sd=("r", "std"), n=("r", "size"), mindd=("dd", "min"))
    pw["sum"] = ch.groupby("w").r.sum()
    pw = pw.loc[[w for w in wins if w in pw.index]]
    # ---- cases
    rows = []
    allwk = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b.timestamp)
            cl = b.close.values; vol = b.volume.values
            lr = np.log(b.close).diff()
            vol30 = lr.rolling(720).std()
            vol30rel = vol30 / vol30.rolling(2160, min_periods=720).mean()
            n = len(b)
            idx = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23))[0]
            for i in idx:
                if i < 168 + 120 or i + 48 >= n: continue
                wkr = cl[i] / cl[i - 48] - 1
                vr = vol[i - 47:i + 1].mean() / vol[i - 167:i - 47].mean()
                pre = cl[i - 48] / cl[i - 168] - 1
                pre30 = cl[i - 48] / cl[max(0, i - 720)] - 1
                fwd = cl[i + 48] / cl[i] - 1
                # path: max adverse excursion signed by weekend move
                s = np.sign(wkr)
                path = s * (cl[i + 1:i + 49] / cl[i] - 1)
                f = b.forecast.iloc[i]; a = b.postRebalance_current_allocation.iloc[i]
                rec = dict(coin=c, w=w, year=ts.iloc[i].year, wkr=wkr, vr=vr, pre=pre, pre30=pre30, fwd=fwd,
                           sfwd=s * fwd, mae=path.min(), f=f, a=a, v30=vol30rel.iloc[i],
                           sig=(f != 0) and not np.isnan(f), absw=abs(wkr) / (vol30.iloc[i] * np.sqrt(48)))
                allwk.append(rec)
    A = pd.DataFrame(allwk)
    S = A[A.sig].copy()
    S["pnl"] = S.a * S.fwd
    S["agree_pre"] = np.sign(S.wkr) == np.sign(S.pre)
    S["agree_pre30"] = np.sign(S.wkr) == np.sign(S.pre30)
    def g(df, key):
        return df.groupby(key).agg(n=("pnl", "size"), mean_pnl=("pnl", "mean"), sfwd=("sfwd", "mean"),
                                  sd=("pnl", "std"), min_pnl=("pnl", "min"), mae=("mae", "mean"))
    out = {}
    out["deepest"] = pd.Series(deep)
    out["per_window"] = pw.round(5)
    out["by_year"] = g(S, "year")
    out["by_coin"] = g(S, "coin")
    S["side"] = np.where(S.wkr > 0, "long", "short")
    out["by_side"] = g(S, "side")
    out["by_agree_pre"] = g(S, "agree_pre")
    out["by_agree_pre30"] = g(S, "agree_pre30")
    S["v30q"] = pd.qcut(S.v30, 4, labels=False, duplicates="drop")
    out["by_v30q"] = g(S, "v30q")
    S["absq"] = pd.qcut(S.absw, 4, labels=False)
    out["by_absq"] = g(S, "absq")
    S["fq"] = pd.qcut(S.f.abs(), 4, labels=False, duplicates="drop")
    out["by_fq"] = g(S, "fq")
    # worst cases features
    worst = S.nsmallest(20, "pnl")
    out["worst20_profile"] = pd.Series({"mean_absw": worst.absw.mean(), "all_absw": S.absw.mean(),
        "mean_v30": worst.v30.mean(), "all_v30": S.v30.mean(), "share_long": (worst.wkr > 0).mean(),
        "share_agree_pre": worst.agree_pre.mean(), "all_agree_pre": S.agree_pre.mean(),
        "mean_absa": worst.a.abs().mean(), "all_absa": S.a.abs().mean(), "sum_worst20": worst.pnl.sum(), "sum_all": S.pnl.sum()})
    # all weekends: heavy vs not, continuation
    A["heavy"] = A.vr > 1
    out["all_weekends_heavy"] = A.groupby("heavy").agg(n=("sfwd", "size"), sfwd=("sfwd", "mean"),
                                                       t=("sfwd", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    return out
