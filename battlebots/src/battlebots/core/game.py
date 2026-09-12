import logging
from dataclasses import dataclass

from battlebots.core.action import Action
from battlebots.core.state import State, PlayerState
from battlebots.core.strategy import Strategy

logger = logging.getLogger(__name__)


@dataclass
class GameConfig:
    health_regeneration: int = 10
    energy_regeneration: int = 5
    game_length: int = 1000


def tick(state: State, strategies: dict[str, Strategy], config: GameConfig):
    # evaluate strategy
    actions: list[Action] = []
    for name, player in state.players.items():
        actions.append(strategies[name].evaluate(name, state))

    for action in actions:
        action.execute(state)

    # remove dead players
    dead_players = []
    for name, player in state.players.items():
        if not player.is_alive():
            logger.info("Player %s has died!", name)
            dead_players.append(name)

    for player in dead_players:
        del state.players[player]

    # regenerate health and energy
    for player in state.players.values():
        player.heal(config.health_regeneration)
        player.add_energy(config.energy_regeneration)

    state.tick += 1


@dataclass
class GameSummary:
    state: State
    strategies: dict[str, Strategy]
    winner: str | None

    def report(self):
        return f"""
Winner: {self.winner}

Final State:
{self.state.report()}
"""


def play_game(
    strategies: dict[str, Strategy],
    config: GameConfig,
) -> GameSummary:
    state = State({player: PlayerState() for player in strategies.keys()})

    while state.tick < config.game_length:
        try:
            tick(state, strategies, config)
        except KeyboardInterrupt:
            logger.info("\nClosing game")
            return GameSummary(state, strategies, None)

        if len(state.players) == 1:
            final_player, _ = state.players.popitem()
            logger.info("Player %s has won!", final_player)
            return GameSummary(state, strategies, final_player)
        elif len(state.players) == 0:
            logger.info("No player won (both died same tick)!")
            return GameSummary(state, strategies, None)

    logger.info("No player won (time expired)")
    return GameSummary(state, strategies, None)
