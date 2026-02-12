import json
from typing import Any


def parse_indented_output(
    text: str,
    *,
    indent: str = "\t",
    list_markers: str = "*-",
) -> dict[str, Any]:
    """
    Parse indented terminal output into a nested dict.

    Handles:
    - "key: value" → key-value
    - "key:" (empty) → nested section
    - "* item" or "- item" → list items under current section

    Args:
        text: Raw output (e.g. from subprocess, file)
        indent: Indent unit; one occurrence = one level. Default "\\t".
                 Use "  " or "    " for space-indented output.
        list_markers: Characters that start a list item. Default "*-" (iw, YAML).

    Returns:
        Nested dict; lists use key "_items".
    """
    lines = [l for l in text.split("\n") if l.strip()]
    root = {}
    stack = [(0, root)]

    def _indent_level(line: str) -> int:
        leading = line[: len(line) - len(line.lstrip())]
        if not leading:
            return 0
        if indent == "\t":
            return leading.count("\t")
        # Spaces: count full indent units
        return len(leading) // len(indent) if indent else 0

    for line in lines:
        level = _indent_level(line)
        content = line.strip()

        while len(stack) > 1 and stack[-1][0] >= level:
            stack.pop()
        cur = stack[-1][1]

        if content and content[0] in list_markers:
            cur.setdefault("_items", []).append(content[1:].strip())
        elif ":" in content:
            key, _, val = content.partition(":")
            key, val = key.strip(), val.strip()
            if val:
                cur[key] = val
            else:
                cur[key] = {}
                stack.append((level, cur[key]))
        else:
            cur[content] = {}
            stack.append((level, cur[content]))

    return root


def to_json(d: dict, **kwargs) -> str:
    """Serialize parsed output to JSON. Pass kwargs to json.dumps (e.g. indent=2)."""
    return json.dumps(d, **kwargs)