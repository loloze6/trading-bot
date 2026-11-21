import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [48, 120, 240]
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rets.append(c[idx + h] / c[idx] - 1)
            r = np.concatenate(rets)
            usual[(coin, h)] = (r.mean(), r.std(ddof=1))
    rows = []
    for coin, wins in bars.items():
        for wi, (w, df) in enumerate(wins.items()):
            c = df["close"].values
            n = len(c)
            s = pd.Series(c)
            r24 = s / s.shift(24) - 1
            mabs = r24.abs().shift(1).rolling(720, min_periods=120).mean()
            m = (r24 / mabs).values
            r720 = s / s.shift(720) - 1
            sd720 = (s.pct_change(24).rolling(720, min_periods=120).std() * np.sqrt(30)).values
            mom30 = r720.values
            z30 = mom30 / sd720
            for start in range(0, n, 120):
                seg = m[start:min(start + 120, n)]
                cand = np.where(seg <= -1.0)[0]
                if len(cand) == 0:
                    continue
                t = start + cand[0]
                rec = dict(coin=coin, m=m[t], mom30=mom30[t], z30=z30[t],
                           year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for h in H:
                    if t + h < n:
                        mu, sd = usual[(coin, h)]
                        ret = c[t + h] / c[t] - 1
                        rec[f"s{h}"] = -(ret - mu) / sd
                        rec[f"tot{h}"] = -ret
                    else:
                        rec[f"s{h}"] = np.nan; rec[f"tot{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"s{h}"].dropna(); y = g[f"tot{h}"].dropna()
            out[f"n{h}"] = len(x)
            out[f"s{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
            out[f"totpct{h}"] = 100 * y.mean()
            out[f"tott{h}"] = y.mean() / (y.std(ddof=1) / np.sqrt(len(y))) if len(y) > 2 else np.nan
        return pd.Series(out)
    d["mom_q"] = pd.qcut(d["mom30"], 5)
    dn = d[d["mom30"] < 0].copy()
    dn["mom_q"] = pd.qcut(dn["mom30"], 4)
    return {
        "by_mom30_quintile": d.groupby("mom_q").apply(summ),
        "down30_by_mom_quartile": dn.groupby("mom_q").apply(summ),
        "down30_by_coin": dn.groupby("coin").apply(summ),
        "down30_by_year": dn.groupby("year").apply(summ),
        "spearman_mom30_s120_all": stats.spearmanr(-d["mom30"], d["s120"], nan_policy="omit")[0],
        "spearman_mom30_s120_down": stats.spearmanr(-dn["mom30"], dn["s120"], nan_policy="omit")[0],
        "spearman_m_s120_down": stats.spearmanr(-dn["m"], dn["s120"], nan_policy="omit")[0],
    }
