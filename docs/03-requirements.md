---
doc_id: VTR-REQ-001
title: VatReel requirements
project: VatReel
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 review; targets confirmed under Amish's pre-approval (VTR-DDR-001); R11 lift and R12 guarding added; concept status for each requirement
- version: "0.3"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 3 status on paper from VTR-CAL-001 for the constructable design; pit length added to the assumptions; R10 against the value-engineering target
---

# VatReel requirements

Twelve measurable requirements. The status column gives the result on paper from the calculation note VTR-CAL-001 on the constructable design; every requirement is verified by test at TRL 4 or later. Ten are met on paper, R6 (corrosion) is at risk and R8 (portability) is not met as written.

*Table 1. Requirements.*

| ID | Requirement | Target | Verification (TRL 4 or later) | Status on paper (VTR-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Operator loads, runs and unloads a batch without any hand entering the liquor | 0 hand contacts with liquor per batch | Observed trial with workers over at least 10 batches | Met on paper: the top carrier bar is 100 to 800 mm above the rim at every working depth; loading with long hooks |
| R2 | Handle force to turn the loaded reel | 100 N (22 lbf) or less with a 25 kg (55 lb) wet load | Spring balance at the handle on a water-filled test tank | Met: 90 N with the whole load on one bar |
| R3 | Width of pits and vats served | 1.0 to 2.5 m (3 to 8 ft), adjustable | Fit check on test frames of minimum and maximum width | Met: 1.0 to 2.52 m |
| R4 | Immersion depth of the lowest carrier bar below the rim | Adjustable 0.3 to 1.0 m (1 to 3.3 ft) | Measurement at both settings | Met: any depth from 0.30 to 1.00 m |
| R5 | Holding brake | Holds the rated load at any position with 1.5 times rated load applied, no slip | CalRig proof-load test | Met on paper: ratchet stresses under 13 MPa |
| R6 | Corrosion resistance of wetted parts | No structural corrosion after 500 h immersion in sample liming, pickling and chrome liquors | Coupon immersion test and inspection | At risk: shown only by material choice; stainless chain 2 in chloride pickle is the weak point |
| R7 | Heat tolerance for dye use | Operates in baths up to 98 °C (208 °F) with no deformation of reel or carriers | Hot-bath trial with temperature log | Met on paper: all materials rated |
| R8 | Portability | Each module 25 kg (55 lb) or less; two people set up in 15 min or less | Weigh modules; timed setup trial | **Not met:** two modules 27.1 and 29.6 kg (two-person carries, 14.8 kg each at most); setup about 29 min |
| R9 | Splash control at the crank position | No liquor droplets reaching the operator at normal cranking speed | Indicator paper on the operator's apron during trials | Met on paper: every sight line from the reel to the eye is blocked |
| R10 | Cost | Value-engineering target USD 1,500 for prototype parts | Costed bill of materials | USD 1,437, USD 63 under the value-engineering target |
| R11 | Lift and depth setting | Self-locking: holds the reel at any height with no brake applied; 100 N or less at the handwheel at 1.5 x load; lifts every carrier bar above the rim | Proof-load and handwheel force test | Met on paper: self-locking thread; 79 N; lowest bar 149 mm above the rim when lifted |
| R12 | Guarding of moving parts | Chains, sprockets and ratchet enclosed; no nip point reachable from the operator position | Inspection against ISO 13857 by a competent person | Met on paper by enclosure; openings to check |

## Assumptions

- Pit rims are strong enough to carry the stands and load (under 600 N per stand); to be checked on site.
- Pits are at least 1.9 m (6.2 ft) long so the reel can swing; the arm pivot sits 350 mm in from the pit's end wall.
- The liquor stands about 150 mm below the rim; the rim is level with the floor.
- Hides can be toggled or hooked at one edge and yarn hanks looped over a bar so they stay on the reel as it turns.
- Existing process times and chemistry stay as they are; VatReel changes only how the load moves.
- A reel speed that a person can crank (about 5 rpm) is slow enough for even treatment.

> **Safety:** These requirements cover moving machinery beside open pits of corrosive and hot liquor. Meeting them on paper does not make the design safe to use; gloves, eye protection and boots stay in use, and every site needs its own risk assessment.
