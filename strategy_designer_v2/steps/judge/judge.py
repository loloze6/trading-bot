"""Branch 1 (was the idea right?), computed only from the engine's own output files; never opens the price cache.
Usage: python3 steps/judge/judge.py <engine_dir> <claims.yaml> <claim_id>
Measure: Spearman rank correlation (Pearson of ranks) of the engine's `forecast` and the forward return over
horizon_bars, on event bars. Windows are W1..W6, never dates."""
import sys, pathlib, datetime as dt
import numpy as np, pandas as pd, yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
LEDGER = ROOT / "strategy_designer_v2" / "records" / "trials.yaml"
MIN_EVENTS, AGREE = 30, 5   # VERDICT RULES (written once): pass iff fold_ic >= min_effect AND same sign as the fold in >= AGREE
                            # windows (all but one, at least 1, when fewer than 6) AND pooled event bars >= MIN_EVENTS;
                            # refused if any window's bars.csv lacks the forecast or the event column. t_stat is information only.


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3: return float("nan")
    rx, ry = pd.Series(x).rank().to_numpy(), pd.Series(y).rank().to_numpy()   # average ranks for ties
    return float("nan") if rx.std() == 0 or ry.std() == 0 else float(np.corrcoef(rx, ry)[0, 1])


def judge_engine_run(engine_dir, claims_path, claim_id):
    engine_dir = pathlib.Path(engine_dir).resolve()
    idea = next(i for i in yaml.safe_load(pathlib.Path(claims_path).read_text())["ideas"] if i["id"] == claim_id)
    h, min_effect = int(idea["claim"]["horizon_bars"]), float(idea["claim"]["min_effect"])
    ev = yaml.safe_load((engine_dir / "engine_verdict.yaml").read_text())
    col = f"debug_info.components.{claim_id}.event"
    rows, pooled_f, pooled_r, all_f, all_r, missing = [], [], [], [], [], []
    for w in ev["full_size"]["windows"]:
        d = pd.read_csv(ROOT / w["run_dir"] / "bars.csv")
        if "forecast" not in d.columns or col not in d.columns:
            missing.append(w["window"]); continue
        fwd = d["close"].shift(-h) / d["close"] - 1          # within the window only; the last h bars get NaN and drop
        ok = fwd.notna() & d["forecast"].notna()
        on = ok & (d[col].fillna(0).astype(float) > 0)
        all_f += list(d.loc[ok, "forecast"]); all_r += list(fwd[ok])
        pooled_f += list(d.loc[on, "forecast"]); pooled_r += list(fwd[on])
        rows.append({"window": w["window"], "n_event": int(on.sum()), "ic_event": spearman(d.loc[on, "forecast"], fwd[on]),
                     "ic_all": spearman(d.loc[ok, "forecast"], fwd[ok])})
    out = {"claim": claim_id, "fold": ev["fold"], "symbol": ev["symbol"], "horizon_bars": h, "min_effect": min_effect}
    if missing:
        out.update(verdict="refused", why=f"forecast or event column missing in {missing}", windows=rows)
    else:
        n, r = len(pooled_f), spearman(pooled_f, pooled_r)
        sign = np.sign(r) if r == r else 0
        need = AGREE if len(rows) >= 6 else max(len(rows) - 1, 1)
        same = sum(1 for x in rows if x["ic_event"] == x["ic_event"] and sign != 0 and np.sign(x["ic_event"]) == sign)
        checks = {f"fold_ic_ge_min_effect_{min_effect}": bool(r == r and r >= min_effect),
                  f"same_sign_in_{need}_of_{len(rows)}_windows": bool(same >= need),
                  f"pooled_events_ge_{MIN_EVENTS}": bool(n >= MIN_EVENTS)}
        t = float(r * np.sqrt((n - 2) / (1 - r * r))) if n > 2 and r == r and abs(r) < 1 else None
        out.update(windows=rows, fold_totals={"n_event": n, "ic_event": r, "windows_same_sign": same, "windows": len(rows),
                   "ic_all": spearman(all_f, all_r)}, checks=checks, verdict="pass" if all(checks.values()) else "fail", t_stat=t)
        if len(rows) < 6: out["note"] = f"only {len(rows)} window(s): same-sign check needs {need}"
    out = yaml.safe_load(yaml.safe_dump(out))   # plain floats, NaN kept
    (engine_dir / "judge_verdict.yaml").write_text(yaml.safe_dump(out, sort_keys=False))
    for x in rows: print(f"  {x['window']}: n_event={x['n_event']} ic_event={x['ic_event']:+.4f} ic_all={x['ic_all']:+.4f}")
    ft = out.get("fold_totals", {})
    print(f"{claim_id} {out['symbol']}: judge {out['verdict']}" + (f"  fold_ic={ft['ic_event']:+.4f} n_event={ft['n_event']} t={out['t_stat']:.2f} checks={out['checks']}" if ft else f" ({out['why']})")
          + (f"  NOTE {out['note']}" if out.get("note") else ""))
    led = yaml.safe_load(LEDGER.read_text()); led["trials"].append(
        {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "try": "judge", "claim": claim_id, "symbols": [out["symbol"]],
         "bar_size": ev.get("bar_size"), "fold": out["fold"], "verdict": f"judge:{out['verdict']}", "windows": len(rows)})
    LEDGER.write_text(yaml.safe_dump(led, sort_keys=False))
    return out


if __name__ == "__main__":
    judge_engine_run(*sys.argv[1:4])
