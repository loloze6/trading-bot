def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s: int(s[1:]))
    # per-bar attribution: gain on bar t = alloc after trade t * next return
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values; f = b.forecast.values; al = b.postRebalance_current_allocation.values
            s = pd.Series(cl)
            nxt = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            ma50 = s.rolling(50, min_periods=30).mean().values
            r20 = (s / s.shift(20) - 1).values
            # bars since last positive forecast
            since = np.full(len(b), np.nan); last = -10**9
            for i in range(len(b)):
                if f[i] > 0: last = i
                since[i] = i - last if last > -10**8 else np.nan
            vol = pd.Series(b.volume.values)
            lv = np.log(vol / vol.shift(1).rolling(20).mean()).values
            rng = (b.high - b.low).values
            clv = np.where(rng > 0, (cl - b.low.values) / np.where(rng > 0, rng, 1), np.nan)
            r1 = s.pct_change().values
            for i in range(len(b) - 1):
                recs.append(dict(coin=c, win=w, i=i, f=f[i], al=al[i], nxt=nxt[i], gain=al[i] * nxt[i],
                                 above=(cl[i] > ma50[i]) if not np.isnan(ma50[i]) else np.nan, r20=r20[i],
                                 since=since[i], lv=lv[i], clv=clv[i], r1=r1[i]))
    B = pd.DataFrame(recs)
    B["state"] = np.where(B.f > 0, "sig_now", np.where(B.since <= 10, "held_<=10_after", np.where(B.al > 0, "held_other", "flat")))
    out["gain_by_state"] = B.groupby("state").agg(share_bars=("gain", "size"), mean_alloc=("al", "mean"),
                                                   mean_gain=("gain", "mean"), mean_nxt=("nxt", "mean"),
                                                   sum_gain=("gain", "sum"))
    out["gain_by_state_trend"] = B.dropna(subset=["above"]).groupby(["above", "state"]).agg(
        mean_alloc=("al", "mean"), mean_gain=("gain", "mean"), mean_nxt=("nxt", "mean"), n=("gain", "size"), sum_gain=("gain", "sum"))
    # grid with forecast buckets and trend / clv / day sign; horizon 10 and 20
    G = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b.close.values; f = b.forecast.values
            s = pd.Series(cl); ma50 = s.rolling(50, min_periods=30).mean().values
            vol = pd.Series(b.volume.values); lv = np.log(vol / vol.shift(1).rolling(20).mean()).values
            r1 = s.pct_change().values
            rng = (b.high - b.low).values
            clv = np.where(rng > 0, (cl - b.low.values) / np.where(rng > 0, rng, 1), np.nan)
            for H in (10, 20):
                for t in range(0, len(b) - H, H):
                    G.append(dict(H=H, coin=c, f=f[t], lv=lv[t], fwd=cl[t + H] / cl[t] - 1,
                                  above=(cl[t] > ma50[t]) if not np.isnan(ma50[t]) else np.nan, r1=r1[t], clv=clv[t]))
    G = pd.DataFrame(G)
    G["ex"] = G.fwd - G.groupby(["H", "coin"]).fwd.transform("mean")
    G["fb"] = pd.cut(G.f, [-1, 0, 0.5, 1.0, 1.5, 100], labels=["0", "0-0.5", "0.5-1", "1-1.5", ">1.5"])
    def tt(s): return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    out["grid_by_fbucket"] = G.groupby(["H", "fb"]).agg(mean_fwd=("fwd", "mean"), mean_ex=("ex", "mean"),
                                                       t_ex=("ex", tt), n=("ex", "size"))
    g2 = G.dropna(subset=["above"])
    out["grid_trend_x_sig"] = g2.groupby(["H", "above", G.f > 0]).agg(mean_fwd=("fwd", "mean"), mean_ex=("ex", "mean"),
                                                                  t=("ex", tt), n=("ex", "size"))
    g3 = G.dropna(subset=["r1"])
    out["grid_daysign_x_fb"] = g3[g3.H == 10].groupby([g3.r1 > 0, "fb"]).agg(mean_ex=("ex", "mean"), t=("ex", tt), n=("ex", "size"))
    # book daily in falls: share of exposure from signal now vs held
    return out
