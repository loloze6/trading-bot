def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s: int(s[1:]))
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values; f = b.forecast.values; al = b.postRebalance_current_allocation.values
            s = pd.Series(cl)
            nxt = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            ma50 = s.rolling(50, min_periods=30).mean().values
            ma100 = s.rolling(100, min_periods=50).mean().values
            r20 = (s / s.shift(20) - 1).values
            since = np.full(len(b), np.nan); last = -10**9
            for i in range(len(b)):
                if f[i] > 0: last = i
                since[i] = i - last if last > -10**8 else 999
            for i in range(len(b) - 1):
                recs.append(dict(coin=c, win=w, i=i, f=f[i], al=al[i], nxt=nxt[i],
                                 a50=cl[i] > ma50[i] if not np.isnan(ma50[i]) else False,
                                 a100=cl[i] > ma100[i] if not np.isnan(ma100[i]) else False,
                                 r20p=r20[i] > 0 if not np.isnan(r20[i]) else False, since=since[i]))
    B = pd.DataFrame(recs)
    B["chg"] = B.groupby(["coin", "win"]).al.diff().abs().fillna(B.al.abs())
    cost = 0.0019 / 2
    def book(mask, name):
        a = np.where(mask, B.al, 0.0)
        tmp = B[["coin", "win", "i", "nxt"]].copy(); tmp["a"] = a
        tmp["chg"] = tmp.groupby(["coin", "win"]).a.diff().abs().fillna(tmp.a.abs())
        tmp["g"] = tmp.a * tmp.nxt - tmp.chg * cost
        d = tmp.groupby(["win", "i"]).g.mean().reset_index()
        d["wn"] = d.win.str[1:].astype(int); d = d.sort_values(["wn", "i"])
        v = (1 + d.g).cumprod(); mdd = float((v / v.cummax() - 1).min())
        yrs = len(d) / 365; yr = float(v.iloc[-1] ** (1 / yrs) - 1)
        sh = d.g.mean() / d.g.std() * np.sqrt(365)
        return dict(variant=name, yearly=yr, maxdd=mdd, calmar=yr / abs(mdd), sharpe=sh, exposure=float((tmp.a > 0).mean()))
    rows = [book(np.ones(len(B), bool), "as_is"),
            book(B.a50.values, "only_above_ma50"),
            book(B.a100.values, "only_above_ma100"),
            book(B.r20p.values, "only_r20_pos"),
            book((B.since <= 5).values, "held_5_after_signal"),
            book(((B.since <= 10) & B.a50).values, "held10_and_above50"),
            book(((B.since <= 5) & B.a50).values, "held5_and_above50"),
            book(((B.since <= 10) & B.a100).values, "held10_and_above100")]
    out["variants"] = pd.DataFrame(rows)
    # condition-alone check: holding coin (alloc 1) on above-ma50 bars without signal within 10 vs with
    B["sigwin"] = B.since <= 10
    out["cond_check_nxt"] = B.groupby(["a50", "sigwin"]).nxt.agg(["mean", "count"])
    out["cond_check_nxt100"] = B.groupby(["a100", "sigwin"]).nxt.agg(["mean", "count"])
    return out
