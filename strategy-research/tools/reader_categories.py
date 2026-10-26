"""The reader categories, as a plain constant (D-197).

The campaign's proposals directory (artifacts/proposals/<category>.yaml) has had five files
per run since the five specialist readers: profitability, trade_efficiency, forecast_power,
regime_power, component_attribution. Since E-075 PR-5 (D-092) the analyst's two lenses write
two of them (lens `forecast` -> forecast_power.yaml, lens `trade_efficiency` ->
trade_efficiency.yaml); the other three exist only in an old run's directory as readers' files
(D-198 deleted the five readers, the report builder tools/build_reports.py and the code that
wrote them as `replaced_by_analyst` readings).

This module is the one list every loader and writer shares:

  ANALYST_LENS_CATEGORIES   the two categories the analyst's lenses write.
  LEGACY_READER_CATEGORIES  the three old names. Kept only so that load_proposals,
                            decide_next.load_inputs, campaign_memory and fold_confirm still
                            load an old run's five proposal files; no new run needs them.
  READER_CATEGORIES         all five, in the order the old report builder listed them.

Plain lists: never mutate them; copy with list(...) first.
"""
from __future__ import annotations

READER_CATEGORIES = ["profitability", "trade_efficiency", "forecast_power", "regime_power",
                     "component_attribution"]

ANALYST_LENS_CATEGORIES = ["trade_efficiency", "forecast_power"]

LEGACY_READER_CATEGORIES = ["profitability", "regime_power", "component_attribution"]
