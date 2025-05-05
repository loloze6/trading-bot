import os
from dotenv import load_dotenv

load_dotenv(override = True)

USE_TESTNET = os.getenv("USE_TESTNET", "True").lower() == "true"

if USE_TESTNET:
    API_KEY = os.getenv("BINANCE_API_KEY_TEST")
    API_SECRET = os.getenv("BINANCE_API_SECRET_TEST")
    BASE_URL = os.getenv("BASE_URL_TEST", "https://testnet.binance.vision/api")
    
else:
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    BASE_URL = os.getenv("BASE_URL", "https://api.binance.com")

from typing import Dict, List, Optional, Union, Any
import json
import logging

logger = logging.getLogger(__name__)  # Use the logger set up elsewhere

class ConfigManager:
    """Manages the configuration of the trading bot."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the ConfigManager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        # Default configuration
        default_config = {
            "api": {
                "key": "",
                "secret": ""
            },
            "trading": {
                "test_mode": True,
                "symbols": ["BTCUSDT"],
                "interval": "15m",
                "check_interval_seconds": 60
            },
            "strategy": {
                "name": "SimpleMovingAverage",
                "params": {
                    "short_window": 50,
                    "long_window": 200
                }
            },
            "risk_management": {
                "max_position_size": 0.1,  # 10% of available balance
                "stop_loss_pct": 0.05      # 5% stop loss
            },
            "logging": {
                "level": "INFO",
                "file_path": "trading_bot.log"
            }
        }
        
        # Try to load from file
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                
                # Merge with default config to ensure all keys exist
                self._deep_update(default_config, loaded_config)
                logger.info(f"Configuration loaded from {self.config_path}")
                
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
                logger.info("Using default configuration")
        else:
            logger.info(f"Configuration file {self.config_path} not found. Using default configuration.")
            # Save default config
            self.save_config(default_config)
            
        return default_config

    def _deep_update(self, original: Dict, update: Dict) -> None:
        """
        Recursively update a nested dictionary.
        
        Args:
            original: Original dictionary to update
            update: Dictionary with updates
        """
        for key, value in update.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                self._deep_update(original[key], value)
            else:
                original[key] = value

    def save_config(self, config: Optional[Dict] = None) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration to save (uses current config if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            config_to_save = config if config is not None else self.config
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=4)
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def get(self, section: str, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key (if None, returns entire section)
            default: Default value if key is not found
            
        Returns:
            Configuration value
        """
        if section not in self.config:
            return default
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value

    def update(self, section: str, values: Dict[str, Any]) -> None:
        """
        Update multiple configuration values in a section.
        
        Args:
            section: Configuration section
            values: Dictionary of values to update
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section].update(values)

    def validate(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required API keys if not in test mode
            if not self.config.get('trading', {}).get('test_mode', True):
                api_key = self.config.get('api', {}).get('key')
                api_secret = self.config.get('api', {}).get('secret')
                
                if not api_key or not api_secret:
                    logger.error("API key and secret are required when not in test mode")
                    return False
            
            # Check if there are symbols to trade
            symbols = self.config.get('trading', {}).get('symbols')
            if not symbols:
                logger.error("No trading symbols specified")
                return False
        except Exception as e:        
            raise RuntimeError(f"Could not fetch price: {e}")
        # More validation rules can be added here
        return True