import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            up = r > 0; dn = r < 0
            # run of down days ending yesterday
            run = np.zeros(len(b), dtype=int); cnt = 0
            for i in range(len(b)):
                run[i] = cnt if up.iloc[i] else 0
                cnt = cnt + 1 if dn.iloc[i] else 0
            # up run ending yesterday (for mirror)
            urun = np.zeros(len(b), dtype=int); cnt = 0
            for i in range(len(b)):
                urun[i] = cnt if dn.iloc[i] else 0
                cnt = cnt + 1 if up.iloc[i] else 0
            tr60 = c / c.shift(60) - 1
            sd30 = r.rolling(30).std()
            sd10 = r.rolling(10).std(); sd60 = r.rolling(60).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r": r, "nxt": nxt, "run": run, "urun": urun, "tr60": tr60,
                "rz": r / sd30, "vr": sd10 / sd60, "sd30": sd30,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "body": (c - b["open"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["nxt"])
    mu = D.groupby("coin")["nxt"].transform("mean")
    D["un"] = D["nxt"] - mu
    D["trend"] = np.where(D.tr60 < -0.10, "falling", np.where(D.tr60 > 0.10, "rising", np.where(D.tr60.notna(), "choppy", "na")))
    sdmed = D.groupby("coin")["sd30"].transform("median")
    D["agit"] = np.where(D.sd30 > sdmed, "agit", "calm")

    def summ(g, col="un", sign=1):
        x = sign * g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    cases = D[D.run > 0]
    cases = cases.assign(runb=cases.run.clip(upper=5))
    out["runbreak_by_trend_runlen (short-signed unusual)"] = cases.groupby(["trend", "runb"]).apply(summ, sign=-1)
    out["runbreak_by_trend_agit"] = cases.groupby(["trend", "agit"]).apply(summ, sign=-1)
    # all days by trend: day-after any up day vs down day
    D["dirr"] = np.sign(D.r)
    out["all_days_trend_x_todaysign (unusual, long-signed)"] = D.groupby(["trend", "dirr"]).apply(summ)
    # by today's return z quintile and trend
    D["rzq"] = D.groupby("coin")["rz"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["rz_quintile_x_trend (long-signed unusual)"] = D.groupby(["trend", "rzq"]).apply(summ)
    # mirror: first down day after up run
    m = D[D.urun > 0].assign(urb=lambda x: x.urun.clip(upper=5))
    out["mirror_downbreak_by_trend_runlen (long-signed)"] = m.groupby(["trend", "urb"]).apply(summ)
    # tested cases: by up-day size, close position, weekday, year
    tc = D[D.fc < 0].copy()
    tc["rzq"] = pd.qcut(tc.rz, 4, labels=False, duplicates="drop")
    out["cases_by_upday_size_q (short-signed)"] = tc.groupby("rzq").apply(summ, sign=-1)
    tc["clq"] = pd.qcut(tc.clpos, 3, labels=False, duplicates="drop")
    out["cases_by_close_position_tercile"] = tc.groupby("clq").apply(summ, sign=-1)
    out["cases_by_weekday"] = tc.groupby("wd").apply(summ, sign=-1)
    out["cases_by_year"] = tc.groupby("year").apply(summ, sign=-1)
    out["cases_by_coin"] = tc.groupby("coin").apply(summ, sign=-1)
    # weekday effect overall by trend
    out["all_weekday_x_falling"] = D[D.trend == "falling"].groupby("wd").apply(summ)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"]).book_return.mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "std", "min", "max"])
    return out
