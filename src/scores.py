"""
Score management system for the Discord bot.
Handles loading, saving, and manipulation of user scores.
"""

import json
from typing import Dict, Optional, Union
from pathlib import Path

from constants import SCORES_JSON_PATH, ERROR_MESSAGES
from exceptions import ScoreError
from bot_types import UserScore, UserID, ScoreDict
from logging_utils import get_logger

logger = get_logger(__name__)


class ScoreManager:
    """Manages user scores with proper error handling and validation."""
    
    def __init__(self, db_path: str = SCORES_JSON_PATH):
        """
        Initialize the score manager.
        
        Args:
            db_path: Path to the scores JSON file
        """
        self.db_path = Path(db_path)
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load_scores(self) -> ScoreDict:
        """
        Load scores from the JSON file.
        
        Returns:
            Dictionary mapping user IDs to UserScore objects
            
        Raises:
            ScoreError: If there's an error loading scores
        """
        if not self.db_path.exists():
            logger.warning("Scores file %s does not exist. Returning empty dict.", self.db_path)
            return {}
        
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                raw_scores = json.load(f)
            
            # Convert raw dict to UserScore objects
            scores = {}
            for user_id, score_data in raw_scores.items():
                try:
                    scores[user_id] = UserScore(
                        username=score_data.get("username", ""),
                        pontos=score_data.get("pontos", 0),
                        arkdle_last_win=score_data.get("arkdle_last_win")
                    )
                except ValueError as e:
                    logger.error("Invalid score data for user %s: %s", user_id, e)
                    continue
            
            logger.info("Scores loaded successfully from %s. Loaded %d users.", 
                       self.db_path, len(scores))
            return scores
            
        except json.JSONDecodeError as e:
            error_msg = ERROR_MESSAGES["JSON_DECODE_ERROR"].format(self.db_path)
            logger.error("%s: %s", error_msg, e)
            raise ScoreError(error_msg) from e
        except Exception as e:
            error_msg = ERROR_MESSAGES["LOAD_ERROR"].format(e)
            logger.error("%s", error_msg)
            raise ScoreError(error_msg) from e
    
    def save_scores(self, scores: ScoreDict) -> None:
        """
        Save scores to the JSON file.
        
        Args:
            scores: Dictionary mapping user IDs to UserScore objects
            
        Raises:
            ScoreError: If there's an error saving scores
        """
        try:
            # Convert UserScore objects to dict for JSON serialization
            raw_scores = {}
            for user_id, user_score in scores.items():
                raw_scores[user_id] = {
                    "username": user_score.username,
                    "pontos": user_score.pontos,
                    "arkdle_last_win": user_score.arkdle_last_win
                }
            
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(raw_scores, f, ensure_ascii=False, indent=2)
            
            logger.info("Scores saved successfully to %s. Saved %d users.", 
                       self.db_path, len(scores))
            
        except Exception as e:
            error_msg = ERROR_MESSAGES["SAVE_ERROR"].format(e)
            logger.error("%s", error_msg)
            raise ScoreError(error_msg) from e
    
    def get_user_score(self, user_id: UserID) -> Optional[UserScore]:
        """
        Get a specific user's score.
        
        Args:
            user_id: The user's ID
            
        Returns:
            UserScore object if found, None otherwise
        """
        scores = self.load_scores()
        return scores.get(user_id)
    
    def update_user_score(self, user_id: UserID, username: str, 
                         points: int, arkdle_last_win: Optional[str] = None) -> None:
        """
        Update a user's score.
        
        Args:
            user_id: The user's ID
            username: The user's username
            points: Points to add (can be negative)
            arkdle_last_win: Last operator won in Arkdle (optional)
        """
        scores = self.load_scores()
        
        if user_id in scores:
            scores[user_id].pontos += points
            scores[user_id].username = username
            if arkdle_last_win:
                scores[user_id].arkdle_last_win = arkdle_last_win
        else:
            scores[user_id] = UserScore(
                username=username,
                pontos=points,
                arkdle_last_win=arkdle_last_win
            )
        
        self.save_scores(scores)
    
    def get_ranking(self, limit: Optional[int] = None) -> list[tuple[UserID, UserScore]]:
        """
        Get the user ranking sorted by points.
        
        Args:
            limit: Maximum number of users to return (None for all)
            
        Returns:
            List of tuples (user_id, UserScore) sorted by points (descending)
        """
        scores = self.load_scores()
        ranking = sorted(scores.items(), key=lambda x: x[1].pontos, reverse=True)
        
        if limit:
            ranking = ranking[:limit]
        
        return ranking


# Global score manager instance
_score_manager = ScoreManager()


# Backward compatibility functions
def load_scores() -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Load scores (backward compatibility).
    
    Returns:
        Dictionary in the old format for backward compatibility
    """
    scores = _score_manager.load_scores()
    # Convert back to old format for compatibility
    return {
        user_id: {
            "username": score.username,
            "pontos": score.pontos,
            "arkdle_last_win": score.arkdle_last_win
        }
        for user_id, score in scores.items()
    }


def save_scores(scores: Dict[str, Dict[str, Union[str, int]]]) -> None:
    """
    Save scores (backward compatibility).
    
    Args:
        scores: Dictionary in the old format
    """
    # Convert to new format
    new_scores = {}
    for user_id, score_data in scores.items():
        new_scores[user_id] = UserScore(
            username=score_data.get("username", ""),
            pontos=score_data.get("pontos", 0),
            arkdle_last_win=score_data.get("arkdle_last_win")
        )
    
    _score_manager.save_scores(new_scores)