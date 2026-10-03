---
doc_id: VTR-CAL-001
title: VatReel sizing and first-principles checks
project: VatReel
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First TRL 3 sizing note against every requirement (depth, span, drive, brake, lift, structure, masses, splash, cost)
- version: "0.2"
  date: '2026-10-03'
  author: Amish Chadha
  change: Rerun on the constructable design (VTR-DDR-002); torque tube, guard case, wider shield, extension tube 1.55 m; cost USD 1,437
---

# VatReel sizing and first-principles checks

On paper VatReel does what it is meant to do: every carrier bar comes up above the rim at every working depth, so hides and yarn are loaded and unloaded without a hand in the liquor; the reel turns with about 90 N at the crank with the whole 25 kg wet load on one bar; the lowest bar can be set anywhere from 300 to 1,000 mm below the rim; and the self-locking lift screw holds the reel at any height and lifts every bar clear of the rim. Ten of the twelve requirements are met on paper. R8 (portability) is not met as written: two modules weigh 27.1 and 29.6 kg, so they are two-person carries, and first setup is estimated at about 29 minutes against 15. R6 (corrosion) can only be shown by a coupon test and is at risk for the stainless chain in chloride pickling liquor. The parts cost about USD 1,437 against the USD 1,500 value-engineering target, USD 63 under it.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`). The script reads the geometry from `PARAMS` and `geometry()` in `cad/src/model.py`, takes masses from the model solids and reads prices from `bom/bom.csv`, so the model, the drawing VTR-DWG-001, the BOM and this note agree. All values are first-principles estimates; nothing here is measured.

> **Safety:** VatReel is moving machinery used beside open pits of corrosive and, in dyeing, hot liquor (up to 98 °C (208 °F)). The checks below are paper checks of strength and reach; they do not replace a risk assessment of the site, the pit edge or the process chemistry.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Wet load | 25 kg of hides or yarn with the liquor they carry | R2 |
| Worst case for torque | Whole wet load on one carrier bar level with the axle; buoyancy and drag ignored | Conservative |
| Proof factor | 1.5 x the rated load; stresses held to yield / 1.5 at proof | R5 |
| Pit | 1.0 to 2.5 m wide, at least 1.9 m long, rim level with the floor, liquor 150 mm below the rim | VTR-PRB-001; site survey to confirm |
| Materials | 316L tube and sheet, yield 170 MPa; 316 bar and 304 sections, yield 205 MPa; E = 193 GPa | Minimum 0.2 % proof stresses |
| Chain | ISO 606 08B-1, minimum tensile strength 18.0 kN | Standard |
| Chain stage efficiency | 0.95 per stage including its plain bearings | Typical |
| Axle bearings | Glass-filled PTFE on stainless, friction 0.10 wet | Typical |
| Lift screw | Tr24 x 5 single start, bronze nut, thread friction 0.15 (wet, dirty), thrust ball bearing at the top | Conservative |
| Operator | Eye 1,600 mm high, 1,150 mm behind the near pit edge, at the crank | 1.75 m person |
| Cranking speed | 30 rpm | Steady hand cranking |
| Prices (2026) | 304 stainless USD 4.50/kg, 316 and 316L USD 6.50/kg; bought parts at regional retail estimates | Indicative, not quotes |

## 2. Depth and positions (R1, R4, R11)

The arms swing on the pivot line 200 mm above the rim; the arm angle sets the depth. Every working position keeps the top carrier bar above the rim, which is where loads are hung and taken off.

*Table 2. Arm positions (heights from the rim; + is up; mm).*

| Position | Arm angle below level | Axle height | Lowest bar | Top bar | Reel extends along the pit | Screw length |
| --- | --- | --- | --- | --- | --- | --- |
| Lifted | -33.7 deg | +699 | +149 | +1,249 | 159 to 1,339 | 1,020 |
| Shallowest working | -3.2 deg | +250 | -300 | +800 | 309 to 1,489 | 894 |
| Mid depth (modelled) | +20.0 deg | -108 | -658 | +442 | 256 to 1,436 | 795 |
| Deepest working | +46.2 deg | -450 | -1,000 | +100 | 33 to 1,213 | 704 |

R4 is met: the lowest bar can be set anywhere from 300 to 1,000 mm below the rim. R1 is met on paper: the top bar is 100 to 800 mm above the rim at every working depth, and lifted, every bar is at least 149 mm above it. The model's fit check confirms that nothing collides with the frame or the pit walls at the lifted, shallowest and deepest positions (`python cad/src/model.py --check`).

## 3. Spans (R3)

The pivot tube alone reaches pits 1,000 to 1,220 mm wide; with the extension tube pinned inside it, 1,220 to 2,520 mm. R3 is met. The reel needs a pit at least 1,890 mm long (the pivot 350 mm in from the end wall, plus the reel swing and 50 mm clear); this is added to the assumptions in VTR-REQ-001. The drum is 600 mm long and the far end of the arm frame is 955 mm in from the near edge, so a 1.0 m pit leaves 45 mm clear.

## 4. Drive (R2)

*Table 3. Drive at the worst case.*

| Item | Value |
| --- | --- |
| Load torque on the reel (25 kg at 550 mm) | 134.9 N m |
| Axle bearing friction | 1.3 N m |
| Ratio, chain 1 (15 to 30 teeth) x chain 2 (17 to 51 teeth) | 6.0 |
| Torque on the jackshaft | 47.8 N m |
| Torque on the crank shaft | 25.1 N m |
| Hand force at 280 mm crank radius | **90 N** |
| Chain 1 tension; factor on breaking load at proof | 823 N; 15 |
| Chain 2 tension; factor on breaking load at proof | 1,383 N; 9 |
| At 30 rpm on the crank: reel speed; carrier bar speed; time per turn | 5.0 rpm; 0.29 m/s; 12 s |

R2 is met: 90 N against 100 N in the worst case. With loads spread round the reel the torque is a fraction of this.

## 5. Holding brake (R5)

The ratchet on the crank shaft holds 1.5 x the worst load torque with no credit for chain friction: 33.7 N m on the crank shaft, a tooth force of 602 N, 12.5 MPa bearing on the 8 mm tooth, 5.3 MPa shear in the 12 mm pawl pin, and 6.4 MPa (crank shaft) and 5.4 MPa (jackshaft) in torsion. R5 is met on paper with large margins; the CalRig proof-load test is TRL 4 work.

## 6. Lift screw (R11)

The Tr24 x 5 thread has a lead angle of 4.23 deg against a friction angle of 8.83 deg, so it is self-locking: the reel cannot run down on its own. Its stroke is 316 mm, 63 turns from lifted to deepest.

*Table 4. Lift screw at 1.5 x the load moment.*

| Position | Screw length (mm) | Lever arm (mm) | Moment (N m) | Screw force (N) | Torque (N m) | Handwheel rim force (N) |
| --- | --- | --- | --- | --- | --- | --- |
| Lifted | 1,020 | 214 | 704 | 3,298 | 8.5 | 68 |
| Shallowest | 894 | 250 | 845 | 3,386 | 8.7 | 70 |
| Mid depth | 795 | 233 | 795 | 3,410 | 8.8 | 70 |
| Deepest | 704 | 152 | 586 | 3,847 | 9.9 | 79 |

The screw is in compression; its Euler load at the longest length is 10.5 kN against 3.85 kN (factor 2.7), and the root stress is 14.3 MPa. R11 is met on paper.

## 7. Structure at the proof load

*Table 5. Stresses at 1.5 x, against yield / 1.5.*

| Part | Load case | Stress (MPa) | Yield (MPa) | Factor on yield |
| --- | --- | --- | --- | --- |
| Carrier bar | Whole load spread along one bar, simply supported | 19 | 170 | 9.2 |
| Spoke | Half that load at the tip, no help from the hexagon ties | 106 | 170 | 1.6 |
| Reel axle | Reel and load at mid span plus torque | 43 | 170 | 4.0 |
| Arm | Half the reel and load at its end, arm level | 40 | 170 | 4.3 |
| Torque tube | Far arm's moment carried to the lever | 29 | 170 | 5.8 |
| Jackshaft | Overhang carrying the near bush and the pivot tube plug (242 N m) | 39 | 205 | 5.3 |
| Pivot tube | 2.5 m pit, far bush load between plug and clamp (299 N m) | 25 | 205 | 8.2 |
| Lift screw bracket | 3.85 kN at 255 mm | 118 | 205 | 1.7 |

Every part is within yield / 1.5 at the proof load. The spoke and the bracket have the smallest margins; the spoke figure ignores the ties, which share the load.

## 8. Support

The centre of the reel stays well inside the feet of both stands (451 mm at the lifted position, 577 mm at the deepest). With the reel loaded, the near stand carries 316 to 550 N and the far stand 471 to 237 N across pits 1.0 to 2.5 m wide; both are small loads on a sound rim.

## 9. Masses and setup (R8)

*Table 6. Masses of the parts carried to the pit (kg).*

| Module | Mass | Carry |
| --- | --- | --- |
| Near stand base frame with pads and hooks | 19.5 | One person |
| Bearing tower, bare | 23.2 | One person |
| Shafts, sprockets, chain 1, crank and ratchet (fitted in place) | 16.2 | Several pieces |
| Tower braces | 4.0 | One person |
| Splash shield | 12.1 | One person |
| Lift screw bracket | 3.9 | One person |
| Lift screw with trunnions and handwheel | 8.6 | One person |
| Pivot tube with the arm frame on it | 27.1 | Two people, 13.5 each |
| Extension tube | 6.3 | One person |
| Far stand | 12.4 | One person |
| Chain 2 with its guard | 8.2 | One person |
| Reel with carrier bars and axle sprocket | 29.6 | Two people, 14.8 each |
| **Total** | **171.2** | |

R8 is not met as written: two modules exceed 25 kg, though no person carries more than 23.2 kg. First setup is estimated at 29 minutes over ten steps (`setup_time()` in the script) against 15; moving between pits of the same width is quicker. Both are recorded as decided limits in VTR-DEC-001.

## 10. Splash (R9)

All 156 straight lines checked from the top half of the reel, at four depths and three positions along it, to the operator's eye pass through the splash shield (crossings 89 to 1,427 mm above the rim, inside the shield's 60 to 1,450 mm) or into the near pit wall. R9 is met on paper; droplets do not travel in straight lines, so the indicator paper trial remains the test (TRL 4).

## 11. Heat and corrosion (R6, R7)

*Table 7. Material limits.*

| Material | Where | Limit | Against 98 °C liquor |
| --- | --- | --- | --- |
| 316L stainless | Reel, arms, wetted parts | Well above 98 °C | Met |
| Glass-filled PTFE | Axle bushes in the liquor | About 260 °C | Met |
| UHMW-PE | Bushes above the liquor | About 80 °C continuous | Met if splash only; temperature at the bushes to confirm |
| Polypropylene | Shield sheet | About 100 °C | Met (splash only) |
| EPDM | Pads | About 120 °C | Met |

R7 is met on paper. R6 cannot be shown by calculation: 316L resists lime and sulphide liquors and chrome liquors well, but chloride pickling liquor can pit stainless steel, and the 304 chain 2 is the weakest part. It is marked at risk until the coupon immersion test.

## 12. Cost (R10)

The priced BOM totals USD 1,437. Value-engineering target: USD 1,500. Estimated cost of the constructable design: USD 1,437 (USD 63 under the target).

## 13. Results against the requirements

*Table 8. Requirements on paper.*

| ID | Requirement | Result on paper | Status |
| --- | --- | --- | --- |
| R1 | No hand in the liquor | Top bar 100 to 800 mm above the rim at every working depth; loaded with hooks | Met on paper |
| R2 | Crank force 100 N or less, 25 kg | 90 N worst case | Met |
| R3 | Pits 1.0 to 2.5 m wide | 1.0 to 2.52 m; pit at least 1.89 m long | Met |
| R4 | Lowest carrier 0.3 to 1.0 m deep | 0.30 to 1.00 m, any depth between | Met |
| R5 | Brake holds 1.5 x | Ratchet stresses under 13 MPa; self-locking lift screw | Met on paper |
| R6 | Corrosion, 500 h in three liquors | Material choice only | At risk (chain 2 in pickle) |
| R7 | 98 °C baths | All materials rated | Met on paper |
| R8 | Modules 25 kg or less; setup 15 min | Two modules 27.1 and 29.6 kg (two-person carries); about 29 min | **Not met** |
| R9 | No droplets reach the operator | All sight lines blocked | Met on paper |
| R10 | Cost against the USD 1,500 target | USD 1,437 | USD 63 under the target |
| R11 | Self-locking lift, 100 N or less | 79 N at 1.5 x; self-locking | Met on paper |
| R12 | Moving parts guarded | Chains, sprockets and ratchet enclosed | Met on paper; openings to check |
