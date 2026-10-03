---
doc_id: VTR-DDR-002
title: VatReel design for construction
project: VatReel
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Constructability review of the TRL 3 model; every change made under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** accepted
- **Decided by:** Amish Chadha, by pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

Writing the prototype build plan (VTR-BLD-001) means every part must be makeable by the stated process and must fit and fasten to its neighbours (STANDARDS section 18; Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"). The TRL 3 model was checked with build123d: no two components overlap, every joint face touches (a gap of 0.6 mm at most, a sliding fit), and nothing collides with the frame or the pit walls with the arms lifted, at the shallowest and at the deepest setting (`python cad/src/model.py --check`, 45 components). The changes below were needed to get there. None changes what VatReel does, its pitch or its safety case, except to make guarding more complete.

## Decision

*Table 1. Changes from the concept to the constructable design.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| 1 | Arm frame | Two arms joined by a small tie tube 180 mm out from the pivot | Both arms welded to a 76.1 x 3 mm torque tube round the pivot line | The lift screw acts on the near arm only; the tie would have carried the far arm's moment in bending at about 280 MPa. The torque tube carries it in torsion at 29 MPa |
| 2 | Sprockets | 12 teeth on the 30 and 40 mm shafts | 15 and 30 teeth (chain 1), 17 and 51 teeth (chain 2); ratio kept at 6 to 1 | A 12-tooth 08B sprocket cannot be bored to 30 or 40 mm |
| 3 | Chain 2 guard | A flat plate on the wall side | A closed case of 1.5 mm sheet round the chain, on two spacers | The plate left the chain open at its edges (R12) |
| 4 | Bearing tower | Open at the bottom; ratchet exposed | Bottom sheet closes the chain box; a cover over the ratchet and pawl with the release lever outside | Close the last openings to chain 1 and the pawl (R12) |
| 5 | Far bearing | A split block with a bolted cap | An open-topped saddle with a keeper that swings shut | The far bearing is 0.9 m into the pit; the reel must drop in without anyone reaching there |
| 6 | Near bearing | Solid housing | Split block with a bolted cap | The reel is fitted from above, not slid along its axle |
| 7 | Pivot tube support | A bracket from the stand round the chain 2 sprocket | A plug in the tube's near end riding on the jackshaft tip | No bracket can pass the sprocket and the swinging arm; the jackshaft carries it at 39 MPa |
| 8 | Arm frame location | Not set | An inner collar (inside the torque tube) and an outer collar on the pivot tube | Holds the frame along the tube so chain 2 stays in line |
| 9 | Pivot tube reach | One telescopic tube | Pivot tube 1.2 m plus a 1.55 m extension pinned inside it at 100 mm steps; far stand clamps on either through a split sleeve | Spans 1.0 to 2.52 m with no tube end standing out more than about 150 mm |
| 10 | Splash shield | 1.12 m wide, from 260 mm above the rim | 1.32 m wide, from 60 mm, with a hole for the jackshaft | Sight lines from the reel to the operator's eye missed the narrower shield (R9) |
| 11 | Base frame | 1.55 m long | 1.75 m long | Carries the wider shield |
| 12 | Tower braces | Welded to the tower | Bolted, and lowered to clear the ratchet cover | Keeps the tower at 23.2 kg to carry; the braces clashed with the cover |
| 13 | Spiders | Spokes butted to the axle | Spokes on a 40 mm hub sleeve, hexagon ties between them | A joint that can be jigged and welded square |
| 14 | Carrier bars | Bars welded to the spokes | Bars with end plates bolted to the spoke tips; eye tabs for snap hooks | Bars can be replaced; the reel is carried as one piece |
| 15 | Axle sprocket | Hub toward the arm | Hub on the wall side | The hub hit the guard case's inner plate |
| 16 | Loading hooks | Not sized | 1.5 m hooks stored on the base frame's back rail | They must reach the far end of a carrier bar from the near rim |
| 17 | Reel installation | Not worked out | A 3.6 m assembly bar through the hollow axle; two people on opposite rims carry the reel onto the raised arms | No one reaches 0.9 m over the pit |
| 18 | Assembly order | Not worked out | The thirteen steps of VTR-BLD-001 section 4, set by what fits past what | The arm frame must be on the pivot tube before the tube goes onto the jackshaft |

## Consequences

- `cad/src/model.py` holds every change; STEP and STL are regenerated; the general arrangement VTR-DWG-001 moves to Rev P2; the concept media and the build plan pictures are regenerated from the model.
- The parts cost moves to USD 1,437 against the USD 1,500 value-engineering target (USD 63 under). The guard case, cover and wider shield added about USD 40; the BOM lists every part.
- VTR-CAL-001 v0.2 reruns every check on the constructable design; all stresses stay within yield / 1.5 at the proof load.
- R8 is not met as written (two two-person modules, setup about 29 minutes); this is recorded as a decided limit in VTR-DEC-001.
- `design_state: constructable` is set in `project.yaml`.

> **Safety:** Changes 3, 4, 5 and 10 improve guarding and splash protection. The plan's safety stops (VTR-BLD-001 section 6) apply to every step.
