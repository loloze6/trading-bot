import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (12, 24, 48, 72, 120)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        usual[coin] = {h: np.std(v) for h, v in allr.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            v = df["volume"].values
            n = len(df)
            # event bars: Sunday 23:00 (weekend) and Wednesday 23:00 (weekday control: Tue-Wed move)
            for t in range(n):
                tt = ts.iloc[t]
                if tt.hour != 23 or tt.weekday() not in (6, 2):
                    continue
                if t < 167:
                    continue
                past = c[t] / c[t - 48] - 1
                vr = np.log(np.mean(v[t - 47:t + 1]) / max(np.mean(v[t - 167:t - 47]), 1e-12))
                rec = dict(coin=coin, win=w, year=tt.year, kind="wkend" if tt.weekday() == 6 else "midwk",
                           past=past, past_z=past / usual[coin][48], lvr=vr,
                           fc=df["forecast"].iloc[t])
                for h in (12, 24, 48, 72, 120):
                    if t + h < n:
                        r = c[t + h] / c[t] - 1
                        rec[f"u{h}"] = (r - drift[coin][h]) / usual[coin][h]
                    else:
                        rec[f"u{h}"] = np.nan
                rows.append(rec)
    E = pd.DataFrame(rows)
    E["dirn"] = -np.sign(E["past"])
    for h in (12, 24, 48, 72, 120):
        E[f"s{h}"] = E[f"u{h}"] * E["dirn"]  # strength in reversal direction

    def summ(g):
        out = {"n": len(g)}
        for h in (12, 24, 48, 72, 120):
            s = g[f"s{h}"].dropna()
            out[f"str{h}"] = s.mean()
            out[f"t{h}"] = s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
        # graded: slope of u48 on -past_z
        gg = g.dropna(subset=["u48"])
        if len(gg) > 5:
            sl = stats.linregress(-gg["past_z"], gg["u48"])
            out["slope48_t"] = sl.slope / sl.stderr
        return pd.Series(out)

    E["thin"] = np.where(E["lvr"] < 0, "thin", "heavy")
    res = {}
    res["kind_x_thin"] = E.groupby(["kind", "thin"]).apply(summ)
    W = E[E.kind == "wkend"].copy()
    W["mq"] = pd.qcut(W["past_z"].abs(), 4, labels=["q1", "q2", "q3", "q4"])
    res["wkend_by_move_size"] = W.groupby("mq").apply(summ)
    W["vq"] = pd.qcut(W["lvr"], 4, labels=["v1thin", "v2", "v3", "v4heavy"])
    res["wkend_by_vol_ratio"] = W.groupby("vq").apply(summ)
    W["side"] = np.where(W["past"] > 0, "up_wkend", "down_wkend")
    res["wkend_by_side"] = W.groupby("side").apply(summ)
    res["wkend_by_coin"] = W.groupby("coin").apply(summ)
    res["wkend_by_year"] = W.groupby("year").apply(summ)
    M = E[E.kind == "midwk"].copy()
    M["mq"] = pd.qcut(M["past_z"].abs(), 4, labels=["q1", "q2", "q3", "q4"])
    res["midwk_by_move_size"] = M.groupby("mq").apply(summ)
    return res
