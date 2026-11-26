import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            loc = np.where(rng > 0, (c - lo) / np.where(rng > 0, rng, 1), np.nan)
            ret1 = pd.Series(c).pct_change()
            gain = (ret1 / ret1.rolling(20).std()).values
            locz = pd.Series(loc).rolling(60, min_periods=20).apply(lambda x: (x[-1]-x.mean())/x.std(), raw=True).values
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values
            n = len(c)
            for i in range(n):
                if reg[i] != "mean_reversion":
                    continue
                rec = dict(coin=coin, w=w, i=i, cell10=i // 10, cell5=i // 5, loc=loc[i], gain=gain[i],
                           fc=abs(fc[i]), locz=locz[i], ts=str(df["timestamp"].iloc[i])[:10])
                for h in H:
                    rec[f"u{h}"] = -(c[i+h]/c[i]-1-drift[(coin, h)]) if i+h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def split(cases, key, col):
        x = cases.dropna(subset=[key, col])
        med = x[key].median()
        hi_ = x[x[key] >= med][col]; lo_ = x[x[key] < med][col]
        return pd.Series(dict(n_hi=len(hi_), m_hi=hi_.mean(), n_lo=len(lo_), m_lo=lo_.mean(), diff=hi_.mean()-lo_.mean()))
    for h, cell in [(5, "cell5"), (10, "cell10")]:
        cases = d.sort_values("i").groupby(["coin", "w", cell]).head(1)
        out[f"split_h{h}"] = pd.DataFrame({k: split(cases, k, f"u{h}") for k in ["fc", "loc", "gain"]}).T
        out[f"corr_h{h}"] = cases[["fc", "loc", "locz", "gain", f"u{h}"]].corr().round(3)
        cases = cases.copy()
        cases["locb"] = pd.cut(cases["loc"], [0.74, 0.85, 0.95, 1.01])
        cases["gb"] = pd.cut(cases["gain"], [0, 0.5, 1.2])
        out[f"loc_x_gain_h{h}"] = cases.groupby(["locb", "gb"], observed=True)[f"u{h}"].agg(["count", "mean"])
        cases["locb2"] = pd.cut(cases["loc"], [0.74, 0.9, 1.01])
        out[f"loc_by_window_h{h}"] = cases.groupby(["w", "locb2"], observed=True)[f"u{h}"].mean().unstack()
    return out
