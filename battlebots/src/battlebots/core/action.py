import logging
from abc import ABC
from dataclasses import dataclass
from typing import override

from battlebots.core.state import State

logger = logging.getLogger(__name__)


@dataclass
class Action(ABC):
    actor: str
    target: str | None

    def execute(self, state: State):
        raise NotImplementedError


class LightDamageAction(Action):
    DAMAGE_VALUE = 20
    ACTION_DRAIN = 10

    @override
    def execute(self, state: State):
        logger.info(
            "%s damaging %s for %d HP", self.actor, self.target, self.DAMAGE_VALUE
        )
        state.players[self.target].damage(self.DAMAGE_VALUE)
        state.players[self.actor].drain_energy(self.ACTION_DRAIN)


class HeavyDamageAction(Action):
    DAMAGE_VALUE = 40
    ACTION_DRAIN = 20

    @override
    def execute(self, state: State):
        logger.info(
            "%s damaging %s for %d HP", self.actor, self.target, self.DAMAGE_VALUE
        )
        state.players[self.target].damage(self.DAMAGE_VALUE)
        state.players[self.actor].drain_energy(self.ACTION_DRAIN)


class HealAction:
    HEAL_VALUE = 50
    ACTION_DRAIN = 50

    @override
    def execute(self, state: State):
        logger.info("%s healing for %s HP", self.actor, self.HEAL_VALUE)
        state.players[self.actor].heal(self.HEAL_VALUE)
        state.players[self.actor].drain_energy(self.ACTION_DRAIN)


class WaitAction(Action):
    @override
    def execute(self, state: State):
        logger.info("%s waiting", self.actor)
