#!/usr/bin/env python3
# =============================================================================
# SENSITIVITY ANALYSIS — State-Capacity Attenuation and Cooperative-Equilibrium
# Breakdown, "Institutional Agency in Asymmetric Rivalries"
#
# This script is fully self-contained and does not import from SM.3. It
# reuses the same hardcoded Government Effectiveness (GE) series so the two
# scripts can be run and verified independently.
#
# Requirements: numpy (no other dependencies).
# =============================================================================

"""
SM.4 Sensitivity Analysis
==========================

Purpose: quantify how the qualitative claim in Sections 6.4/6.6 — that the
cooperative equilibrium becomes infeasible at historically low levels of
Government Effectiveness (GE), "most notably the 2015 trough" — depends on
where exactly the illustrative parameters tau (transparency penalty) and
kappa (opacity-delivery premium) sit within the ranges already stated in
the main text (tau in [0.20, 0.25], kappa in [0.05, 0.08]).

Model recap (Section 6.4): tau_effective = tau_design * f(GE), where
f(GE) in [0,1] is a state-capacity attenuation function. Cooperation is
feasible only if tau_effective > kappa, i.e. f(GE) > kappa/tau_design.

The main text does not specify f(.) beyond "linear attenuation." This
script adopts f(GE) = GE/100, the simplest linear form and the same
percentile-to-unit-interval convention the paper already uses for the
baseline stability index S0 (Sections 3.1, 6.3). This is an illustrative
choice made to operationalize the sensitivity check, not a claim derived
from or asserted by the main text. Under this specification the breakeven
threshold is:

    GE* = 100 * kappa / tau

Cooperation is feasible for GE > GE*, infeasible for GE <= GE*.

IMPORTANT — scope: as with the main text and SM.2/SM.3, only the ordinal
and structural claims are load-bearing. The cardinal thresholds computed
below are illustrative sensitivity diagnostics, not point estimates of a
"true" breakdown level. The purpose of this script is precisely to show
how much the specific numerical story (e.g. "2015 alone is infeasible")
depends on where tau and kappa sit within their stated ranges, rather than
to assert a single calibration as correct.
"""

import numpy as np

# -----------------------------------------------------------------------------
# 1. Data — same Government Effectiveness series as SM.3 Table 1, column GE
# -----------------------------------------------------------------------------

ge_by_year = {
    2002: 30.98, 2003: 30.80, 2004: 37.39, 2005: 33.43, 2006: 31.25,
    2007: 32.93, 2008: 31.58, 2009: 36.03, 2010: 37.87, 2011: 35.86,
    2012: 29.77, 2013: 30.89, 2014: 33.93, 2015: 28.72, 2016: 32.25,
    2017: 33.30, 2018: 33.56, 2019: 29.73, 2020: 31.38, 2021: 32.94,
    2022: 32.78, 2023: 34.93, 2024: 34.14,
}

ge_min_year = min(ge_by_year, key=ge_by_year.get)
ge_max_year = max(ge_by_year, key=ge_by_year.get)
ge_min, ge_max = ge_by_year[ge_min_year], ge_by_year[ge_max_year]

print("=" * 78)
print("SM.4 SENSITIVITY ANALYSIS — State-capacity breakdown threshold GE*")
print("=" * 78)
print(f"Historical GE range: {ge_min:.2f} ({ge_min_year}) to {ge_max:.2f} ({ge_max_year})")
print()

# -----------------------------------------------------------------------------
# 2. Illustrative parameter grid (values as stated in main text Section 6.3)
# -----------------------------------------------------------------------------

tau_grid = [0.200, 0.225, 0.250]
kappa_grid = [0.050, 0.065, 0.080]

print("-" * 78)
print("Breakeven threshold GE* = 100*kappa/tau, and years falling below it")
print("-" * 78)
print(f"{'tau':>6} {'kappa':>7} {'GE*':>7}  {'# infeasible yrs':>17}  infeasible years")

