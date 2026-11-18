import pandas as pd, numpy as np

def explore(data):
    out = {}
    allb = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1)/b["close"] - 1
            b["ret1"] = b["close"].pct_change()
            b["mad60"] = b["ret1"].abs().rolling(60, min_periods=20).mean()
            b["fz"] = -b["ret1"]/b["mad60"]
            sd20 = b["ret1"].rolling(20).std()
            b["vr"] = sd20/sd20.rolling(100, min_periods=40).mean()
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["nxt"]
            b["coin"]=coin; b["win"]=w
            b["inreg"] = b["regime"]=="mean_reversion"
            b["fc"] = b["forecast"]
            allb.append(b)
    B = pd.concat(allb)
    # book drawdowns: chained daily per coin in window order
    dd_rows = []
    for coin in data["days"]:
        ws = sorted(data["days"][coin].keys(), key=lambda x:int(x[1:]))
        r = pd.concat([data["days"][coin][w].assign(win=w) for w in ws])
        r = r.dropna(subset=["book_return"])
        eq = (1+r["book_return"]).cumprod().values
        peak = np.maximum.accumulate(eq)
        dd = eq/peak-1
        i = dd.argmin(); j = eq[:i+1].argmax()
        seg = r.iloc[j:i+1]
        dd_rows.append(dict(coin=coin, maxdd=dd.min(), days=i-j, win_start=seg["win"].iloc[0], win_end=seg["win"].iloc[-1],
                            coin_ret_sum=seg["coin_return"].sum(), book_sum=seg["book_return"].sum()))
        # per-window book loss share
    out["deepest_dd"] = pd.DataFrame(dd_rows)
    # within active bars: losing contributions by condition
    act = B[B["pos"].abs()>1e-6].dropna(subset=["nxt"]).copy()
    act["fresh"] = act["fc"]>0
    g = act.groupby("fresh")
    out["fresh_vs_carry"] = pd.DataFrame({"n":g.size(),"pos":g["pos"].mean(),"gain_mean":g["gain"].mean(),"gain_sum":g["gain"].sum(),"nxt":g["nxt"].mean()})
    # falls (fz>1) in regime: graded by vr tercile x fz
    F = B[(B["fz"]>1)].dropna(subset=["nxt","vr"]).copy()
    F["vrb"] = pd.qcut(F["vr"],3,labels=["lo","mid","hi"])
    F["fzb"] = pd.cut(F["fz"],[1,1.5,2.5,np.inf])
    g = F.groupby(["vrb","fzb"])
    out["falls_vr_x_fz"] = pd.DataFrame({"n":g.size(),"nxt":g["nxt"].mean(),"t":g["nxt"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan)})
    # falls by trend
    F2 = F.dropna(subset=["ret20"]).copy()
    F2["trb"] = pd.qcut(F2["ret20"],3,labels=["down","flat","up"])
    g = F2.groupby(["vrb","trb"])
    out["falls_vr_x_trend"] = g["nxt"].agg(["size","mean"])
    # cost: fee per active bar vs gain
    B["fee"] = B["total_portfolio_value"]-B["postRebalance_total_value"]
    B["feer"] = B["fee"]/B["total_portfolio_value"]
    out["fee_vs_gain"] = pd.Series({"fee_per_bar":B["feer"].mean(),"gain_per_bar":B["gain"].mean()})
    # gain by vr in regime fresh signals
    fr = act[act["fresh"]].copy()
    fr["vrb"] = pd.qcut(fr["vr"],4)
    g = fr.groupby("vrb")
    out["fresh_by_vr"] = pd.DataFrame({"n":g.size(),"nxt":g["nxt"].mean(),"gain":g["gain"].mean(),"fz":g["fz"].mean()})
    return out
