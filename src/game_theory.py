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

def create_battle_of_sexes() -> Tuple[Game, Dict[str, Action]]:
    """
    Create a Battle of the Sexes game.
    
    In this game, two players want to coordinate but have different preferences:
    - Player 1 prefers going to the Opera
    - Player 2 prefers going to the Football game
    
    The payoffs are:
    - If they coordinate, both get positive payoff (but different amounts based on preference)
    - If they don't coordinate, both get 0
    
    @return: Tuple of (Game instance, Dictionary mapping action names to Action objects)
    """
    # Define actions
    opera = Action("opera")
    football = Action("football")
    
    # Create players
    player1 = Player("Player 1", [opera, football])
    player2 = Player("Player 2", [opera, football])
    
    # Battle of the Sexes payoffs:
    # (player1_action, player2_action): (player1_payoff, player2_payoff)
    payoff_matrix = {
        ("opera", "opera"): (3, 2),      # Both go to opera (Player 1 happier)
        ("opera", "football"): (0, 0),    # They don't coordinate
        ("football", "opera"): (0, 0),    # They don't coordinate
        ("football", "football"): (2, 3)  # Both go to football (Player 2 happier)
    }
    
    # Create actions dictionary
    actions = {
        "opera": opera,
        "football": football
    }
    
    return Game([player1, player2], payoff_matrix), actions

def create_chicken() -> Tuple[Game, Dict[str, Action]]:
    """
    Create a Chicken game.
    
    In this game, two players face off in a dangerous situation:
    - Each player can either "swerve" or "straight"
    - If both swerve, they both get a small positive payoff
    - If one swerves and the other goes straight, the straight player "wins" (higher payoff)
    - If both go straight, they both get a large negative payoff (crash)
    
    @return: Tuple of (Game instance, Dictionary mapping action names to Action objects)
    """
    # Define actions
    swerve = Action("swerve")
    straight = Action("straight")
    
    # Create players
    player1 = Player("Player 1", [swerve, straight])
    player2 = Player("Player 2", [swerve, straight])
    
    # Chicken game payoffs:
    # (player1_action, player2_action): (player1_payoff, player2_payoff)
    payoff_matrix = {
        ("swerve", "swerve"): (1, 1),        # Both swerve (safe)
        ("swerve", "straight"): (-1, 2),     # Player 1 swerves, Player 2 "wins"
        ("straight", "swerve"): (2, -1),     # Player 1 "wins", Player 2 swerves
        ("straight", "straight"): (-10, -10) # Both crash (disaster)
    }
    
    # Create actions dictionary
    actions = {
        "swerve": swerve,
        "straight": straight
    }
    
    return Game([player1, player2], payoff_matrix), actions

def create_stag_hunt() -> Tuple[Game, Dict[str, Action]]:
    """
    Create a Stag Hunt game.
    
    In this game, two players can either hunt a stag (cooperate) or hunt a hare (defect):
    - If both hunt the stag, they both get a large payoff
    - If one hunts the stag and the other hunts the hare, the hare hunter gets a small payoff
    - If both hunt the hare, they both get a small payoff
    
    This game demonstrates the tension between risk and reward in coordination.
    
    @return: Tuple of (Game instance, Dictionary mapping action names to Action objects)
    """
    # Define actions
    stag = Action("stag")
    hare = Action("hare")
    
    # Create players
    player1 = Player("Player 1", [stag, hare])
    player2 = Player("Player 2", [stag, hare])
    
    # Stag Hunt payoffs:
    # (player1_action, player2_action): (player1_payoff, player2_payoff)
    payoff_matrix = {
        ("stag", "stag"): (4, 4),     # Both hunt stag (best outcome)
        ("stag", "hare"): (0, 2),     # Player 1 hunts stag alone, Player 2 gets hare
        ("hare", "stag"): (2, 0),     # Player 2 hunts stag alone, Player 1 gets hare
        ("hare", "hare"): (2, 2)      # Both hunt hare (safe outcome)
    }
    
    # Create actions dictionary
    actions = {
        "stag": stag,
        "hare": hare
    }
    
    return Game([player1, player2], payoff_matrix), actions

