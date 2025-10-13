"""
Utility functions for the Discord bot.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path

from constants import ALTERNATIVE_NAMES_PATH, ERROR_MESSAGES
from exceptions import DataError
from logging_utils import get_logger

logger = get_logger(__name__)


def load_alternative_names(path: str = ALTERNATIVE_NAMES_PATH) -> Dict[str, List[str]]:
    """
    Load alternative operator names from a JSON file.
    
    The file must have the format: {"MainName": ["alternative1", "alternative2", ...], ...}
    Returns a dictionary with keys and values in lowercase for easier search.
    
    Args:
        path: Path to the alternative names JSON file
        
    Returns:
        Dictionary mapping lowercase main names to lists of lowercase alternatives
        
    Raises:
        DataError: If there's an error loading the file
    """
    names = {}
    file_path = Path(path)
    
    if not file_path.exists():
        logger.warning("Alternative names file %s does not exist.", path)
        return names
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for key, alternatives in data.items():
            if isinstance(alternatives, list):
                # Normalize all names to lowercase and strip whitespace
                normalized_alternatives = [
                    alt.strip().lower() 
                    for alt in alternatives 
                    if isinstance(alt, str) and alt.strip()
                ]
                names[key.lower()] = normalized_alternatives
            else:
                logger.warning("Invalid alternative names format for key '%s': expected list", key)
        
        logger.info("Loaded %d alternative name mappings from %s", len(names), path)
        return names
        
    except json.JSONDecodeError as e:
        error_msg = ERROR_MESSAGES["JSON_DECODE_ERROR"].format(path)
        logger.error("%s: %s", error_msg, e)
        raise DataError(error_msg) from e
    except Exception as e:
        error_msg = ERROR_MESSAGES["LOAD_ERROR"].format(e)
        logger.error("%s", error_msg)
        raise DataError(error_msg) from e


def normalize_operator_name(name: str) -> str:
    """
    Normalize an operator name for comparison.
    
    Args:
        name: The operator name to normalize
        
    Returns:
        Normalized name (lowercase, stripped)
    """
    return name.strip().lower() if name else ""


def find_operator_alternatives(operator_name: str, 
                             alternative_names: Optional[Dict[str, List[str]]] = None) -> List[str]:
    """
    Find all alternative names for an operator.
    
    Args:
        operator_name: The operator name to find alternatives for
        alternative_names: Pre-loaded alternative names dict (optional)
        
    Returns:
        List of all alternative names including the original
    """
    if alternative_names is None:
        alternative_names = load_alternative_names()
    
    normalized_name = normalize_operator_name(operator_name)
    
    # Start with the original name
    alternatives = [normalized_name]
    
    # Find alternatives from the mapping
    for main_name, alt_list in alternative_names.items():
        if normalized_name == main_name or normalized_name in alt_list:
            # Add all alternatives for this operator
            alternatives.extend([main_name] + alt_list)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_alternatives = []
    for alt in alternatives:
        if alt not in seen:
            seen.add(alt)
            unique_alternatives.append(alt)
    
    return unique_alternatives


def is_valid_operator_name(name: str) -> bool:
    """
    Check if an operator name is valid.
    
    Args:
        name: The name to validate
        
    Returns:
        True if the name is valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    normalized = normalize_operator_name(name)
    return len(normalized) > 0 and len(normalized) <= 50  # Reasonable length limit