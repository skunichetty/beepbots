import copy
import logging
import random
import time
from dataclasses import dataclass

from battlebots.core.action import Action, ActionType
from battlebots.core.state import State, PlayerState
from battlebots.core.strategy import Strategy

logger = logging.getLogger(__name__)


@dataclass
class GameConfig:
    health_regeneration: int = 5
    energy_regeneration: int = 10
    game_length: int = 1000


@dataclass
class TickSummary:
    state: State
    actions: dict[str, ActionType]


def tick(
    state: State, strategies: dict[str, Strategy], config: GameConfig
) -> TickSummary:
    # evaluate strategy
    actions: dict[str, Action] = {}
    for name, player in state.players.items():
        actions[name] = strategies[name].evaluate(name, state)

    # randomly shuffle actions to debias game-ending action states
    action_list = list(actions.values())
    random.shuffle(action_list)

    for action in action_list:
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

    summary = TickSummary(
        copy.deepcopy(state),
        {player: action.name for player, action in actions.items()},
    )
    state.tick += 1
    return summary


@dataclass
class GameSummary:
    history: list[TickSummary]
    elapsed: int
    winner: str | None


def play_game(
    strategies: dict[str, Strategy],
    config: GameConfig,
) -> GameSummary:
    state = State({player: PlayerState() for player in strategies.keys()})

    history = []
    start = time.perf_counter_ns()
    while state.tick < config.game_length:
        try:
            history.append(tick(state, strategies, config))
        except KeyboardInterrupt:
            logger.info("\nClosing game")
            end = time.perf_counter_ns()
            return GameSummary(history, end - start, None)

        if len(state.players) == 1:
            final_player, _ = state.players.popitem()
            logger.info("Player %s has won!", final_player)
            end = time.perf_counter_ns()
            return GameSummary(history, end - start, final_player)
        elif len(state.players) == 0:
            logger.info("No player won (both died same tick)!")
            end = time.perf_counter_ns()
            return GameSummary(history, end - start, None)

    logger.info("No player won (time expired)")
    return GameSummary(history, None)
