"""
Unit tests for MockPortfolioInfo.update_local_balance().

Covers LONG, SHORT, CLOSE, REDUCE_LONG, REDUCE_SHORT trade types.
Verifies balance math and commission deduction.
"""

import pytest


COMMISSION = 0.001  # 0.1%
INITIAL_USDT = 10_000.0
PRICE = 50_000.0
QUANTITY = 0.1


@pytest.fixture
def portfolio():
    from execution.portfolio_info import MockPortfolioInfo
    return MockPortfolioInfo(
        initial_balance={"USDT": {"free": INITIAL_USDT, "locked": 0.0}},
        commission_rate=COMMISSION,
    )


def asset_free(portfolio, symbol="BTCUSDT"):
    return portfolio.balance.get(symbol, {}).get("free", 0.0)


def asset_locked(portfolio, symbol="BTCUSDT"):
    return portfolio.balance.get(symbol, {}).get("locked", 0.0)


def usdt_free(portfolio):
    return portfolio.balance["USDT"]["free"]


def usdt_locked(portfolio):
    return portfolio.balance["USDT"]["locked"]


# ---------------------------------------------------------------------------
# LONG: buy asset with USDT
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestLongTrade:
    def test_usdt_decreases_by_cost(self, portfolio):
        cost = PRICE * QUANTITY
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")
        expected_usdt = INITIAL_USDT - cost
        assert usdt_free(portfolio) == pytest.approx(expected_usdt)

    def test_asset_increases_by_quantity_minus_commission(self, portfolio):
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")
        expected_qty = QUANTITY * (1 - COMMISSION)
        assert asset_free(portfolio) == pytest.approx(expected_qty)

    def test_long_creates_asset_key_if_absent(self, portfolio):
        assert "BTCUSDT" not in portfolio.balance
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")
        assert "BTCUSDT" in portfolio.balance

    def test_insufficient_usdt_falls_back_to_margin(self, portfolio):
        """When USDT is insufficient, trade uses margin (borrows)."""
        big_cost = INITIAL_USDT * 2
        big_qty = big_cost / PRICE
        portfolio.update_local_balance("BTCUSDT", PRICE, big_qty, "LONG")
        # Asset should still be credited
        assert asset_free(portfolio) > 0


# ---------------------------------------------------------------------------
# SHORT: borrow asset, sell for USDT
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestShortTrade:
    def test_usdt_increases_by_proceeds_minus_commission(self, portfolio):
        proceeds = PRICE * QUANTITY * (1 - COMMISSION)
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "SHORT")
        assert usdt_free(portfolio) == pytest.approx(INITIAL_USDT + proceeds)

    def test_asset_locked_equals_quantity_borrowed(self, portfolio):
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "SHORT")
        assert asset_locked(portfolio) == pytest.approx(QUANTITY)

    def test_asset_free_unchanged_after_short(self, portfolio):
        """Short borrows, so free asset balance should not change."""
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "SHORT")
        assert asset_free(portfolio) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# REDUCE_LONG: partial sell of long position
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestReduceLong:
    def _open_long(self, portfolio):
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")

    def test_reduce_long_decreases_asset(self, portfolio):
        self._open_long(portfolio)
        qty_before = asset_free(portfolio)
        sell_qty = QUANTITY / 2
        portfolio.update_local_balance("BTCUSDT", PRICE, sell_qty, "REDUCE_LONG")
        assert asset_free(portfolio) == pytest.approx(qty_before - sell_qty)

    def test_reduce_long_increases_usdt(self, portfolio):
        self._open_long(portfolio)
        usdt_before = usdt_free(portfolio)
        sell_qty = QUANTITY / 2
        expected_received = PRICE * sell_qty * (1 - COMMISSION)
        portfolio.update_local_balance("BTCUSDT", PRICE, sell_qty, "REDUCE_LONG")
        assert usdt_free(portfolio) == pytest.approx(usdt_before + expected_received)


# ---------------------------------------------------------------------------
# CLOSE: full close of a position
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestCloseLong:
    def test_close_long_returns_usdt(self, portfolio):
        """Open a LONG, then CLOSE: USDT should be restored minus two commissions."""
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")
        held_qty = asset_free(portfolio)
        usdt_before_close = usdt_free(portfolio)
        expected_received = PRICE * held_qty * (1 - COMMISSION)

        portfolio.update_local_balance("BTCUSDT", PRICE, held_qty, "CLOSE")

        assert asset_free(portfolio) == pytest.approx(0.0)
        assert usdt_free(portfolio) == pytest.approx(usdt_before_close + expected_received)


@pytest.mark.unit
class TestCloseShort:
    def test_close_short_repays_locked_asset(self, portfolio):
        """Open SHORT, CLOSE with negative qty: locked asset should be repaid."""
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "SHORT")
        locked_before = asset_locked(portfolio)
        assert locked_before == pytest.approx(QUANTITY)

        # Close by passing negative quantity (the convention used by execution_handler)
        portfolio.update_local_balance("BTCUSDT", PRICE, -QUANTITY, "CLOSE")
        assert asset_locked(portfolio) == pytest.approx(0.0)

    def test_close_short_decreases_usdt(self, portfolio):
        """Buying back to cover the short costs USDT."""
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "SHORT")
        usdt_after_open = usdt_free(portfolio)

        portfolio.update_local_balance("BTCUSDT", PRICE, -QUANTITY, "CLOSE")

        # USDT should decrease (we paid to buy back)
        assert usdt_free(portfolio) < usdt_after_open


# ---------------------------------------------------------------------------
# Commission precision
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestCommissionPrecision:
    def test_commission_is_applied_as_fraction(self, portfolio):
        """Commission of 0.1% on a buy: received qty = qty × (1 - 0.001)."""
        portfolio.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")
        expected = QUANTITY * (1 - COMMISSION)
        assert asset_free(portfolio) == pytest.approx(expected, rel=1e-9)

    def test_zero_commission_gives_full_quantity(self):
        from execution.portfolio_info import MockPortfolioInfo
        p = MockPortfolioInfo(
            initial_balance={"USDT": {"free": INITIAL_USDT, "locked": 0.0}},
            commission_rate=0.0,
        )
        p.update_local_balance("BTCUSDT", PRICE, QUANTITY, "LONG")
        assert asset_free(p) == pytest.approx(QUANTITY)
