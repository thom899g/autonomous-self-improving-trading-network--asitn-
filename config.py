"""
ASITN Configuration Management
Handles environment variables, trading pairs, and system constants
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase_credentials.json")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "asitn-system")
    collections: Dict[str, str] = None
    
    def __post_init__(self):
        self.collections = {
            "strategies": "trading_strategies",
            "transactions": "trade_transactions",
            "performance": "strategy_performance",
            "evolution": "neuroevolution_state",
            "system": "system_health"
        }

@dataclass
class TradingConfig:
    """Trading platform configuration"""
    exchange: str = os.getenv("TRADING_EXCHANGE", "binance")
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    trading_pairs: List[str] = None
    paper_trading: bool = os.getenv("PAPER_TRADING", "true").lower() == "true"
    
    def __post_init__(self):
        self.trading_pairs = [
            "BTC/USDT",
            "ETH/USDT",
            "SOL/USDT",
            "ADA/USDT"
        ]

@dataclass
class RLConfig:
    """Reinforcement Learning configuration"""
    training_episodes: int = int(os.getenv("RL_TRAINING_EPISODES", "1000"))
    state_size: int = 20  # Features per timestep
    action_size: int = 3  # Buy, Sell, Hold
    learning_rate: float = float(os.getenv("RL_LEARNING_RATE", "0.001"))
    gamma: float = float(os.getenv("RL_DISCOUNT_FACTOR", "0.95"))
    
@dataclass
class NeuroevolutionConfig:
    """Neuroevolution configuration"""
    population_size: int = int(os.getenv("NE_POPULATION_SIZE", "50"))
    mutation_rate: float = float(os.getenv("NE_MUTATION_RATE", "0.1"))
    generations: int = int(os.getenv("NE_GENERATIONS", "100"))
    elite_size: int = int(os.getenv("NE_ELITE_SIZE", "5"))

@dataclass
class SystemConfig:
    """System operation configuration"""
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    health_check_interval: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "60"))
    max_concurrent_strategies: int = int(os.getenv("MAX_CONCURRENT_STRATEGIES", "5"))
    max_loss_percentage: float = float(os.getenv("MAX_LOSS_PERCENTAGE", "0.05"))
    risk_free_rate: float = float(os.getenv("RISK_FREE_RATE", "0.02"))

class ConfigManager:
    """Manages all system configurations"""
    
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.rl = RLConfig()
        self.neuroevolution = NeuroevolutionConfig()
        self.system = SystemConfig()
        
        # Validate critical configurations
        self._validate_config()
    
    def _validate_config(self):
        """Validate critical configuration parameters"""
        if not self.trading.api_key and not self.trading.paper_trading:
            logging.warning("No API key found. Running in paper trading mode.")
            self.trading.paper_trading = True
        
        if not os.path.exists(self.firebase.credentials_path):
            logging.error(f"Firebase credentials not found at {self.firebase.credentials_path}")
            raise FileNotFoundError("Firebase credentials file is required")
    
    def get_logging_config(self) -> Dict:
        """Get logging configuration"""
        return {
            "level": self.system.log_level,
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
        }

# Global configuration instance
config = ConfigManager()