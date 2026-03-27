@dataclass
class PriceTick:
    """Individual price tick."""
    symbol: str
    price: float
    timestamp: datetime.datetime
    volume: Optional[float] = None

@dataclass
class Candle:
    """Custom candle structure."""
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    start_time: datetime.datetime
    end_time: datetime.datetime
    tick_count: int = 0

class CandleBuilder:
    """Builds custom candles from real-time price ticks."""
 
     def __init__(self, interval_seconds: int, candle_completion_callback: Callable[[str, Candle], None] = None):
        """
        Initialize CandleBuilder.
        
        Args:
            interval_seconds: Candle interval in seconds
            candle_completion_callback: Function to call when a candle is completed
                                      Should accept (symbol: str, candle: Candle) parameters
        """
    
    def add_tick(self, tick: PriceTick) -> Optional[Candle]:
        """
        Add a price tick and return completed candle if interval finished.
        
        Returns:
            Completed candle if interval finished, None otherwise
        """

    def _start_new_candle(self, tick: PriceTick) -> Candle:
        """Start a new candle with the given tick."""

    def _update_candle(self, candle: Candle, tick: PriceTick):
        """Update existing candle with new tick."""

    def _align_to_interval(self, timestamp: datetime.datetime) -> datetime.datetime:
        """Align timestamp to interval boundary."""

    def get_candle_history(self, symbol: str, count: int = 1) -> pd.DataFrame:
        """Get historical candles as DataFrame."""

class DataManager:
    """Manages real-time data fetching and candle building."""

    def __init__(self, symbols: List[str], price_fetch_interval: int, candle_builder: CandleBuilder):
        """
        Initialize DataManager.
        
        Args:
            symbols: List of trading symbols
            price_fetch_interval: Interval for fetching prices in seconds
            candle_builder: CandleBuilder instance for processing ticks
        """

    def initiate_start_thread(self) -> Optional[threading.Thread]:
        """Start the price fetching thread."""

    def _rest_price_fetcher(self):        
        """Fetch prices using REST API at regular intervals for all symbols and store them in a queue."""
 
    def _get_current_price(self, symbol: str) -> Optional[Dict]:
        """Get current price from exchange."""

    def _main_candle_processing_loop(self):
        """Main loop that retrieve ticks from a queue and ask to process it."""

    def _process_price_tick(self, tick: PriceTick):
        """Process a single price tick."""

class HistoricalDataManager:
    """Manager of historical data during backtesting."""
    def __init__(self, historical_data: Dict[str, pd.DataFrame] = None):
        """
        Initialize the historical data provider with data library.
        
        Args:
            historical_data: Dictionary mapping symbols to their historical data DataFrames - see structure above
        """

    def get_historical_klines(self, symbol: str, interval: str, limit: int = 1) -> pd.DataFrame:
        """
        Fetch historical kline (candlestick) data at current index (index simulated into HistoricalDataProvider)
        
        Args:
            symbol: Trading pair symbol
            interval: Kline interval (ignored in backtesting)
            limit: Number of klines to retrieve
            
        Returns:
            DataFrame with OHLCV data
        """

    def advance(self, symbol: str, steps: int = 1) -> bool:
        """
        Advance the current index for a symbol.
        
        Args:
            symbol: Trading pair symbol
            steps: Number of steps to advance
            
        Returns:
            True if successful, False if no more data
        """

class HistoricalDataFetcher:
    """Provider for historical data during backtesting with intelligent merging."""
    def __init__(self, start_date, end_date, symbols=["BTCUSDT"], candle_interval_seconds="5m", exchange="binance", localStorage= False):
        """
        Initialize the data fetcher with date range and symbols.
        
        Args:
            start_date: Start date for data collection (string or datetime)
            end_date: End date for data collection (string or datetime)
            symbols: List of trading symbols to fetch
            candle_interval_seconds: Data interval (e.g., "5m", "1h", "1d")
            exchange: CCXT-supported exchange name (default: binance)
        """

    (...)

    def get_data(self, symbol=None):
        """
        Get the loaded data for a specific symbol or all symbols.
        
        Args:
            symbol: Specific symbol to get data for. If None, returns all data.
            
        Returns:
            Data for the requested symbol(s)
        """