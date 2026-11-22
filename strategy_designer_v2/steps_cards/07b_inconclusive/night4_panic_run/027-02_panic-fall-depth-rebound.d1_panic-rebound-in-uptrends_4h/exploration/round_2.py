import pandas as pd, numpy as np
from scipy import stats

def _raw(v):
    try:
        if isinstance(v, str):
            import json
            v = json.loads(v)
        if isinstance(v, dict):
            p = v.get("panic_buy", v)
            if isinstance(p, dict):
                return p.get("last_history_value", np.nan), p.get("post_pipeline_value", np.nan)
    except Exception:
        pass
    return np.nan, np.nan

def explore(data):
    bars = data["bars"]
    drift = {}
    for H in (18, 42, 84):
        for coin, ws in bars.items():
            r = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                r += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = (np.mean(r), np.std(r))
    rows = []
    sample_type = None
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            f = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            rng = (df["high"] - df["low"]) / df["close"]
            ratio = (rng.rolling(180).mean() / rng.rolling(6).mean()).values
            r6 = (df["close"] / df["close"].shift(6) - 1)
            fall_z = (-r6 / r6.abs().rolling(180).mean()).values
            comp = df["debug_info.components"] if "debug_info.components" in df else None
            if sample_type is None and comp is not None:
                nz = comp.dropna()
                if len(nz): sample_type = type(nz.iloc[0]).__name__
            prev = np.r_[0, f[:-1]]
            sig = (f >= 2) & (prev < 2)
            cell = np.arange(n) // 84
            seen = set()
            for i in np.where(sig)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                rawv, postv = _raw(comp.iloc[i]) if comp is not None else (np.nan, np.nan)
                rec = dict(coin=coin, w=w, year=yr[i], raw=rawv, post=postv,
                           fall=fall_z[i], ratio=ratio[i])
                for H in (18, 42, 84):
                    if i + H < n:
                        m, s = drift[(coin, H)]
                        rec[f"u{H}"] = c[i + H] / c[i] - 1 - m
                        rec[f"s{H}"] = rec[f"u{H}"] / s
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u84"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              hit=(x > 0).mean()))
    out = {}
    out["component cell type"] = str(sample_type)
    out["raw component describe"] = d["raw"].describe()
    out["by horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in (18, 42, 84)}).T
    out["strength by horizon"] = pd.DataFrame({h: summ(d, f"s{h}") for h in (18, 42, 84)}).T
    out["u42 by year"] = d.groupby("year").apply(lambda g: summ(g, "u42"))
    out["u42 by coin"] = d.groupby("coin").apply(lambda g: summ(g, "u42"))
    dd = d.dropna(subset=["raw"])
    if len(dd) > 10:
        dd = dd.assign(rq=pd.qcut(dd.raw.rank(method="first"), 2, labels=["lower", "upper"]))
        out["by raw half u84"] = dd.groupby("rq").apply(summ)
        out["by raw half u42"] = dd.groupby("rq").apply(lambda g: summ(g, "u42"))
        out["spearman raw vs u84/u42"] = pd.Series({
            "u84": stats.spearmanr(dd.raw, dd.u84, nan_policy="omit")[0],
            "u42": stats.spearmanr(dd.raw, dd.u42, nan_policy="omit")[0]})
    df2 = d.dropna(subset=["fall"])
    df2 = df2.assign(fq=pd.qcut(df2.fall.rank(method="first"), 2, labels=["shallower", "deeper"]))
    out["bets by fall half u84"] = df2.groupby("fq").apply(summ)
    out["bets by fall half u42"] = df2.groupby("fq").apply(lambda g: summ(g, "u42"))
    out["bets excl 2018 u84"] = summ(d[d.year != 2018]).to_frame().T
    out["bets excl 2018 u42"] = summ(d[d.year != 2018], "u42").to_frame().T
    return out
