import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [24, 48, 120, 240]
    rows = []
    # usual move per coin per horizon from non-overlapping grid
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
    for coin, wins in bars.items():
        for wi, (w, df) in enumerate(wins.items()):
            c = df["close"].values
            n = len(c)
            s = pd.Series(c)
            r24 = s / s.shift(24) - 1
            mabs = r24.abs().shift(1).rolling(720, min_periods=120).mean()
            m = (r24 / mabs).values
            mom30 = (s / s.shift(720) - 1).values
            fc = df["forecast"].values
            prev_m = np.r_[np.nan, m[:-1]]
            for start in range(0, n, 120):
                end = min(start + 120, n)
                seg = m[start:end]
                # first bar in cell where multiple <= -1 and it is a new crossing
                cand = np.where((seg <= -1.0))[0]
                if len(cand) == 0:
                    continue
                t = start + cand[0]
                rec = dict(coin=coin, win=wi, m=m[t], mom30=mom30[t], fc=fc[t],
                           first=bool(prev_m[t] > -1.0), hour=pd.Timestamp(df["timestamp"].iloc[t]).hour,
                           year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for h in H:
                    if t + h < n:
                        mu, sd = usual[(coin, h)]
                        rec[f"s{h}"] = -((c[t + h] / c[t] - 1) - mu) / sd
                        rec[f"tot{h}"] = -(c[t + h] / c[t] - 1)
                    else:
                        rec[f"s{h}"] = np.nan
                        rec[f"tot{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"s{h}"].dropna()
            out[f"n{h}"] = len(x)
            out[f"mean{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    d["mb"] = pd.cut(d["m"], [-100, -3, -2, -1.5, -1.0])
    d["reg"] = np.where(d["mom30"] > 0, "up30", "down30")
    res = {
        "all": summ(d).to_frame().T,
        "by_multiple": d.groupby("mb").apply(summ),
        "by_coin": d.groupby("coin").apply(summ),
        "by_regime": d.groupby("reg").apply(summ),
        "by_regime_mult": d.groupby(["reg", "mb"]).apply(summ),
        "by_year": d.groupby("year").apply(summ),
        "spearman_m_s120": stats.spearmanr(-d["m"], d["s120"], nan_policy="omit")[0],
        "spearman_m_s24": stats.spearmanr(-d["m"], d["s24"], nan_policy="omit")[0],
    }
    return res
