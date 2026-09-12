import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override, Literal

from battlebots.core.state import State

logger = logging.getLogger(__name__)


ActionType = Literal["light_damage", "heavy_damage", "heal", "wait"]


class Constraint(ABC):
    @abstractmethod
    def constraint_satisfied(self, state: State) -> tuple[bool, str | None]:
        raise NotImplementedError


class Effect(ABC):
    @abstractmethod
    def execute(self, state: State):
        raise NotImplementedError


@dataclass(kw_only=True)
class Action:
    name: ActionType
    actor: str
    effects: list[Effect]
    constraints: list[Constraint]

    def validate_constraints(self, state: State) -> bool:
        can_execute = True
        reasons = []

        for constraint in self.constraints:
            is_constraint_met, reason = constraint.constraint_satisfied(state)
            can_execute &= is_constraint_met
            if not is_constraint_met:
                reasons.append(reason)

        if not can_execute:
            logger.info(
                "%s is unable to execute action %s for following reasons:\n %s",
                self.actor,
                self.name,
                "\n".join([f"- {reason}" for reason in reasons]),
            )

        return can_execute

    def execute(self, state: State):
        if self.validate_constraints(state):
            logger.info("%s is executing %s", self.actor, self.name)
            for effect in self.effects:
                effect.execute(state)


@dataclass(kw_only=True)
class ConsumeEnergyEffect(Effect):
    actor: str
    energy_consumed: int

    @override
    def execute(self, state: State):
        logger.info(
            "%s consuming %d energy for action", self.actor, self.energy_consumed
        )
        state.players[self.actor].drain_energy(self.energy_consumed)


@dataclass(kw_only=True)
class DamageEffect(Effect):
    actor: str
    target: str
    damage: int

    @override
    def execute(self, state: State):
        logger.info("%s damaging %s for %d HP", self.actor, self.target, self.damage)
        state.players[self.target].damage(self.damage)


@dataclass(kw_only=True)
class HealEffect(Effect):
    actor: str
    heal_amount: int

    @override
    def execute(self, state: State):
        logger.info("%s healing %d HP", self.actor, self.heal_amount)
        state.players[self.actor].heal(self.heal_amount)


@dataclass(kw_only=True)
class WaitEffect(Effect):
    actor: str

    @override
    def execute(self, state: State):
        logger.info("%s is waiting", self.actor)
        return


@dataclass(kw_only=True)
class EnergyConstraint(Constraint):
    actor: str
    energy_consumed: int

    @override
    def constraint_satisfied(self, state: State) -> tuple[bool, str]:
        actual_energy_points = state.players[self.actor].energy_points
        return (
            actual_energy_points >= self.energy_consumed,
            f"{self.actor} requires {self.energy_consumed} EP, has {actual_energy_points}",
        )


def build_action(
    action: ActionType, actor: str, *, target: str | None = None
) -> Action:
    match action:
        case "wait":
            return Action(
                name=action,
                actor=actor,
                effects=[WaitEffect(actor=actor)],
                constraints=[],
            )
        case "light_damage":
            if target is None:
                raise ValueError(f"Must specify target for action {action}")

            return Action(
                name=action,
                actor=actor,
                effects=[
                    DamageEffect(
                        actor=actor,
                        target=target,
                        damage=20,
                    ),
                    ConsumeEnergyEffect(actor=actor, energy_consumed=10),
                ],
                constraints=[EnergyConstraint(actor=actor, energy_consumed=10)],
            )
        case "heavy_damage":
            if target is None:
                raise ValueError(f"Must specify target for action {action}")

            return Action(
                name=action,
                actor=actor,
                effects=[
                    DamageEffect(
                        actor=actor,
                        target=target,
                        damage=40,
                    ),
                    ConsumeEnergyEffect(actor=actor, energy_consumed=20),
                ],
                constraints=[EnergyConstraint(actor=actor, energy_consumed=20)],
            )
        case "heal":
            return Action(
                name=action,
                actor=actor,
                effects=[
                    HealEffect(actor=actor, heal_amount=30),
                    ConsumeEnergyEffect(actor=actor, energy_consumed=20),
                ],
                constraints=[EnergyConstraint(actor=actor, energy_consumed=50)],
            )
        case _:
            raise ValueError("Unknown action: {action}")
