import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["dur_h"] = T["duration_minutes"] / 60
    T["dbin"] = pd.cut(T["dur_h"], [-1, 0.5, 1.5, 47.5, 48.5, 200, 1e6], labels=["0h", "1h", "2-47h", "48h", "49-200h", ">200h"])
    out["trades_by_dur"] = T.groupby("dbin").agg(n=("side", "size"), pnl=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), pnl_sum=("profit_loss_percent", "sum"), comm=("total_commission", "mean"),
        entry_fc=("entry_forecast", "mean"), exit_fc=("exit_forecast", "mean"))
    T["exit_wd"] = pd.to_datetime(T["exit_time"]).dt.weekday
    out["exit_wd_of_long_trades"] = T[T.dur_h > 48.5].groupby("exit_wd").size()
    rows = []
    days = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"] * b["r1"]
            b["fee"] = b["total_portfolio_value"] - b["postRebalance_total_value"]
            b["feer"] = b["fee"] / b["total_portfolio_value"]
            b["chg"] = (b["pos"] - b["previous_allocation"]).abs()
            b["traded"] = b["chg"] > 1e-9
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday
            b["hsince"] = ((ts - ts.dt.normalize()) / pd.Timedelta(hours=1)) + 24 * ((ts.dt.weekday + 1) % 7)  # hours since Sunday 00:00
            b["coin"] = c; b["win"] = w
            # case gain: Mon-Tue hold window after a signal
            sig = np.where(b["forecast"].values != 0)[0]
            for i in sig:
                seg = b.iloc[i:i + 48]
                rest = b.iloc[i + 48:i + 168]
                days.append({"coin": c, "fc": b["forecast"].iat[i], "pos0": b["pos"].iat[i],
                             "g48": seg["g"].sum(), "fee48": seg["feer"].sum(), "ntr48": int(seg["traded"].sum()),
                             "g_after": rest["g"].sum(), "fee_after": rest["feer"].sum(), "pos_end": b["pos"].iat[min(i + 48, len(b) - 1)],
                             "ret48": b["close"].iat[min(i + 48, len(b) - 1)] / b["close"].iat[i] - 1})
            rows.append(b[["coin", "wd", "pos", "g", "feer", "traded", "chg"]])
    B = pd.concat(rows, ignore_index=True)
    out["by_wd_fee_trades"] = B.groupby("wd").agg(gain_sum=("g", "sum"), fee_sum=("feer", "sum"), n_traded=("traded", "sum"),
        turnover=("chg", "sum"), inpos=("pos", lambda p: (p.abs() > 1e-9).mean()))
    D = pd.DataFrame(days)
    out["cases_summary"] = D[["g48", "fee48", "ntr48", "g_after", "fee_after", "pos0", "ret48"]].describe().T[["count", "mean", "50%"]]
    out["share_pos_left_after48"] = float((D["pos_end"].abs() > 1e-9).mean())
    out["t_g48"] = float(D["g48"].mean() / (D["g48"].std() / np.sqrt(len(D))))
    out["t_g_after"] = float(D["g_after"].mean() / (D["g_after"].std() / np.sqrt(len(D))))
    D["q"] = pd.qcut(D["fc"].abs(), 4, labels=False)
    out["cases_by_fc_quart"] = D.groupby("q").agg(n=("fc", "size"), fc=("fc", "mean"), ret48=("ret48", "mean"),
        g48=("g48", "mean"), fee48=("fee48", "mean"), g_after=("g_after", "mean"))
    out["cases_by_coin"] = D.groupby("coin").agg(n=("fc", "size"), ret48=("ret48", "mean"), g48=("g48", "mean"),
        fee48=("fee48", "mean"), g_after=("g_after", "mean"), left=("pos_end", lambda p: (p.abs() > 1e-9).mean()))
    return out
