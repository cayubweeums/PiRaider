import json
import re
from typing import Any


def parse_indented_output(
    text: str,
    *,
    indent: str = "\t",
    list_markers: str = "*-",
    accumulate_repeated_keys: bool = False,
) -> dict[str, Any]:
    """
    Parse indented terminal output into a nested dict.

    Handles:
    - "key: value" → key-value (prefers ": " separator to avoid splitting MAC addresses)
    - "key:" (empty) → nested section
    - "* item" or "- item" → list items under current section

    Args:
        text: Raw output (e.g. from subprocess, file)
        indent: Indent unit; one occurrence = one level. Default "\\t".
                 Use "  " or "    " for space-indented output.
        list_markers: Characters that start a list item. Default "*-" (iw, YAML).
        accumulate_repeated_keys: If True, repeated keys become lists (for bluetoothctl).

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

    # bluetoothctl: "Controller XX:XX:XX:XX:XX:XX (public)" has colons in MAC
    _controller_re = re.compile(
        r"^Controller ([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}\s+.*)$"
    )

    def _set_key_val(cur: dict, key: str, val: str) -> None:
        if accumulate_repeated_keys and key in cur:
            existing = cur[key]
            if isinstance(existing, list):
                existing.append(val)
            else:
                cur[key] = [existing, val]
        else:
            cur[key] = val

    for line in lines:
        level = _indent_level(line)
        content = line.strip()

        while len(stack) > 1 and stack[-1][0] >= level:
            stack.pop()
        cur = stack[-1][1]

        if content and content[0] in list_markers:
            cur.setdefault("_items", []).append(content[1:].strip())
        elif m := _controller_re.match(content):
            _set_key_val(cur, "Controller", m.group(1).strip())
        elif ": " in content:
            key, _, val = content.partition(": ")
            key, val = key.strip(), val.strip()
            if val:
                _set_key_val(cur, key, val)
            else:
                cur[key] = {}
                stack.append((level, cur[key]))
        elif ":" in content:
            key, _, val = content.partition(":")
            key, val = key.strip(), val.strip()
            if val:
                _set_key_val(cur, key, val)
            else:
                cur[key] = {}
                stack.append((level, cur[key]))
        else:
            cur[content] = {}
            stack.append((level, cur[content]))

    return root


def to_json(d: dict, **kwargs) -> str:
    """Serialize parsed output to JSON. Pass kwargs to json.dumps"""
    return json.dumps(d, **kwargs)