grid_results = []
for tau in tau_grid:
    for kappa in kappa_grid:
        ge_star = 100.0 * kappa / tau
        infeasible_years = sorted(yr for yr, v in ge_by_year.items() if v < ge_star)
        grid_results.append((tau, kappa, ge_star, infeasible_years))
        yrs_str = ", ".join(str(y) for y in infeasible_years) if infeasible_years else "(none — feasible in every observed year)"
        print(f"{tau:6.3f} {kappa:7.3f} {ge_star:7.2f}  {len(infeasible_years):17d}  {yrs_str}")

# -----------------------------------------------------------------------------
# 3. Corner cases — the two extremes of the illustrative grid
# -----------------------------------------------------------------------------

print()
print("-" * 78)
print("Corner cases")
print("-" * 78)

tau_hi, kappa_hi = 0.200, 0.080   # largest GE* -> hardest to satisfy
tau_lo, kappa_lo = 0.250, 0.050   # smallest GE* -> easiest to satisfy

for tau, kappa, label in [
    (tau_hi, kappa_hi, "Hardest case (tau=0.20, kappa=0.08)"),
    (tau_lo, kappa_lo, "Easiest case (tau=0.25, kappa=0.05)"),
]:
    ge_star = 100.0 * kappa / tau
    infeasible_years = sorted(yr for yr, v in ge_by_year.items() if v < ge_star)
    print(f"{label}: GE* = {ge_star:.2f}")
    if not infeasible_years:
        print("  -> Every historically observed year (2002-2024) is feasible.")
    elif len(infeasible_years) == len(ge_by_year):
        print("  -> Every historically observed year (2002-2024) is infeasible,")
        print(f"     including the historical maximum ({ge_max:.2f} in {ge_max_year}).")
    else:
        print(f"  -> {len(infeasible_years)} of {len(ge_by_year)} years infeasible: {infeasible_years}")

# -----------------------------------------------------------------------------
# 4. The narrow band under which 2015 is the *unique* infeasible year
# -----------------------------------------------------------------------------

sorted_ge = sorted(ge_by_year.items(), key=lambda kv: kv[1])
lowest, second_lowest = sorted_ge[0], sorted_ge[1]

print()
print("-" * 78)
print("Band isolating 2015 as the unique historically infeasible year")
print("-" * 78)
print(f"Lowest GE:        {lowest[1]:.2f} ({lowest[0]})")
print(f"Second-lowest GE: {second_lowest[1]:.2f} ({second_lowest[0]})")
print(f"For 2015 alone to fall below GE* while every other year remains at or")
print(f"above it, GE* (equivalently kappa/tau) must satisfy:")
print(f"  {lowest[1]:.2f} < GE* <= {second_lowest[1]:.2f}")
print(f"  {lowest[1]/100:.4f} < kappa/tau <= {second_lowest[1]/100:.4f}")
print()
print("This band sits roughly at the midpoint of the illustrative grid")
print("(e.g. tau=0.225, kappa=0.065 gives GE*=28.89, inside the band).")
print("It is a real but narrow portion of the stated tau/kappa ranges, not")
print("their full extent -- see the grid and corner cases above.")

# -----------------------------------------------------------------------------
# 5. Summary
# -----------------------------------------------------------------------------

print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("Across the full illustrative (tau, kappa) grid stated in Section 6.3,")
print("the breakeven threshold GE* ranges from 20.0 to 40.0 percentile points.")
print("The historically observed GE series (28.72-37.87) spans a narrower band,")
print("so the qualitative claim that low state capacity can break the")
print("cooperative equilibrium is well supported in general, but the specific")
print("claim that 2015 alone is the exceptional infeasible year holds only for")
print("a limited sub-range of the stated illustrative parameters, not for the")
print("full stated range. This finding is reported for transparency; per the")
print("paper's scope conditions, no single (tau, kappa) pair within the")
print("illustrative range is treated as load-bearing.")