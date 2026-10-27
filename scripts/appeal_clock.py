#!/usr/bin/env python3
"""Calculate planning dates for a private-plan denial notice."""

import argparse
import calendar
import sys
from datetime import date, timedelta


# 180 days: https://www.law.cornell.edu/cfr/text/29/2560.503-1,
# paragraph (h)(3)(i), and for individual coverage
# https://www.law.cornell.edu/cfr/text/45/147.136, paragraph (b)(3)(i),
# read 2026-10-27.
APPEAL_DAYS = {"employer": 180, "individual": 180}

# 4 months: https://www.law.cornell.edu/cfr/text/45/147.136,
# paragraph (d)(2)(ii), read 2026-10-27.
EXTERNAL_REVIEW_MONTHS = {"employer": 4, "individual": 4}


def iso_date(value):
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD")
    return parsed


def add_calendar_months(value, months):
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notice_date", type=iso_date)
    parser.add_argument(
        "plan_type", choices=("employer", "individual", "government")
    )
    parser.add_argument("--received-date", type=iso_date)
    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_args(argv)
    if arguments.plan_type == "government":
        print(
            "government plans use program-specific review periods; no date calculated",
            file=sys.stderr,
        )
        return 2

    basis = arguments.received_date or arguments.notice_date
    appeal_by = basis + timedelta(days=APPEAL_DAYS[arguments.plan_type])
    external_by = add_calendar_months(
        basis, EXTERNAL_REVIEW_MONTHS[arguments.plan_type]
    )

    print(f"basis date: {basis.isoformat()}")
    print(f"appeal-by date: {appeal_by.isoformat()}")
    print(f"external review request-by date: {external_by.isoformat()}")
    print("The insurer's letter controls where it states a different deadline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
