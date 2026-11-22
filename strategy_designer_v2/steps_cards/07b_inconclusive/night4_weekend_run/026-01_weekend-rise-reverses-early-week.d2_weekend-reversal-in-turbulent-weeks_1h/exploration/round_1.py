import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        g = {h: [] for h in (24, 48, 72, 96)}
        for w, df in ws.items():
            c = df["close"].values
            for h in g:
                idx = np.arange(0, len(c) - h, h)
                g[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(v) for h, v in g.items()}
        drift[coin]["sd48"] = np.std(g[48])
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            n = len(c)
            # anchor: bar closing at a day's 00:00 (start 23:00), any weekday
            cand = np.where(ts.dt.hour.values == 23)[0]
            for t in cand:
                if t < 48:
                    continue
                closeday = (ts.iloc[t] + pd.Timedelta(hours=1)).dayofweek
                r = {"coin": coin, "w": w, "closeday": closeday,
                     "past48": c[t] / c[t - 48] - 1,
                     "fc": df["forecast"].iloc[t],
                     "regime": df["regime"].iloc[t],
                     "year": ts.iloc[t].year}
                for h in (24, 48, 72, 96):
                    r[f"f{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                rows.append(r)
    D = pd.DataFrame(rows)
    for h in (24, 48, 72, 96):
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(lambda k: drift[k][h])
    D["sd"] = D["coin"].map(lambda k: drift[k]["sd48"])
    D["hv"] = D["regime"] == "mean_reversion"
    out = {}
    cases = D[(D.fc != 0) & D.fc.notna()].copy()
    out["cases_closeday_counts"] = cases.closeday.value_counts()
    cases["fall48"] = -cases.u48
    cases["absfc"] = cases.fc.abs()
    def summ(g, col="fall48"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["by_coin"] = cases.groupby("coin").apply(summ)
    out["by_year"] = cases.groupby("year").apply(summ)
    cases["q"] = pd.qcut(cases.absfc.rank(method="first"), 5, labels=False)
    out["by_fc_quintile"] = cases.groupby("q").apply(summ)
    cases["pq"] = pd.qcut(cases.past48.rank(method="first"), 5, labels=False)
    q2 = cases.groupby("pq").apply(summ)
    q2["past48_mean"] = cases.groupby("pq").past48.mean()
    out["by_rawgain_quintile"] = q2
    hz = {}
    for h in (24, 48, 72, 96):
        x = -cases[f"u{h}"].dropna()
        hz[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))}
    out["cases_by_horizon"] = pd.DataFrame(hz).T
    # all Monday anchors split by vol regime and side
    mon = D[D.closeday == 0].copy()
    mon["side"] = np.where(mon.past48 > 0, "rise", "fall")
    mon["rev48"] = np.where(mon.past48 > 0, -mon.u48, mon.u48)
    out["monday_regime_side"] = mon.groupby(["hv", "side"]).apply(lambda g: summ(g, "rev48"))
    # weekday control: rises over 48h ending Wed/Thu/Fri 00:00 in high vol
    D["rev48"] = np.where(D.past48 > 0, -D.u48, D.u48)
    hvr = D[D.past48 > 0]
    out["rise_rev48_by_closeday_all_vol"] = hvr.groupby("closeday").apply(lambda g: summ(g, "rev48"))
    # correlation of size with fall in cases
    out["spearman_past48_fall48"] = str(stats.spearmanr(cases.past48, cases.fall48, nan_policy="omit"))
    out["spearman_past48sd_fall48"] = str(stats.spearmanr(cases.past48 / cases.sd, cases.fall48 / cases.sd, nan_policy="omit"))
    return out
