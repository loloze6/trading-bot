def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    out["top_keys"] = ", ".join([str(k) + ":" + type(v).__name__ for k, v in data.items()]) if hasattr(data, "items") else type(data).__name__
    inv = []
    for name in ["bars", "days", "trades"]:
        t = data.get(name, None) if hasattr(data, "get") else None
        if t is None:
            inv.append({"table": name, "coin": "-", "window": "-", "rows": -1, "cols": "missing"})
            continue
        if isinstance(t, pd.DataFrame):
            inv.append({"table": name, "coin": "flat", "window": "-", "rows": len(t), "cols": ",".join(map(str, t.columns[:15]))})
            continue
        if len(t) == 0:
            inv.append({"table": name, "coin": "-", "window": "-", "rows": 0, "cols": "empty dict"})
        for c in t:
            sub = t[c]
            if isinstance(sub, pd.DataFrame):
                inv.append({"table": name, "coin": c, "window": "flat", "rows": len(sub), "cols": ",".join(map(str, sub.columns[:15]))})
                continue
            for w in sub:
                d = sub[w]
                inv.append({"table": name, "coin": c, "window": w,
                            "rows": len(d) if hasattr(d, "__len__") else -1,
                            "cols": ",".join(map(str, getattr(d, "columns", [])[:12]))})
    out["inventory"] = pd.DataFrame(inv).head(40)
    out["n_entries"] = len(inv)
    # if days exist, compute the pattern from daily closes
    days = data.get("days", {}) if hasattr(data, "get") else {}
    rows = []; allret = []
    H = 5
    try:
        for c in days:
            for w in days[c]:
                d = days[c][w]
                if not isinstance(d, pd.DataFrame) or "close" not in d.columns or len(d) < 70:
                    continue
                cl = d["close"].astype(float).reset_index(drop=True)
                r = cl.pct_change()
                z = r / r.rolling(30).std().shift(1)
                tr60 = cl / cl.shift(60) - 1
                vol30 = r.rolling(30).std()
                vr = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
                fwd = cl.shift(-H) / cl - 1
                for i in range(0, len(cl) - H, H):
                    allret.append({"coin": c, "fwd": fwd[i]})
                df = pd.DataFrame({"coin": c, "i": np.arange(len(cl)), "z": z, "tr60": tr60, "vr": vr, "fwd": fwd,
                                   "br": d["book_return"].reset_index(drop=True) if "book_return" in d.columns else np.nan})
                rows.append(df[df.i % H == 0])
        if rows:
            A = pd.concat(rows).dropna(subset=["z", "fwd"])
            drift = pd.DataFrame(allret).dropna().groupby("coin")["fwd"].mean()
            A["unus"] = A.fwd - A.coin.map(drift)
            A["agit"] = np.where(A.vr.isna(), "na", np.where(A.vr > 0.5, "agitated", "calm"))
            A["trend"] = np.where(A.tr60 > .1, "rising", np.where(A.tr60 < -.1, "falling", "choppy"))
            def summ(g):
                x = g["unus"].dropna()
                return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                                  "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
            A["zbin"] = pd.cut(A.z, [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
            out["by_zbin_agit"] = A.groupby(["agit", "zbin"]).apply(summ)
            out["by_zbin_trend"] = A.groupby(["trend", "zbin"]).apply(summ)
    except Exception as e:
        out["error"] = str(e)[:200]
    return out
