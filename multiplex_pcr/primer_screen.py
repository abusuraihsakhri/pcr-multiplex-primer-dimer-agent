"""Sequence-based heuristic screen for contiguous antiparallel primer complementarity.

This is NOT a thermodynamic ΔG, melting-temperature, specificity, or PCR
performance model. Laboratory validation and established primer-design tools
are required before using a panel experimentally.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Mapping, Sequence

_DNA = re.compile(r"^[ACGT]+$")
_COMPLEMENT = str.maketrans("ACGT", "TGCA")
MAX_PRIMERS = 100
MAX_LENGTH = 80


def reverse_complement(sequence: str) -> str:
    return sequence.translate(_COMPLEMENT)[::-1]


def complementarity(first: str, second: str) -> Dict[str, Any]:
    """Longest contiguous complementary stretch in every antiparallel offset.

    three_prime_run denotes the longest run touching the 3' end of EITHER
    primer. It does not model mismatch energetics or gapped alignments.
    """
    reversed_second = reverse_complement(second)
    longest = 0
    three_prime = 0
    for offset in range(1 - len(second), len(first)):
        start = max(0, offset)
        stop = min(len(first), offset + len(second))
        run = 0
        run_start = start
        for i in range(start, stop):
            if first[i] == reversed_second[i - offset]:
                if run == 0:
                    run_start = i
                run += 1
                longest = max(longest, run)
                if i == len(first) - 1 or run_start == offset:
                    three_prime = max(three_prime, run)
            else:
                run = 0
    if three_prime >= 5 or longest >= 9:
        risk = "high"
    elif three_prime >= 4 or longest >= 7:
        risk = "moderate"
    else:
        risk = "low"
    return {
        "longest_run": longest,
        "three_prime_run": three_prime,
        "risk": risk,
    }


def screen_primers(primers: Sequence[Mapping[str, str]]) -> Dict[str, Any]:
    """Screen an ordered list of named DNA primers; include homodimers.

    Limits bound the quadratic number of pairwise comparisons. Names must be
    unique (case-insensitive), and sequences must be unambiguous DNA.
    """
    if not 1 <= len(primers) <= MAX_PRIMERS:
        raise ValueError(f"Provide 1–{MAX_PRIMERS} primers.")
    clean: List[Dict[str, Any]] = []
    names = set()
    for position, primer in enumerate(primers, 1):
        name = str(primer.get("name", "")).strip()
        sequence = str(primer.get("sequence", "")).strip().upper()
        if not name or len(name) > 80 or any(c in name for c in "\r\n\t"):
            raise ValueError(f"Primer {position}: name must contain 1–80 characters.")
        if name.casefold() in names:
            raise ValueError(f"Duplicate primer name: {name}")
        names.add(name.casefold())
        if not 4 <= len(sequence) <= MAX_LENGTH or not _DNA.fullmatch(sequence):
            raise ValueError(
                f"Primer {position}: sequence must contain 4–{MAX_LENGTH} unambiguous A/C/G/T bases."
            )
        clean.append({
            "name": name,
            "sequence": sequence,
            "length": len(sequence),
            "gc_percent": round(100 * (sequence.count("G") + sequence.count("C")) / len(sequence), 1),
        })

    pairs = []
    summary = {"low": 0, "moderate": 0, "high": 0}
    for i, p in enumerate(clean):
        for q in clean[i:]:
            result = complementarity(p["sequence"], q["sequence"])
            summary[result["risk"]] += 1
            pairs.append({"primer_a": p["name"], "primer_b": q["name"], **result})
    return {
        "method": "Ungapped contiguous antiparallel complementarity heuristic (not ΔG)",
        "thresholds": {"moderate": "3′ ≥4 or longest ≥7 nt", "high": "3′ ≥5 or longest ≥9 nt"},
        "primers": clean,
        "pairs": pairs,
        "risk_summary": summary,
    }
