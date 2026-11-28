import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # down run length ending yesterday, today up close
            run = np.zeros(n, int); cur = 0
            for i in range(1, n):
                if r[i] < 0:
                    cur += 1
                else:
                    if r[i] > 0:
                        run[i] = cur
                    cur = 0
            # current down run length (for days still falling)
            dn = np.zeros(n, int); cur = 0
            for i in range(1, n):
                cur = cur + 1 if r[i] < 0 else 0
                dn[i] = cur
            reg = b["regime"].astype(str).values
            fc = reg != "chop"
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(1, n):
                d = {"coin": coin, "w": w, "year": yr[i], "fc": fc[i], "run": run[i], "dn": dn[i],
                     "r0": r[i]}
                for h in (1, 2, 3, 5):
                    d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    mu = df.groupby("coin")["f1"].mean()
    for h in (1, 2, 3, 5):
        df[f"x{h}"] = df[f"f{h}"] - h * df["coin"].map(mu)
    df["rb"] = df["run"].clip(upper=5)
    out = {}
    up = df[df["run"] >= 1]
    def summ(g):
        res = {"n": len(g)}
        for h in (1, 2, 3, 5):
            x = g[f"x{h}"].dropna()
            res[f"x{h}"] = x.mean()
            res[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(res)
    out["upday_after_run_by_profile_run (excess, + = rise)"] = up.groupby(["fc", "rb"]).apply(summ)
    fcu = up[(up.fc) & (up.run >= 2)].copy()
    out["fc_run2+_by_coin"] = fcu.groupby("coin").apply(summ)
    out["fc_run2+_by_year"] = fcu.groupby("year").apply(summ)
    fcu["r0q"] = pd.qcut(fcu["r0"], 3, labels=["small", "mid", "big"])
    out["fc_run2+_by_upday_size"] = fcu.groupby("r0q").apply(summ)
    dnd = df[(df.fc) & (df.dn >= 1)].copy()
    dnd["db"] = dnd["dn"].clip(upper=5)
    out["fc_down_days_by_current_run"] = dnd.groupby("db").apply(summ)
    out["fc_all_days"] = summ(df[df.fc])
    out["coin_mean_daily"] = mu
    return out
