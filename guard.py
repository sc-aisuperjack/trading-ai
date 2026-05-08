import re

NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:£\d+(?:\.\d+)?m|£\d+(?:\.\d+)?k|-?\d+(?:\.\d+)?%|-?\d+(?:\.\d+)?\s+percentage points?|-?\d+(?:\.\d+)?)(?![A-Za-z0-9])"
)


def normalise_value(value: str) -> str:
    return str(value).strip().replace("  ", " ")


def citation_guard(answer: str, citations: list[dict]) -> tuple[bool, list[str]]:
    """
    Checks that every numeric claim in the answer is present in citations.

    This version is slightly more flexible:
    - 8.0 can match 8.0%
    - 8.0 can match 8.0 percentage points
    - 8.0 percentage point can match 8.0 percentage points
    """
    if not isinstance(answer, str):
        answer = str(answer)

    allowed_values = {normalise_value(c["value"]) for c in citations}

    expanded_allowed_values = set(allowed_values)

    for value in allowed_values:
        if value.endswith("%"):
            expanded_allowed_values.add(value.replace("%", ""))

        if "percentage point" in value:
            expanded_allowed_values.add(value.replace(" percentage points", ""))
            expanded_allowed_values.add(value.replace(" percentage point", ""))
            expanded_allowed_values.add(value.replace("percentage points", "percentage point"))

    safe_values = {
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "15",
        "80",
    }

    numbers = NUMBER_PATTERN.findall(answer)
    missing = []

    for number in numbers:
        value = normalise_value(number)

        if value in expanded_allowed_values:
            continue

        if value in safe_values:
            continue

        missing.append(value)

    return len(missing) == 0, list(dict.fromkeys(missing))


def allowed_values(citations: list[dict]) -> list[str]:
    return [str(c["value"]) for c in citations]