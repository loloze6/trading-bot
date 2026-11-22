def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    drift = {}
    usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].fillna(0).values
            s = np.where(f < 0, -f, 0.0)
            raw = df.get("debug_info.components.bounce_near_low.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            low = None; used = set()
            for t in range(len(df)):
                if s[t] <= 0:
                    low = None; continue
                if low is None:
                    low = 0.0
                if s[t] - low >= 2:
                    cell = t // 5
                    if cell not in used:
                        used.add(cell)
                        rec = dict(coin=c, win=w, year=yr[t], fc=s[t], raw=raw[t], r1=r1[t])
                        for h in H:
                            if t + h < len(cl):
                                ret = cl[t + h] / cl[t] - 1
                                rec[f"u{h}"] = -(ret - drift[(c, h)])
                                rec[f"tot{h}"] = -ret
                                rec[f"s{h}"] = rec[f"u{h}"] / usual[(c, h)]
                    low = s[t]
                else:
                    low = min(low, s[t])
    d = pd.DataFrame(rows if False else [])
    d = pd.DataFrame(rec_list) if False else None
    return {}
