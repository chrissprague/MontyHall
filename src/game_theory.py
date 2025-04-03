#!/usr/bin/env python3

"""
Game theory solver program, focusing on finding Nash equilibria and optimal strategies.
"""

import sys
import argparse
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass

@dataclass
class Action:
    """Represents a possible action in the game."""
    name: Optional[str] = None
    payoff: float = 0
    
    def __post_init__(self):
        if self.name is None:
            self.name = f"Action_{id(self)}"

@dataclass
class Player:
    """Represents a player in the game."""
    name: Optional[str] = None
    actions: List[Action] = None
    current_action: Action = None
    
    def __post_init__(self):
        if self.name is None:
            self.name = f"Player_{id(self)}"
        if self.actions is None:
            self.actions = []

class Game:
    """
    Represents a game theory scenario with defined payoffs and players.
    """
    def __init__(self, players: List[Player], payoff_matrix: Dict[Tuple[str, str], Tuple[float, float]]):
        self.players = players
        self.payoff_matrix = payoff_matrix
        self.nash_equilibria: List[Tuple[str, str]] = []

    def find_best_response(self, player: Player, other_player_action: str) -> Set[str]:
        """
        Find the best response(s) for a player given the other player's action.
        
        @param player: The player finding their best response
        @param other_player_action: The action chosen by the other player
        @return: Set of action names that are best responses
        """
        best_payoff = float('-inf')
        best_actions = set()
        
        for action in player.actions:
            if player == self.players[0]:
                payoff = self.payoff_matrix[(action.name, other_player_action)][0]
            else:
                payoff = self.payoff_matrix[(other_player_action, action.name)][1]
                
            if payoff > best_payoff:
                best_payoff = payoff
                best_actions = {action.name}
            elif payoff == best_payoff:
                best_actions.add(action.name)
                
        return best_actions

    def find_nash_equilibria(self) -> List[Tuple[str, str]]:
        """
        Find all Nash equilibria in the game.
        
        @return: List of (player1_action, player2_action) tuples representing Nash equilibria
        """
        equilibria = []
        
        # Check each possible action combination
        for action1 in self.players[0].actions:
            for action2 in self.players[1].actions:
                # Find best responses for both players
                player1_best = self.find_best_response(self.players[0], action2.name)
                player2_best = self.find_best_response(self.players[1], action1.name)
                
                # If both players are playing their best responses, it's a Nash equilibrium
                if action1.name in player1_best and action2.name in player2_best:
                    equilibria.append((action1.name, action2.name))
        
        self.nash_equilibria = equilibria
        return equilibria

def create_prisoners_dilemma() -> Tuple[Game, Dict[str, Action]]:
    """
    Create a Prisoner's Dilemma game with standard payoffs.
    
    @return: Tuple of (Game instance, Dictionary mapping action names to Action objects)
    """
    # Define actions
    cooperate = Action("cooperate")
    defect = Action("defect")
    
    # Create players (with optional names)
    player1 = Player("Player 1", [cooperate, defect])  # Named player
    player2 = Player(actions=[cooperate, defect])  # Anonymous player
    
    # Standard Prisoner's Dilemma payoffs:
    # (player1_action, player2_action): (player1_payoff, player2_payoff)
    payoff_matrix = {
        ("cooperate", "cooperate"): (3, 3),    # Both cooperate
        ("cooperate", "defect"): (0, 5),       # Player 1 cooperates, Player 2 defects
        ("defect", "cooperate"): (5, 0),       # Player 1 defects, Player 2 cooperates
        ("defect", "defect"): (1, 1)           # Both defect
    }
    
    # Create actions dictionary
    actions = {
        "cooperate": cooperate,
        "defect": defect
    }
    
    return Game([player1, player2], payoff_matrix), actions

def analyze_game(game: Game, actions: Dict[str, Action], verbose: bool = False) -> None:
    """
    Analyze the game to find Nash equilibria and optimal strategies.
    
    @param game: The game to analyze
    @param actions: Dictionary mapping action names to Action objects
    @param verbose: Whether to print detailed information
    """
    equilibria = game.find_nash_equilibria()
    
    print("\nGame Analysis:")
    print("=============")
    
    if verbose:
        print("\nPayoff Matrix:")
        for (action1, action2), (payoff1, payoff2) in game.payoff_matrix.items():
            print(f"{action1}/{action2}: ({payoff1}, {payoff2})")
    
    print("\nNash Equilibria:")
    if equilibria:
        for eq in equilibria:
            print(f"- {eq[0]}/{eq[1]}")
            if verbose:
                payoff = game.payoff_matrix[eq]
                print(f"  Payoffs: ({payoff[0]}, {payoff[1]})")
    else:
        print("No pure Nash equilibria found")
    
    # For the Prisoner's Dilemma, we know the optimal outcome
    if len(equilibria) == 1 and equilibria[0] == (actions["defect"].name, actions["defect"].name):
        print("\nThis is the standard Prisoner's Dilemma outcome:")
        print("Both players defect, demonstrating the conflict between individual and collective rationality")

def parse_args():
    parser = argparse.ArgumentParser(
        description='Analyze game theory scenarios, starting with the Prisoner\'s Dilemma.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Print detailed information about the game analysis')
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    game, actions = create_prisoners_dilemma()
    analyze_game(game, actions, args.verbose) 