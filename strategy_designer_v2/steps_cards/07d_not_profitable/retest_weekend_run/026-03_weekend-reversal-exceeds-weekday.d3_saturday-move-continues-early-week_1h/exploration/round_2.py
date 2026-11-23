def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    cr = []; gen = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            vol30 = r1.rolling(720, min_periods=200).std().values
            nxt = ts + pd.Timedelta(hours=1)
            mid = np.where((nxt.dt.hour.values == 0))[0]
            for i in mid:
                if i < 48 or i + 48 >= len(b): continue
                fwd = cl[i + 48] / cl[i] - 1
                prev = cl[i] / cl[i - 24] - 1
                prev2 = cl[i - 24] / cl[i - 48] - 1
                wd = nxt.iloc[i].weekday()
                gen.append(dict(coin=c, wd=wd, fwd=fwd, prev=prev, prev2=prev2, vol=vol30[i]))
                if wd == 0:
                    f = b["forecast"].iloc[i]
                    cr.append(dict(coin=c, wn=int(w[1:]), year=ts.iloc[i].year, f=f, fwd=fwd,
                                   alloc=b["postRebalance_current_allocation"].iloc[i],
                                   sat=prev2, sun=prev, vol=vol30[i]))
    C = pd.DataFrame(cr); G = pd.DataFrame(gen)
    C = C[C["f"] != 0].copy()
    C["s"] = np.sign(C["f"]); C["ex"] = C["s"] * C["fwd"]
    C["vq"] = C.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    C["fq"] = pd.qcut(C["f"].abs(), 5, labels=False, duplicates="drop")
    C["sunag"] = np.sign(C["sun"]) == C["s"]
    C["sun_z"] = -C["s"] * C["sun"] / (C["vol"] * np.sqrt(24))  # sunday's move against saturday, in usual moves
    def t(x): return x.mean() / x.std() * np.sqrt(len(x))
    # condition alone: fading the previous 24h at midnight, on every weekday, and on Mondays
    G["fade"] = -np.sign(G["prev"]) * G["fwd"]
    G["foll2"] = np.sign(G["prev2"]) * G["fwd"]
    out["fade_prev24_by_weekday"] = G.groupby("wd").agg(n=("fade", "size"), fade_mean=("fade", "mean"), fade_t=("fade", t),
                                                         follow_prev2_mean=("foll2", "mean"), follow_prev2_t=("foll2", t))
    # Sunday against Saturday: Saturday's side vs Sunday-fade side, separated
    M = G[G["wd"] == 0].copy()
    M["agree"] = np.sign(M["prev"]) == np.sign(M["prev2"])
    out["monday_split_sat_vs_sun"] = M.groupby("agree").agg(n=("fwd", "size"), follow_sat=("foll2", "mean"), t_sat=("foll2", t),
                                                           fade_sun=("fade", "mean"), t_fade=("fade", t))
    # graded: sunday counter-move size terciles
    C["szq"] = pd.qcut(C["sun_z"], 4, labels=False, duplicates="drop")
    out["by_sunday_against_quartile"] = C.groupby("szq").agg(n=("ex", "size"), mean=("ex", "mean"), t=("ex", t), sz=("sun_z", "mean"))
    # combined saturday+sunday-against: weekend's "net" vs saturday
    C["wk"] = np.sign(C["sat"] + C["sun"]) == C["s"]
    out["by_weekend_net_sign_agrees_sat"] = C.groupby("wk").agg(n=("ex", "size"), mean=("ex", "mean"), t=("ex", t))
    # vol: unsigned drift per tercile (condition alone)
    out["vol_tercile"] = C.groupby("vq").agg(n=("ex", "size"), signed=("ex", "mean"), t=("ex", t), unsigned_fwd=("fwd", "mean"))
    # variants book: weekly pnl net of cost, mean over coins, chained by window then time
    cost = 0.0019
    C["net"] = C["alloc"] * C["fwd"] - C["alloc"].abs() * cost
    C["wk_id"] = C["wn"] * 1000 + C.groupby("wn").cumcount() * 0  # placeholder
    def book(mask, name):
        x = C.copy(); x.loc[~mask, "net"] = 0.0
        # group by window and week ordinal inside window
        x["ord"] = x.groupby(["coin", "wn"]).cumcount()
        W = x.groupby(["wn", "ord"])["net"].sum() / 6.0
        W = W.sort_index()
        v = (1 + W).cumprod().values; dd = (v / np.maximum.accumulate(v) - 1).min()
        yr = v[-1] ** (52.0 / len(v)) - 1
        return dict(variant=name, weeks=len(v), share_traded=mask.mean(), yearly=yr, maxdd=dd, calmar=yr / -dd,
                    weekly_sharpe=W.mean() / W.std() * np.sqrt(52))
    rows = [book(C["s"] != 0, "all"), book(~C["sunag"], "sunday_against"), book(C["vq"] == 0, "low_vol"),
            book(C["vq"] <= 1, "low_mid_vol"), book(C["fq"] >= 3, "top2_quintiles"),
            book((~C["sunag"]) & (C["vq"] <= 1), "sun_against_lowmid"), book(C["s"] < 0, "short_only")]
    out["variants"] = pd.DataFrame(rows).set_index("variant")
    out["year_by_sunday"] = C.groupby(["year", "sunag"])["ex"].mean().unstack()
    return out
