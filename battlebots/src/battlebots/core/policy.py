import logging
import random
from abc import ABC, abstractmethod

import numpy as np

from battlebots.core.action import (
    ACTION_TYPES,
    ActionEncoder,
    ActionType,
)
from battlebots.core.state import State

logger = logging.getLogger(__name__)


class Policy(ABC):
    @abstractmethod
    def evaluate(
        self, player_name: str, state: State, encoder: ActionEncoder
    ) -> np.ndarray:
        raise NotImplementedError


def _build_one_hot(
    action_type: ActionType, encoder: ActionEncoder, target: str | None
) -> np.ndarray:
    index = encoder.encode(action_type, target)
    probability_vector = np.zeros(shape=(encoder.num_options(),))
    probability_vector[index] = 1

    return probability_vector


class DummyPolicy(Policy):
    def evaluate(
        self, player_name: str, state: State, encoder: ActionEncoder
    ) -> np.ndarray:
        other_players = [name for name in state.players if name != player_name]
        random_player = random.choice(other_players)
        return _build_one_hot("light_damage", encoder, random_player)


class CliPlayerPolicy(Policy):
    def evaluate(
        self, player_name: str, state: State, encoder: ActionEncoder
    ) -> np.ndarray:
        other_players = [name for name in state.players if name != player_name]
        logger.info("%s", state.report())

        desired_action = None
        failures = 0

        while desired_action is None:
            desired_action = input(f"Select an action {list(ACTION_TYPES)}: ")

            match desired_action:
                case "light_damage":
                    desired_target = None
                    while desired_target is None:
                        desired_target = input(
                            f"Select a player to damage {other_players}: "
                        )
                        if desired_target not in other_players:
                            logger.error("%s is not a valid player!", desired_target)
                            desired_target = None

                    return _build_one_hot("light_damage", encoder, desired_target)

                case "heavy_damage":
                    desired_target = None
                    while desired_target is None:
                        desired_target = input(
                            f"Select a player to damage {other_players}: "
                        )
                        if desired_target not in other_players:
                            logger.error("%s is not a valid player!", desired_target)
                            desired_target = None

                    return _build_one_hot("heavy_damage", encoder, desired_target)

                case "heal":
                    return _build_one_hot("heal", encoder, None)

                case "wait":
                    return _build_one_hot("wait", encoder, None)

                case _:
                    if failures < 10:
                        logger.error("%s is not a valid action!", desired_action)
                        desired_action = None
                    else:
                        raise ValueError(
                            f"{desired_action} is not a valid action! (failed 10 times)"
                        )
        return None
