def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            dr = pd.Series(cl).pct_change()
            nxt = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            sd30 = dr.rolling(30, min_periods=10).std().values
            t60 = pd.Series(cl).pct_change(60).values
            down = (dr < 0).values
            k = 0; lo = 0.0
            alloc = b["postRebalance_current_allocation"].values
            for i in range(len(b)):
                if i > 0 and down[i]:
                    k += 1; lo = (1 + lo) * (1 + dr.iloc[i]) - 1
                    run = 0; loss = 0.0
                else:
                    run = k; loss = lo; k = 0; lo = 0.0
                if i == len(b) - 1 or not np.isfinite(t60[i]):
                    continue
                rb = (run >= 2) and dr.iloc[i] > 0
                rows.append(dict(coin=c, w=w, nxt=nxt[i], t60=t60[i], rb=rb, run=run,
                                 depth=-loss / sd30[i] if sd30[i] > 0 else np.nan,
                                 inpos=alloc[i] < 0, up=dr.iloc[i] > 0))
    D = pd.DataFrame(rows)
    D["fall"] = D.t60 < -0.10
    def s(df):
        x = -df["nxt"]
        return pd.Series({"n": len(x), "shortret": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    grp = D.assign(cls=np.where(D.rb & D.inpos, "rb in pos", np.where(D.rb & D.fall, "rb falling not in pos",
                     np.where(D.rb, "rb not falling", np.where(D.fall, "falling no rb", "other")))))
    out["classes"] = grp.groupby("cls").apply(s)
    out["falling no rb, up days only"] = s(D[D.fall & ~D.rb & D.up])
    F = D[D.fall & D.rb & ~D.inpos]
    out["falling not in pos by depth"] = F.groupby(pd.qcut(F.depth, 3, duplicates="drop"), observed=True).apply(s)
    out["falling not in pos by window"] = F.groupby("w").apply(s)
    Fa = D[D.fall & D.rb]
    out["all falling rb by depth"] = Fa.groupby(pd.qcut(Fa.depth, 4, duplicates="drop"), observed=True).apply(s)
    out["all falling rb by run"] = Fa.groupby(Fa.run.clip(upper=5)).apply(s)
    out["all falling rb by window"] = Fa.groupby("w").apply(s)
    R = D[~D.fall & D.rb]
    out["not falling rb by depth"] = R.groupby(pd.qcut(R.depth, 3, duplicates="drop"), observed=True).apply(s)
    # holding 2 days for all falling rb
    return out
