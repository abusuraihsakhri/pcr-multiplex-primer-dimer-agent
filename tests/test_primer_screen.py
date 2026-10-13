"""Regression tests for the sequence complementarity heuristic."""
import pytest
from multiplex_pcr.primer_screen import complementarity, reverse_complement, screen_primers


def test_reverse_complement():
    assert reverse_complement("ACGT") == "ACGT"
    assert reverse_complement("AAGC") == "GCTT"


def test_complementary_ends_flagged():
    result = complementarity("TTTTAAAAA", "TTTTTCCCC")
    assert result["three_prime_run"] >= 5
    assert result["risk"] == "high"


def test_no_false_dimer_for_homopolymer():
    result = complementarity("AAAAAAAA", "AAAAAAAA")
    assert result["longest_run"] == 0
    assert result["risk"] == "low"


def test_symmetry_and_self_dimer():
    a, b = "ACGATCCG", "CGGATCGT"
    assert complementarity(a, b) == complementarity(b, a)
    result = screen_primers([{"name": "P1", "sequence": "ACGTACGT"}])
    assert len(result["pairs"]) == 1
    assert result["pairs"][0]["primer_a"] == "P1"


def test_validation_and_matrix_size():
    with pytest.raises(ValueError, match="Duplicate"):
        screen_primers([{"name": "A", "sequence": "ACTG"}, {"name": "a", "sequence": "ACGT"}])
    for seq in ("ACGN", "", "A" * 81):
        with pytest.raises(ValueError):
            screen_primers([{"name": "A", "sequence": seq}])
    with pytest.raises(ValueError):
        screen_primers([])
    out = screen_primers([
        {"name": "F", "sequence": "ACTGTGAC"},
        {"name": "R", "sequence": "TCACAGTG"},
        {"name": "X", "sequence": "ACCTACGT"},
    ])
    assert len(out["pairs"]) == 6
    assert sum(out["risk_summary"].values()) == 6