def create_matching_pennies() -> Tuple[Game, Dict[str, Action]]:
    """
    Create a Matching Pennies game.
    
    In this zero-sum game:
    - Each player chooses heads or tails
    - If they match, Player 1 wins
    - If they don't match, Player 2 wins
    
    This game has no pure Nash equilibrium, only mixed strategy equilibrium.
    
    @return: Tuple of (Game instance, Dictionary mapping action names to Action objects)
    """
    # Define actions
    heads = Action("heads")
    tails = Action("tails")
    
    # Create players
    player1 = Player("Player 1", [heads, tails])
    player2 = Player("Player 2", [heads, tails])
    
    # Matching Pennies payoffs:
    # (player1_action, player2_action): (player1_payoff, player2_payoff)
    payoff_matrix = {
        ("heads", "heads"): (1, -1),   # Match, Player 1 wins
        ("heads", "tails"): (-1, 1),   # No match, Player 2 wins
        ("tails", "heads"): (-1, 1),   # No match, Player 2 wins
        ("tails", "tails"): (1, -1)    # Match, Player 1 wins
    }
    
    # Create actions dictionary
    actions = {
        "heads": heads,
        "tails": tails
    }
    
    return Game([player1, player2], payoff_matrix), actions

def create_ultimatum_game() -> Tuple[Game, Dict[str, Action]]:
    """
    Create an Ultimatum Game.
    
    In this game:
    - Player 1 (Proposer) has multiple options for how to split a resource (e.g., $10)
    - Player 2 (Responder) only has two options: accept or reject
    - If rejected, both get 0
    - If accepted, they get the proposed split
    
    This game demonstrates the tension between rational and fair behavior.
    
    @return: Tuple of (Game instance, Dictionary mapping action names to Action objects)
    """
    # Define actions for Player 1 (Proposer)
    split_90_10 = Action("90-10")  # Proposer gets 90%, Responder gets 10%
    split_70_30 = Action("70-30")  # Proposer gets 70%, Responder gets 30%
    split_50_50 = Action("50-50")  # Equal split
    
    # Define actions for Player 2 (Responder)
    accept = Action("accept")
    reject = Action("reject")
    
    # Create players
    proposer = Player("Proposer", [split_90_10, split_70_30, split_50_50])
    responder = Player("Responder", [accept, reject])
    
    # Ultimatum Game payoffs:
    # (proposer_action, responder_action): (proposer_payoff, responder_payoff)
    payoff_matrix = {
        ("90-10", "accept"): (9, 1),    # Proposer gets 9, Responder gets 1
        ("90-10", "reject"): (0, 0),    # Both get 0
        ("70-30", "accept"): (7, 3),    # Proposer gets 7, Responder gets 3
        ("70-30", "reject"): (0, 0),    # Both get 0
        ("50-50", "accept"): (5, 5),    # Equal split
        ("50-50", "reject"): (0, 0)     # Both get 0
    }
    
    # Create actions dictionary
    actions = {
        "90-10": split_90_10,
        "70-30": split_70_30,
        "50-50": split_50_50,
        "accept": accept,
        "reject": reject
    }
    
    return Game([proposer, responder], payoff_matrix), actions

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
        # Get unique actions for each player
        player1_actions = sorted(set(action1 for action1, _ in game.payoff_matrix.keys()))
        player2_actions = sorted(set(action2 for _, action2 in game.payoff_matrix.keys()))
        
        # Calculate column widths
        action_width = max(len(action) for action in player1_actions + player2_actions)
        payoff_width = 8  # Width for "(X, Y)" format
        
        # Print header
        print("\nPlayer 2 →")
        header = "Player 1 ↓" + " " * (action_width - 8)
        print(header, end="")
        for action2 in player2_actions:
            print(f"  {action2:<{action_width}}", end="")
        print("\n" + "-" * (action_width + (action_width + 2) * len(player2_actions)))
        
        # Print matrix rows
        for action1 in player1_actions:
            print(f"{action1:<{action_width}}", end="")
            for action2 in player2_actions:
                payoff = game.payoff_matrix[(action1, action2)]
                print(f"  ({payoff[0]:>2}, {payoff[1]:>2})", end="")
            print()
        print()
    
    print("\nNash Equilibria:")
    if equilibria:
        for eq in equilibria:
            print(f"- {eq[0]}/{eq[1]}")
            if verbose:
                payoff = game.payoff_matrix[eq]
                print(f"  Payoffs: ({payoff[0]}, {payoff[1]})")
    else:
        print("No pure Nash equilibria found")
    
    # Identify the game type based on available actions
    game_type = None
    if "defect" in actions and "cooperate" in actions:
        game_type = "prisoners_dilemma"
    elif "opera" in actions and "football" in actions:
        game_type = "battle_of_sexes"
    elif "swerve" in actions and "straight" in actions:
        game_type = "chicken"
    elif "stag" in actions and "hare" in actions:
        game_type = "stag_hunt"
    elif "heads" in actions and "tails" in actions:
        game_type = "matching_pennies"
    elif "90-10" in actions and "accept" in actions:
        game_type = "ultimatum"
    
    # Print game-specific analysis
    if game_type == "prisoners_dilemma" and len(equilibria) == 1 and equilibria[0] == (actions["defect"].name, actions["defect"].name):
        print("\nThis is the standard Prisoner's Dilemma outcome:")
        print("Both players defect, demonstrating the conflict between individual and collective rationality")
        print("The Nash equilibrium is Pareto inefficient - both players would be better off cooperating")
        print("However, the outcome is deterministic - both players will defect")
    elif game_type == "battle_of_sexes" and len(equilibria) == 2 and all(eq in [("opera", "opera"), ("football", "football")] for eq in equilibria):
        print("\nThis is the Battle of the Sexes outcome:")
        print("There are two Nash equilibria, demonstrating coordination problems")
        print("Without coordination, players might choose different equilibria")
        print("This could result in (opera, football) or (football, opera), giving both players 0")
    elif game_type == "chicken" and len(equilibria) == 2 and all(eq in [("swerve", "straight"), ("straight", "swerve")] for eq in equilibria):
        print("\nThis is the Chicken game outcome:")
        print("There are two Nash equilibria, demonstrating the danger of mutual defection")
        print("Unlike Prisoner's Dilemma, both equilibria are Pareto efficient")
        print("The worst outcome (mutual straight) is disastrous, making it crucial to avoid")
        print("Without coordination, players might both choose straight, leading to disaster")
    elif game_type == "stag_hunt" and len(equilibria) == 2 and all(eq in [("stag", "stag"), ("hare", "hare")] for eq in equilibria):
        print("\nThis is the Stag Hunt outcome:")
        print("There are two Nash equilibria, demonstrating the tension between risk and reward")
        print("Without coordination, players might choose different equilibria")
        print("This could result in one player hunting stag alone while the other gets a hare")
    elif game_type == "matching_pennies" and len(equilibria) == 0:
        print("\nThis is the Matching Pennies outcome:")
        print("No pure Nash equilibria exist, demonstrating the need for mixed strategies")
        print("The outcome is inherently non-deterministic")
        print("Players must randomize their choices to play optimally")
    elif game_type == "ultimatum" and len(equilibria) == 1 and equilibria[0] == (actions["90-10"].name, actions["accept"].name):
        print("\nThis is the Ultimatum Game outcome:")
        print("The proposer offers the minimum amount (90-10 split)")
        print("The responder accepts any positive amount")
        print("This demonstrates the tension between rational and fair behavior")

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
    
    # Create and analyze all games
    print("\nAnalyzing Prisoner's Dilemma:")
    game, actions = create_prisoners_dilemma()
    analyze_game(game, actions, args.verbose)
    
    print("\nAnalyzing Battle of the Sexes:")
    game, actions = create_battle_of_sexes()
    analyze_game(game, actions, args.verbose)
    
    print("\nAnalyzing Chicken:")
    game, actions = create_chicken()
    analyze_game(game, actions, args.verbose)
    
    print("\nAnalyzing Stag Hunt:")
    game, actions = create_stag_hunt()
    analyze_game(game, actions, args.verbose)
    
    print("\nAnalyzing Matching Pennies:")
    game, actions = create_matching_pennies()
    analyze_game(game, actions, args.verbose)
    
    print("\nAnalyzing Ultimatum Game:")
    game, actions = create_ultimatum_game()
    analyze_game(game, actions, args.verbose) 