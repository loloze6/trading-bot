def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [6, 12, 18, 36]
    drift = {}
    for coin, wins in bars.items():
        for h in hs:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr)
            drift[(coin, h, "sd")] = np.std(rr)
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            f = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # streak length (up bars in a row ending at t)
            L = np.zeros(n, int)
            for t in range(1, n):
                L[t] = L[t-1] + 1 if r1[t] > 0 else 0
            for h in hs:
                for t in range(0, n - h, h):
                    if not (f[t] > 0) or L[t] < 1:
                        continue
                    s = t - L[t] + 1
                    vs = v[s:t+1]
                    # volume fade: last bar volume vs mean of streak bars, or vs prior 30-bar mean
                    vprior = np.nanmean(v[max(0, s-30):s]) if s > 0 else np.nan
                    fade = vs[-1] / np.mean(vs) if len(vs) > 1 else np.nan
                    rows.append(dict(coin=coin, win=w, year=yr[t], h=h, f=f[t], L=L[t],
                                     ex=c[t+h]/c[t]-1-drift[(coin, h)],
                                     tot=c[t+h]/c[t]-1, fade=fade,
                                     vrel=vs.mean()/vprior if vprior and vprior > 0 else np.nan))
    d = pd.DataFrame(rows)
    def tt(x):
        x = np.asarray(x); x = x[~np.isnan(x)]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))))
    out = {}
    out["by_h_weighted"] = d.groupby("h").apply(lambda g: tt(g.f/10*g.ex))
    out["by_h_excess"] = d.groupby("h").apply(lambda g: tt(g.ex))
    g18 = d[d.h == 18].copy()
    out["18_by_coin"] = g18.groupby("coin").apply(lambda g: tt(g.f/10*g.ex))
    out["18_by_year"] = g18.groupby("year").apply(lambda g: tt(g.ex))
    g18["fq"] = pd.qcut(g18.f, 5, labels=False, duplicates="drop")
    out["18_by_fquint_ex"] = g18.groupby("fq").apply(lambda g: pd.concat([tt(g.ex), pd.Series({"fmean": g.f.mean(), "Lmean": g.L.mean()})]))
    out["18_by_len"] = g18.assign(Lb=np.clip(g18.L, 1, 6)).groupby("Lb").apply(lambda g: tt(g.ex))
    g18["fadeq"] = pd.qcut(g18.fade, 3, labels=False, duplicates="drop")
    out["18_multi_by_fade_tercile"] = g18[g18.L >= 2].groupby("fadeq").apply(lambda g: tt(g.ex))
    g18["vrq"] = pd.qcut(g18.vrel, 3, labels=False, duplicates="drop")
    out["18_by_vrel_tercile"] = g18.groupby("vrq").apply(lambda g: tt(g.ex))
    for h in [6, 12, 36]:
        gh = d[d.h == h].copy()
        gh["fq"] = pd.qcut(gh.f, 3, labels=False, duplicates="drop")
        out[f"{h}_by_ftercile"] = gh.groupby("fq").apply(lambda g: tt(g.ex))
    out["sd18"] = pd.Series({k[0]: v for k, v in drift.items() if len(k) == 3 and k[1] == 18})
    return out
