#!/usr/bin/env python3
"""Estimate one claim from five person-supplied plan numbers."""

import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


CENT = Decimal("0.01")
ARGUMENTS = (
    "charge",
    "allowed amount",
    "deductible remaining",
    "plan share percent",
    "out-of-pocket remaining",
)


def refuse(message):
    print(f"error: {message}", file=sys.stderr)
    return 2


def parse_numbers(values):
    if len(values) != len(ARGUMENTS):
        raise ValueError(
            "provide charge, allowed amount, deductible remaining, "
            "plan share percent, and out-of-pocket remaining"
        )
    numbers = []
    for label, value in zip(ARGUMENTS, values):
        try:
            number = Decimal(value)
        except InvalidOperation as error:
            raise ValueError(f"{label} must be a number") from error
        if not number.is_finite():
            raise ValueError(f"{label} must be a finite number")
        if number < 0:
            raise ValueError(f"{label} cannot be negative")
        numbers.append(number)
    if numbers[3] > 100:
        raise ValueError("plan share percent must be from 0 to 100")
    return numbers


def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def estimate(values):
    charge, allowed, deductible_remaining, plan_share, oop_remaining = values
    charge = money(charge)
    allowed = money(allowed)
    deductible_remaining = money(deductible_remaining)
    oop_remaining = money(oop_remaining)

    covered_base = min(charge, allowed)
    deductible_applied = min(
        covered_base,
        deductible_remaining,
        oop_remaining,
    )
    covered_after_deductible = covered_base - deductible_applied
    ordinary_person_coinsurance = money(
        covered_after_deductible * (Decimal("100") - plan_share) / Decimal("100")
    )
    oop_space_after_deductible = oop_remaining - deductible_applied
    person_coinsurance = min(
        ordinary_person_coinsurance,
        oop_space_after_deductible,
    )
    plan_payment = covered_after_deductible - person_coinsurance
    tracked_person_cost = deductible_applied + person_coinsurance

    return (
        deductible_applied,
        plan_payment,
        charge - plan_payment,
        deductible_remaining - deductible_applied,
        oop_remaining - tracked_person_cost,
    )


def main(argv=None):
    values = sys.argv[1:] if argv is None else argv
    try:
        numbers = parse_numbers(values)
    except ValueError as error:
        return refuse(str(error))

    labels = (
        "amount applied to deductible",
        "plan expected payment",
        "person expected cost",
        "remaining deductible",
        "remaining out-of-pocket",
    )
    for label, value in zip(labels, estimate(numbers)):
        print(f"{label}: {money(value):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
