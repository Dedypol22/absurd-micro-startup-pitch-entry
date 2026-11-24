#!/usr/bin/env python3
"""NapSaaS: a lazy agent that attends your meetings so you can nap.

Your boss pays for a warm body on the call. NapSaaS supplies one that
never sleeps on the job — because it is not the one sleeping. It joins
your Zoom meetings on mute, nods on camera at the right moments, and
bills your boss $5 an hour for looking busy while you nap. This program
delivers that one-sentence pitch as a single line, written to entry.txt
in the output directory and echoed to stdout.
"""

import os
import sys

# The pitch itself: one sentence, absurdly specific, with a buyer, a
# price, and a lazy agent doing the work while its human naps.
PITCH = (
    "NapSaaS: an agent that attends your Zoom meetings on mute, nods on "
    "camera, and bills your boss $5 an hour for looking busy while you nap."
)


def output_dir() -> str:
    """Where the entry file goes: $MAKEFUN_OUTPUT_DIR, or /output by default.

    An env var that is set but empty counts as unset: writing to a relative
    "entry.txt" in the caller's cwd would silently lose the entry.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main() -> int:
    # Self-check the pitch before anything is written: one line, in the
    # gate's 1-200 character window with room for the trailing newline,
    # and not only whitespace.
    assert "\n" not in PITCH, "pitch must be a single line"
    assert 1 <= len(PITCH) <= 195, "pitch must be 1-195 characters"
    assert PITCH.strip(), "pitch must not be only whitespace"
    # Reject any other control character (tab, carriage return, NUL, ...)
    # by name, so a stray invisible byte fails loudly instead of
    # silently corrupting the single-line deliverable.
    for char in PITCH:
        assert char.isprintable(), (
            f"pitch contains non-printable character U+{ord(char):04X}"
        )
    # No invisible padding at either end: a leading or trailing space
    # would be stripped by some judges and kept by others, so the
    # deliverable must be exactly the visible pitch, nothing more.
    assert PITCH == PITCH.strip(), "pitch must not start or end with whitespace"

    # Build the payload once, so the file and stdout can never disagree
    # about the exact bytes of the pitch.
    text = PITCH + "\n"

    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)

    entry_path = os.path.join(target_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    # Self-check the written file: re-read it and confirm it matches.
    with open(entry_path, "r", encoding="utf-8", newline="\n") as handle:
        assert handle.read() == text, "entry.txt does not match the pitch"

    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
