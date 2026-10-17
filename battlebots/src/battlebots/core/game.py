import copy
import logging
import random
import time
from dataclasses import dataclass

import numpy as np

from battlebots.core.action import Action, ActionEncoder, build_action
from battlebots.core.policy import Policy
from battlebots.core.state import State, PlayerState

logger = logging.getLogger(__name__)


@dataclass
class GameConfig:
    health_regeneration: int = 5
    energy_regeneration: int = 10
    game_length: int = 1000


@dataclass
class TickSummary:
    state: State
    actions: dict[str, np.ndarray]


def tick(
    state: State,
    policies: dict[str, Policy],
    config: GameConfig,
    encoder: ActionEncoder,
) -> TickSummary:
    # evaluate policy
    actions: dict[str, Action] = {}
    action_vectors: dict[str, np.ndarray] = {}

    for name, player in state.players.items():
        action_vector = policies[name].evaluate(name, state, encoder)
        index = np.random.choice(np.arange(len(action_vector)), p=action_vector)
        action, target = encoder.decode(index)
        actions[name] = build_action(action, name, target=target)
        action_vectors[name] = action_vector

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

    summary = TickSummary(copy.deepcopy(state), action_vectors)
    state.tick += 1
    return summary


@dataclass
class GameSummary:
    history: list[TickSummary]
    elapsed: int
    winner: str | None


def play_game(
    policies: dict[str, Policy],
    config: GameConfig,
) -> GameSummary:
    state = State({player: PlayerState() for player in policies.keys()})
    encoder = ActionEncoder(list(policies.keys()))

    history = []
    start = time.perf_counter_ns()
    while state.tick < config.game_length:
        try:
            history.append(tick(state, policies, config, encoder))
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
