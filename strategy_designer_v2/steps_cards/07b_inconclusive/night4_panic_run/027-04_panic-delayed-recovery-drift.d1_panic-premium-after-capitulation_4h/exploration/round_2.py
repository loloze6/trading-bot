import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [78, 84]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    cases = []; panics = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; n = len(cl)
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            f = df["forecast"].fillna(0).values
            s = df["close"]
            r24 = s / s.shift(6) - 1
            sd = r24.rolling(180).std()
            rng = (df["high"].rolling(6).max() - df["low"].rolling(6).min()) / s
            rm = rng / rng.rolling(180).mean()
            pscore = (np.clip(-r24 / sd, 0, None) * rm).values
            prior = (s.shift(6) / s.shift(546) - 1).values
            p30 = (s.shift(6) / s.shift(186) - 1).values
            lowest = None
            for start in range(0, n, 78):
                done = False
                for t in range(start, min(start + 78, n)):
                    if f[t] <= 0:
                        lowest = None; continue
                    if lowest is None: lowest = f[t]
                    lowest = min(lowest, f[t])
                    if not done and f[t] - lowest >= 2:
                        u = (cl[t + 78] / cl[t] - 1 - drift[(c, 78)]) if t + 78 < n else np.nan
                        cases.append(dict(coin=c, year=year[t], f=f[t], prior=prior[t], p30=p30[t], u78=u,
                                          s78=u / usual[(c, 78)] if u == u else np.nan)); done = True; lowest = None
                for t in range(start, min(start + 78, n)):
                    if pscore[t] == pscore[t] and pscore[t] > 3:
                        u = (cl[t + 84] / cl[t + 6] - 1 - drift[(c, 78)]) if t + 84 < n else np.nan
                        panics.append(dict(coin=c, year=year[t], ps=pscore[t], p30=p30[t], u=u,
                                           s=u / usual[(c, 78)] if u == u else np.nan)); break
    C = pd.DataFrame(cases); P = pd.DataFrame(panics)
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["cases_all"] = summ(C, "u78")
    out["cases_prior_nonnan_share"] = float(C.prior.notna().mean())
    Cn = C[C.year != 2020]
    out["cases_ex2020"] = summ(Cn, "u78")
    C["p30q"] = pd.qcut(C["p30"].rank(method="first"), 4, labels=["deep", "q2", "q3", "shallow"])
    out["cases_by_p30q"] = C.groupby("p30q").apply(lambda g: pd.concat([summ(g, "u78"), pd.Series({"p30": g.p30.mean()})]))
    Cn = C[C.year != 2020].copy()
    out["cases_by_p30q_ex2020"] = Cn.groupby("p30q").apply(lambda g: summ(g, "u78"))
    out["cases_spearman_f_u78"] = pd.Series(stats.spearmanr(C.f, C.u78, nan_policy="omit"), index=["rho", "p"])
    out["panics_all_u6_84"] = summ(P, "u")
    out["panics_strength"] = float(P.s.mean())
    P["p30q"] = pd.qcut(P["p30"].rank(method="first"), 4, labels=["deep", "q2", "q3", "shallow"])
    out["panics_by_p30q"] = P.groupby("p30q").apply(lambda g: pd.concat([summ(g, "u"), pd.Series({"p30": g.p30.mean()})]))
    out["panics_spearman_ps_u"] = pd.Series(stats.spearmanr(P.ps, P.u, nan_policy="omit"), index=["rho", "p"])
    out["panics_spearman_p30_u"] = pd.Series(stats.spearmanr(P.p30, P.u, nan_policy="omit"), index=["rho", "p"])
    out["panics_ex2021_2024"] = summ(P[~P.year.isin([2021, 2024])], "u")
    return out
