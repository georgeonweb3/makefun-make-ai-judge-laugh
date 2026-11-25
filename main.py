#!/usr/bin/env python3
"""Make the AI Judge Laugh — make.fun entry.

Writes one line to /output/entry.txt:

    Our manager calls the 4:55 Friday meeting 'a quick sync', and by
    6:30 the cleaner is hoovering around our chairs while we just lift
    our feet.

The joke: a manager's euphemism ("a quick sync") collides with the
reality of a Friday meeting that runs to 6:30, and the punch is the
whole room silently lifting its feet for the cleaner — a small,
shared defeat everyone in an office recognises. Three beats
(euphemism / late hour / cleaner), three anchors (4:55 Friday,
6:30, the cleaner), ends on the concrete image "lift our feet".

Winner of a blind pairwise tournament (6 candidates, 15 pairs,
fresh Gemini judge): tied top with 4 wins, then won the tiebreak
against the runner-up in both label orders. Extra-mile pass
compared it with the leaderboard top and kept it exactly as judged:
the field's dominant angle is the domestic/family anecdote and the
office stock lines ("this meeting could have been an email",
printer, coffee) — this line uses none of them.

Python 3.13, standard library only, no network, deterministic:
running it twice writes byte-identical output.
"""

import os

ENTRY = (
    "Our manager calls the 4:55 Friday meeting 'a quick sync', and by "
    "6:30 the cleaner is hoovering around our chairs while we just lift "
    "our feet."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# Gate from the competition's own kit (competition.yaml): entry.txt
# must be UTF-8 text of 1 to 200 characters, not only whitespace.
MAX_CHARS = 200


def main() -> None:
    # Gate self-check: /output/entry.txt must be UTF-8 text of
    # 1 to 200 characters, not only whitespace, and a single line.
    # Verified live: 141 characters, one line, no trailing newline.
    assert 1 <= len(ENTRY) <= MAX_CHARS, (
        f"entry is {len(ENTRY)} chars, gate wants 1-{MAX_CHARS}"
    )
    assert "\n" not in ENTRY and "\r" not in ENTRY, "entry must be a single line"
    assert ENTRY.strip(), "entry must not be only whitespace"
    assert ENTRY == ENTRY.strip(), "entry must not start or end with whitespace"
    assert ENTRY.encode("utf-8").decode("utf-8") == ENTRY
    # No control characters: the gate reads the file as text, and a
    # stray control byte would make the line unreadable aloud.
    assert all(ord(ch) >= 32 or ch in "\t" for ch in ENTRY), (
        "entry must not contain control characters"
    )
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(ENTRY.encode("utf-8"))
    # Read-back verification: the graded artifact is the file on
    # disk, not the string in memory — confirm the bytes landed.
    # No randomness, no clock, no I/O beyond the one write, so a
    # second run reproduces the same 141 bytes exactly.
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    assert written == ENTRY.encode("utf-8"), (
        f"entry.txt on disk differs from ENTRY: {written!r}"
    )


if __name__ == "__main__":
    main()
