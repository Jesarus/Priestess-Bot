"""
Game state management for the Discord bot.
Handles game rounds, user states, and game logic.
"""

from typing import Dict, Optional, List, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from bot_types import GameRound, GameState, UserID
from constants import ARKDLE_HINT_FIELDS, ARKDLE_BASE_POINTS
from exceptions import InvalidGameStateError
from logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class UserGameState:
    """Represents a user's state in a game."""
    user_id: UserID
    hint_index: int = 1
    has_won: bool = False
    last_guess: Optional[str] = None
    join_time: datetime = field(default_factory=datetime.now)


class GameStateManager:
    """Manages game states for all games."""
    
    def __init__(self):
        """Initialize the game state manager."""
        self._guess_who_round: Optional[GameRound] = None
        self._arkdle_round: Optional[GameRound] = None
        self._user_states: Dict[UserID, UserGameState] = {}
        self._active_games: Set[str] = set()
    
    # Guess Who Game Management
    
    def start_guess_who_round(self, operator_name: str, correct_answers: List[str]) -> str:
        """
        Start a new Guess Who round.
        
        Args:
            operator_name: Name of the operator
            correct_answers: List of correct answer variations
            
        Returns:
            Round ID
            
        Raises:
            InvalidGameStateError: If a round is already in progress
        """
        if self._guess_who_round and self._guess_who_round.state == GameState.IN_PROGRESS:
            raise InvalidGameStateError("A Guess Who round is already in progress")
        
        self._guess_who_round = GameRound(
            state=GameState.IN_PROGRESS,
            current_operator=operator_name,
            correct_answer=correct_answers,
            start_time=datetime.now().isoformat()
        )
        
        self._active_games.add("guess_who")
        logger.info("Started Guess Who round: %s", operator_name)
        return self._guess_who_round.round_id
    
    def submit_guess_who_answer(self, user_id: UserID, guess: str) -> bool:
        """
        Submit a guess for the current Guess Who round.
        
        Args:
            user_id: User ID
            guess: User's guess
            
        Returns:
            True if guess was accepted, False if already answered
            
        Raises:
            InvalidGameStateError: If no round is in progress
        """
        if not self._guess_who_round or self._guess_who_round.state != GameState.IN_PROGRESS:
            raise InvalidGameStateError("No Guess Who round in progress")
        
        if user_id in self._guess_who_round.answers:
            return False  # Already answered
        
        self._guess_who_round.answers[user_id] = guess.lower().strip()
        logger.info("User %s submitted guess: %s", user_id, guess)
        return True
    
    def end_guess_who_round(self) -> Dict[str, List[str]]:
        """
        End the current Guess Who round and return results.
        
        Returns:
            Dictionary with 'winners' and 'all_answers' lists
            
        Raises:
            InvalidGameStateError: If no round is in progress
        """
        if not self._guess_who_round or self._guess_who_round.state != GameState.IN_PROGRESS:
            raise InvalidGameStateError("No Guess Who round in progress")
        
        winners = []
        all_answers = list(self._guess_who_round.answers.keys())
        
        if self._guess_who_round.correct_answer:
            for user_id, guess in self._guess_who_round.answers.items():
                if guess in self._guess_who_round.correct_answer:
                    winners.append(user_id)
        
        self._guess_who_round.state = GameState.COMPLETED
        self._active_games.discard("guess_who")
        
        logger.info("Ended Guess Who round. Winners: %d, Total answers: %d", 
                   len(winners), len(all_answers))
        
        return {
            "winners": winners,
            "all_answers": all_answers
        }
    
    def get_guess_who_round(self) -> Optional[GameRound]:
        """Get the current Guess Who round."""
        return self._guess_who_round
    
    # Arkdle Game Management
    
    def start_arkdle_round(self, operator_data: Dict[str, str]) -> str:
        """
        Start a new Arkdle round.
        
        Args:
            operator_data: Operator data dictionary
            
        Returns:
            Round ID
            
        Raises:
            InvalidGameStateError: If a round is already in progress
        """
        if self._arkdle_round and self._arkdle_round.state == GameState.IN_PROGRESS:
            raise InvalidGameStateError("An Arkdle round is already in progress")
        
        self._arkdle_round = GameRound(
            state=GameState.IN_PROGRESS,
            current_operator=operator_data.get("name"),
            correct_answer=[operator_data.get("name", "").lower()],
            start_time=datetime.now().isoformat()
        )
        
        # Store operator data for hints
        self._arkdle_round.operator_data = operator_data
        
        self._active_games.add("arkdle")
        logger.info("Started Arkdle round: %s", operator_data.get("name"))
        return self._arkdle_round.round_id
    
    def get_user_arkdle_state(self, user_id: UserID) -> UserGameState:
        """
        Get or create a user's Arkdle state.
        
        Args:
            user_id: User ID
            
        Returns:
            User's game state
        """
        if user_id not in self._user_states:
            self._user_states[user_id] = UserGameState(user_id=user_id)
        return self._user_states[user_id]
    
    def submit_arkdle_guess(self, user_id: UserID, guess: str) -> Dict[str, any]:
        """
        Submit a guess for the current Arkdle round.
        
        Args:
            user_id: User ID
            guess: User's guess
            
        Returns:
            Dictionary with result information
            
        Raises:
            InvalidGameStateError: If no round is in progress
        """
        if not self._arkdle_round or self._arkdle_round.state != GameState.IN_PROGRESS:
            raise InvalidGameStateError("No Arkdle round in progress")
        
        user_state = self.get_user_arkdle_state(user_id)
        
        if user_state.has_won:
            return {"status": "already_won", "message": "You already won this round!"}
        
        normalized_guess = guess.lower().strip()
        correct_name = self._arkdle_round.correct_answer[0] if self._arkdle_round.correct_answer else ""
        
        if normalized_guess == correct_name:
            # Correct guess
            user_state.has_won = True
            hints_used = user_state.hint_index
            points = max(1, ARKDLE_BASE_POINTS // hints_used)
            
            logger.info("User %s won Arkdle with %d hints, earned %d points", 
                       user_id, hints_used, points)
            
            return {
                "status": "correct",
                "points": points,
                "hints_used": hints_used,
                "operator_name": self._arkdle_round.current_operator
            }
        else:
            # Wrong guess, provide next hint
            if user_state.hint_index < len(ARKDLE_HINT_FIELDS):
                hint_field = ARKDLE_HINT_FIELDS[user_state.hint_index]
                hint_value = self._arkdle_round.operator_data.get(hint_field, "Unknown")
                user_state.hint_index += 1
                
                return {
                    "status": "incorrect",
                    "hint": f"{hint_field.capitalize()} is '{hint_value}'",
                    "hint_index": user_state.hint_index
                }
            else:
                return {
                    "status": "no_more_hints",
                    "message": "No more hints available!"
                }
    
    def end_arkdle_round(self) -> None:
        """
        End the current Arkdle round.
        
        Raises:
            InvalidGameStateError: If no round is in progress
        """
        if not self._arkdle_round or self._arkdle_round.state != GameState.IN_PROGRESS:
            raise InvalidGameStateError("No Arkdle round in progress")
        
        self._arkdle_round.state = GameState.COMPLETED
        self._active_games.discard("arkdle")
        
        # Reset user states for next round
        self._user_states.clear()
        
        logger.info("Ended Arkdle round")
    
    def get_arkdle_round(self) -> Optional[GameRound]:
        """Get the current Arkdle round."""
        return self._arkdle_round
    
    # General Game Management
    
    def get_active_games(self) -> Set[str]:
        """Get set of currently active games."""
        return self._active_games.copy()
    
    def cleanup_old_states(self, max_age_hours: int = 24) -> int:
        """
        Clean up old user states.
        
        Args:
            max_age_hours: Maximum age in hours for user states
            
        Returns:
            Number of states cleaned up
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        old_states = [
            user_id for user_id, state in self._user_states.items()
            if state.join_time < cutoff_time
        ]
        
        for user_id in old_states:
            del self._user_states[user_id]
        
        if old_states:
            logger.info("Cleaned up %d old user states", len(old_states))
        
        return len(old_states)
    
    def reset_all_games(self) -> None:
        """Reset all games and clear all states."""
        self._guess_who_round = None
        self._arkdle_round = None
        self._user_states.clear()
        self._active_games.clear()
        logger.info("Reset all game states")


# Global game state manager instance
game_state = GameStateManager()
