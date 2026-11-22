import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    FC = "forecast"
    H = [6, 18, 42, 78, 84]
    # normal drift and usual move per coin per horizon
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
            f = df[FC].fillna(0).values
            raw = df.get("debug_info.components.capitulation_panic.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            # price-based panic and prior fall
            s = df["close"]
            r24 = s / s.shift(6) - 1
            sd = r24.rolling(180).std()
            rng = (df["high"].rolling(6).max() - df["low"].rolling(6).min()) / s
            rm = rng / rng.rolling(180).mean()
            pscore = (np.clip(-r24 / sd, 0, None) * rm).values
            prior = (s.shift(6) / s.shift(546) - 1).values
            r7 = (s / s.shift(42) - 1).values
            # cases as in step 5 (approx)
            lowest = None
            for start in range(0, n, 78):
                done = False
                for t in range(start, min(start + 78, n)):
                    if f[t] <= 0:
                        lowest = None; continue
                    if lowest is None: lowest = f[t]
                    lowest = min(lowest, f[t])
                    if not done and f[t] - lowest >= 2:
                        rec = dict(coin=c, w=w, year=year[t], f=f[t], raw=raw[t], prior=prior[t], ps=pscore[t], r7=r7[t])
                        for h in H:
                            rec[f"u{h}"] = (cl[t + h] / cl[t] - 1 - drift[(c, h)]) if t + h < n else np.nan
                        # delayed: from t to t+... already delayed 1d by construction
                        cases.append(rec); done = True; lowest = None
                # price panics: first bar in cell with pscore above 3
                for t in range(start, min(start + 78, n)):
                    if pscore[t] == pscore[t] and pscore[t] > 3:
                        rec = dict(coin=c, year=year[t], ps=pscore[t], prior=prior[t])
                        for h in [6, 42, 84]:
                            rec[f"u{h}"] = (cl[t + h] / cl[t] - 1 - drift[(c, h)]) if t + h < n else np.nan
                        rec["u6_84"] = (cl[t + 84] / cl[t + 6] - 1 - drift[(c, 78)]) if t + 84 < n else np.nan
                        panics.append(rec); break
    C = pd.DataFrame(cases); P = pd.DataFrame(panics)
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["cases_by_horizon"] = pd.DataFrame({h: summ(C, f"u{h}") for h in H}).T
    out["cases_by_coin_u78"] = C.groupby("coin").apply(lambda g: summ(g, "u78"))
    out["cases_by_year_u78"] = C.groupby("year").apply(lambda g: summ(g, "u78"))
    C["fq"] = pd.qcut(C["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["cases_by_forecast_q"] = C.groupby("fq").apply(lambda g: pd.concat([summ(g, "u78"), pd.Series({"u6": g.u6.mean(), "u42": g.u42.mean(), "fmean": g.f.mean()})]))
    C["pq"] = pd.qcut(C["prior"].rank(method="first"), 4, labels=["deep", "q2", "q3", "shallow"])
    out["cases_by_prior_q"] = C.groupby("pq").apply(lambda g: pd.concat([summ(g, "u78"), pd.Series({"prior_mean": g.prior.mean()})]))
    C["psq"] = pd.qcut(C["ps"].rank(method="first"), 4, labels=["low", "q2", "q3", "high"])
    out["cases_by_pricepanic_q"] = C.groupby("psq").apply(lambda g: pd.concat([summ(g, "u78"), pd.Series({"ps_mean": g.ps.mean()})]))
    out["cases_count_ps_gt3"] = float((C.ps > 3).mean())
    P["side"] = np.where(P.prior < 0, "prior_neg", "prior_pos")
    P["psq"] = pd.qcut(P["ps"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["panics_by_side"] = P.groupby("side").apply(lambda g: pd.concat([summ(g, "u84"), pd.Series({"u6": g.u6.mean(), "u42": g.u42.mean(), "u6_84": g.u6_84.mean()})]))
    out["panics_by_ps"] = P.groupby("psq").apply(lambda g: pd.concat([summ(g, "u84"), pd.Series({"u6_84": g.u6_84.mean(), "ps": g.ps.mean()})]))
    out["panics_by_coin"] = P.groupby("coin").apply(lambda g: summ(g, "u84"))
    out["panics_by_year"] = P.groupby("year").apply(lambda g: summ(g, "u84"))
    return out
