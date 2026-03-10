"""Mutable surface for autonomous optimization.

Agent can change this file only.
"""


def candidate_solution(x: float) -> float:
    """Example objective function output.

    The harness will compare this output against a hidden target value.
    """
    # Baseline intentionally simple/suboptimal.
    return (x * 0.8) + 1.5
