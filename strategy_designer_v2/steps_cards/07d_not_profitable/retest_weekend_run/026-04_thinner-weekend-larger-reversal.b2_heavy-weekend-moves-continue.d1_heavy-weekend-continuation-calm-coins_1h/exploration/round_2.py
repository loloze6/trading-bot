def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    coins = list(bars.keys())
    allwk = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b.timestamp)
            cl = b.close.values; vol = b.volume.values
            lr = np.log(b.close).diff()
            vol30 = lr.rolling(720).std()
            n = len(b)
            idx = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23))[0]
            for i in idx:
                if i < 288 or i + 48 >= n: continue
                wkr = cl[i] / cl[i - 48] - 1
                vr = vol[i - 47:i + 1].mean() / vol[i - 167:i - 47].mean()
                pre = cl[i - 48] / cl[i - 168] - 1
                s = np.sign(wkr)
                f = b.forecast.iloc[i]; a = b.postRebalance_current_allocation.iloc[i]
                allwk.append(dict(coin=c, w=int(w[1:]), wk=ts.iloc[i].floor("D"), year=ts.iloc[i].year,
                    wkr=wkr, vr=vr, pre=pre, s=s, f=f, a=a,
                    sfwd48=s * (cl[i + 48] / cl[i] - 1), sfwd24=s * (cl[i + 24] / cl[i] - 1),
                    sfwd12=s * (cl[i + 12] / cl[i] - 1),
                    sig=(f != 0) and not np.isnan(f), absw=abs(wkr) / (vol30.iloc[i] * np.sqrt(48))))
    A = pd.DataFrame(allwk)
    A["agree"] = np.sign(A.wkr) == np.sign(A.pre)
    A["heavy"] = A.vr > 1
    tf = lambda x: x.mean() / x.std() * np.sqrt(len(x))
    out = {}
    out["heavy_x_agree"] = A.groupby(["heavy", "agree"]).agg(n=("sfwd48", "size"), sfwd48=("sfwd48", "mean"), t=("sfwd48", tf), sfwd24=("sfwd24", "mean"))
    S = A[A.sig].copy()
    out["horizon"] = pd.DataFrame({h: [S[h].mean(), tf(S[h])] for h in ["sfwd12", "sfwd24", "sfwd48"]}, index=["mean", "t"])
    S["late"] = np.where(S.w >= 22, "w22-24", "w1-21")
    out["late_profile"] = S.groupby("late").agg(n=("a", "size"), sfwd=("sfwd48", "mean"), absa=("a", lambda x: x.abs().mean()),
        absw=("absw", "mean"), agree=("agree", "mean"), long=("s", lambda x: (x > 0).mean()), vr=("vr", "mean"))
    S["late_side"] = S.late + "_" + np.where(S.s > 0, "L", "S")
    out["late_side"] = S.groupby("late_side").agg(n=("a", "size"), sfwd=("sfwd48", "mean"), pnl=("a", "size"))
    S["late_agree"] = S.late + "_" + S.agree.astype(str)
    out["late_agree"] = S.groupby("late_agree").agg(n=("a", "size"), sfwd=("sfwd48", "mean"))
    # per-weekend chain variants
    def chain(df, pos, ret):
        r = (df.assign(p=pos * ret).groupby(["w", "wk"]).p.sum() / 6).sort_index()
        eq = (1 + r).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yrs = 7.94
        yr = eq.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar_proxy": yr / -dd, "n": len(df)})
    sa = S.s * S.a.abs()
    base_pos = S.a
    capped = np.sign(S.a) * np.minimum(S.a.abs(), S.a.abs().median())
    flat = np.sign(S.a) * S.a.abs().mean()
    res = {"base48": chain(S, base_pos, S.s * S.sfwd48 * 0 + S.sfwd48 * np.sign(S.a) * S.s),
           }
    # pnl = a * fwd = |a| * sfwd when sign(a)=s
    absa = S.a.abs()
    res = {"base48": chain(S, absa, S.sfwd48),
           "base24": chain(S, absa, S.sfwd24),
           "capped48": chain(S, np.minimum(absa, absa.median()), S.sfwd48),
           "flat48": chain(S, pd.Series(absa.mean(), index=S.index), S.sfwd48),
           "agree_only48": chain(S[S.agree], absa[S.agree], S.sfwd48[S.agree]),
           "agree_capped48": chain(S[S.agree], np.minimum(absa, absa.median())[S.agree], S.sfwd48[S.agree])}
    out["chains"] = pd.DataFrame(res).T
    out["sign_a_matches_s"] = float((np.sign(S.a) == S.s).mean())
    S["aq"] = pd.qcut(absa, 4, labels=False)
    out["by_absa_q"] = S.groupby("aq").agg(n=("a", "size"), absa=("a", lambda x: x.abs().mean()), sfwd=("sfwd48", "mean"), sd=("sfwd48", "std"))
    return out
