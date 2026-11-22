import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars, days = data["bars"], data["days"]
    coins = list(bars.keys())
    # --- combined book daily returns, chained in window order
    rows = []
    for c in coins:
        for w, d in days[c].items():
            d = d.reset_index(drop=True)
            rows.append(pd.DataFrame({"coin": c, "w": w, "wi": int(w[1:]), "di": np.arange(len(d)),
                                      "br": d["book_return"].values, "cr": d["coin_return"].values}))
    D = pd.concat(rows)
    B = D.groupby(["wi", "di"]).agg(br=("br", "mean"), cr=("cr", "mean")).dropna().sort_index()
    eq = (1 + B["br"]).cumprod()
    dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    out["deepest_fall"] = float(dd.min())
    yr = eq.iloc[-1] ** (365 / len(B)) - 1
    out["yearly_return"] = float(yr)
    # drawdown episode: from peak to trough
    trough = dd.idxmin()
    peak = eq.loc[:trough].idxmax()
    out["fall_peak_window_dayidx"] = str(peak)
    out["fall_trough_window_dayidx"] = str(trough)
    ep = B.loc[peak:trough]
    out["fall_length_days"] = len(ep)
    out["fall_windows"] = str(sorted(set(ep.index.get_level_values(0))))
    out["fall_coin_cum_return_during"] = float((1 + ep["cr"]).prod() - 1)
    # per window book vs coin
    pw = D.groupby("wi").agg(book=("br", "sum"), coin=("cr", "sum")).round(4)
    pw["window_maxdd"] = B.groupby(level=0)["dd"].min().round(4)
    out["per_window"] = pw
    # per coin contribution during fall
    epD = D.set_index(["wi", "di"]).loc[lambda x: x.index.isin(ep.index)]
    out["fall_by_coin"] = epD.groupby("coin").agg(book=("br", "sum"), coin=("cr", "sum")).round(4)

    # --- trades features at entry
    feats = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; lr = np.log(cl).diff()
            r180 = cl / cl.shift(180) - 1
            r42 = cl / cl.shift(42) - 1
            v42 = lr.rolling(42).std(); v360 = lr.rolling(360).std()
            rng6 = b["high"].rolling(6).max() / b["low"].rolling(6).min() - 1
            rm = rng6 / rng6.rolling(180).mean()
            fwd = cl.shift(-84) / cl - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            prev = a.shift(1).fillna(0)
            ent = (a > 0) & (prev <= 0)
            # position gain per bar
            g = a * (cl.shift(-1) / cl - 1)
            idx = np.where(ent)[0]
            for i in idx:
                # gain until allocation returns to 0
                j = i
                while j < len(a) and a.iloc[j] > 0: j += 1
                feats.append(dict(coin=c, wi=int(w[1:]), r180=r180[i], r42=r42[i], vr=v42[i] / v360[i] if v360[i] else np.nan,
                                  rm=rm[i], fwd=fwd[i], gain=g.iloc[i:j].sum(), hold=j - i, alloc=a.iloc[i]))
    F = pd.DataFrame(feats)
    out["n_entries"] = len(F)
    out["entry_summary"] = F[["r180", "r42", "vr", "rm", "fwd", "gain", "hold", "alloc"]].describe().round(4)
    res = {}
    for col in ["r180", "r42", "vr", "rm"]:
        G = F.dropna(subset=[col, "gain"])
        q = pd.qcut(G[col], 4, labels=False, duplicates="drop")
        t = G.groupby(q).agg(lo=(col, "min"), hi=(col, "max"), n=("gain", "size"), gain=("gain", "mean"),
                              worst=("gain", "min"), fwd=("fwd", "mean"))
        t.index = [f"{col}_q{i}" for i in t.index]
        res[col] = t.round(4)
    out["by_r180"] = res["r180"]; out["by_r42"] = res["r42"]; out["by_vr"] = res["vr"]; out["by_rm"] = res["rm"]
    # worst 20 trades features
    out["worst20_means"] = F.nsmallest(20, "gain")[["r180", "r42", "vr", "rm", "fwd", "gain", "hold"]].mean().round(4)
    out["all_means"] = F[["r180", "r42", "vr", "rm", "fwd", "gain", "hold"]].mean().round(4)
    return out
