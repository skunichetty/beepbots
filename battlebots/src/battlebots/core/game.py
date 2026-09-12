import logging
from dataclasses import dataclass

from battlebots.core.action import Action
from battlebots.core.state import State, PlayerState
from battlebots.core.strategy import Strategy

logger = logging.getLogger(__name__)


def tick(state: State, strategies: dict[str, Strategy]):
    # regenerate health and energy
    for player in state.players.values():
        player.heal(10)
        player.add_energy(5)

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

    state.tick += 1


@dataclass
class GameSummary:
    players: dict[str, PlayerState]
    strategies: dict[str, Strategy]
    ticks: int
    winner: str | None


def play_game(strategies: dict[str, Strategy]) -> GameSummary:
    state = State({player: PlayerState() for player in strategies.keys()})

    while state.tick < 1000:
        tick(state, strategies)
        if len(state.players) == 1:
            final_player, _ = state.players.popitem()
            logger.info("Player %s has won!", final_player)
            return GameSummary(state.players, strategies, state.tick, final_player)
        elif len(state.players) == 0:
            logger.info("No player won (both died same tick)!")
            return GameSummary(state.players, strategies, state.tick, None)

    logger.info("No player won (time expired)")
    return GameSummary(state.players, strategies, state.tick, None)
