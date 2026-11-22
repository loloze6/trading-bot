import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = {h: [] for h in (24, 48, 72)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h].extend(list(c[idx + h] / c[idx] - 1))
        drift = {h: np.mean(v) for h, v in allr.items()}
        usual = {h: np.std(v) for h, v in allr.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            v = df["volume"].values
            n = len(df)
            hrs = ts.dt.hour.values; wds = ts.dt.weekday.values
            for t in np.where((hrs == 23) & np.isin(wds, [6, 2]))[0]:
                if t < 167:
                    continue
                past = c[t] / c[t - 48] - 1
                vr = np.log(np.mean(v[t - 47:t + 1]) / max(np.mean(v[t - 167:t - 47]), 1e-12))
                rec = dict(coin=coin, win=w, year=ts.iloc[t].year,
                           kind="wkend" if wds[t] == 6 else "midwk",
                           past=past, past_z=past / usual[48], lvr=vr)
                for h in (24, 48, 72):
                    if t + h < n:
                        r = c[t + h] / c[t] - 1
                        rec[f"u{h}"] = (r - drift[h]) / usual[h]
                        rec[f"raw{h}"] = r - drift[h]
                        rec[f"tot{h}"] = r
                    else:
                        rec[f"u{h}"] = np.nan; rec[f"raw{h}"] = np.nan; rec[f"tot{h}"] = np.nan
                rows.append(rec)
    E = pd.DataFrame(rows)
    E["dirn"] = -np.sign(E["past"])
    for h in (24, 48, 72):
        E[f"s{h}"] = E[f"u{h}"] * E["dirn"]
    E["rawdir48"] = E["raw48"] * E["dirn"]
    E["totdir48"] = E["tot48"] * E["dirn"]

    def summ(g):
        out = {"n": len(g)}
        for h in (24, 48, 72):
            s = g[f"s{h}"].dropna()
            out[f"str{h}"] = s.mean()
            out[f"t{h}"] = s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
        out["unusual48_pct"] = 100 * g["rawdir48"].mean()
        out["total48_pct"] = 100 * g["totdir48"].mean()
        return pd.Series(out)

    res = {}
    W = E[E.kind == "wkend"].copy()
    M = E[E.kind == "midwk"].copy()
    W["vd"] = pd.qcut(W["lvr"], 8, labels=[f"o{i}" for i in range(1, 9)])
    res["wkend_by_vol_octile"] = W.groupby("vd").apply(summ)
    res["wkend_octile_edges_lvr"] = W.groupby("vd")["lvr"].agg(["min", "max", "mean"])
    # graded: s48 on -lvr (thinness), and interaction
    g = W.dropna(subset=["s48"])
    sl = stats.linregress(-g["lvr"], g["s48"])
    res["s48_on_thinness_slope_t"] = float(sl.slope / sl.stderr)
    # midweek control by its own volume quartile
    M["vq"] = pd.qcut(M["lvr"], 4, labels=["v1thin", "v2", "v3", "v4heavy"])
    res["midwk_by_vol_quartile"] = M.groupby("vq").apply(summ)
    # within thinnest weekend quartile
    q25 = W["lvr"].quantile(0.25)
    T = W[W["lvr"] <= q25].copy()
    res["thin_q1_by_year"] = T.groupby("year").apply(summ)
    res["thin_q1_by_coin"] = T.groupby("coin").apply(summ)
    T["side"] = np.where(T["past"] > 0, "up_wkend", "down_wkend")
    res["thin_q1_by_side"] = T.groupby("side").apply(summ)
    T["mq"] = pd.qcut(T["past_z"].abs(), 3, labels=["small", "mid", "large"])
    res["thin_q1_by_move_size"] = T.groupby("mq").apply(summ)
    # thin weekend: share of weekends with lvr<0
    res["share_wkend_lvr_lt0"] = float((W["lvr"] < 0).mean())
    res["share_midwk_lvr_lt0"] = float((M["lvr"] < 0).mean())
    return res
