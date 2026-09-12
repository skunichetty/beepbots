import logging
import random
from abc import ABC, abstractmethod

from battlebots.core.action import (
    Action,
    LightDamageAction,
    HeavyDamageAction,
    HealAction,
    WaitAction,
)
from battlebots.core.state import State

logger = logging.getLogger(__name__)


class Strategy(ABC):
    @abstractmethod
    def evaluate(self, player_name: str, state: State) -> Action:
        raise NotImplementedError


class DummyStrategy(Strategy):
    def evaluate(self, player_name: str, state: State) -> Action:
        other_players = [name for name in state.players if name != player_name]
        random_player = random.choice(other_players)
        return LightDamageAction(player_name, random_player)


class CliPlayerStrategy(Strategy):
    def evaluate(self, player_name: str, state: State) -> Action:
        other_players = [name for name in state.players if name != player_name]
        logger.info("%s", state.report())

        desired_action = None
        failures = 0

        while desired_action is None:
            desired_action = input(
                "Select an action [light_damage, heavy_damage, heal, wait]: "
            )

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

                    return LightDamageAction(player_name, desired_target)

                case "heavy_damage":
                    desired_target = None
                    while desired_target is None:
                        desired_target = input(
                            f"Select a player to damage: {other_players}"
                        )
                        if desired_target not in other_players:
                            logger.error("%s is not a valid player!", desired_target)
                            desired_target = None

                    return HeavyDamageAction(player_name, desired_target)

                case "heal":
                    return HealAction(player_name)

                case "wait":
                    return WaitAction(player_name)

                case _:
                    if failures < 10:
                        logger.error("%s is not a valid action!", desired_action)
                        desired_action = None
                    else:
                        raise ValueError(
                            f"{desired_action} is not a valid action! (failed 10 times)"
                        )
        return None
