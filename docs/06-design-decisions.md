---
doc_id: VTR-DEC-001
title: VatReel design decisions register
project: VatReel
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened; every decision made under Amish's 2026-10-03 pre-approval
---

# VatReel design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list decisions.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The stainless 17 and 51 tooth sprockets come bored 40 and 48.3 with hubs long enough for a roll pin | Sets the jackshaft and axle drilling and the guard case clearance | VTR-DDR-002, change 2 |
| 2 | Pitting of the 304 chain 2 and 316L coupons in the partner's pickling and chrome liquors | R6 is at risk until shown; chain 2 may move to a 316 chain or a polymer drive | VTR-CAL-001, section 11 |
| 3 | The bronze Tr24 x 5 nut bought is single start and runs self-locking on the rod under load | R11 depends on it; a two-start nut would not lock | VTR-CAL-001, section 6 |
| 4 | Running clearance and creep of the glass-filled PTFE axle bushes in 98 °C water | R7; sets the bush bore | VTR-CAL-001, section 11 |
| 5 | Temperature at the UHMW-PE bushes above a hot bath | UHMW-PE is good to about 80 °C; PTFE bushes there if it runs hotter | VTR-CAL-001, section 11 |
| 6 | The first partner's pit: rim strength, width, length (at least 1.9 m), liquor level and end wall | The pivot sits 350 in from the end wall; the stands bear on the rims | VTR-REQ-001, assumptions |
| 7 | How the partner's workers hang hides (toggles through a punched hole) and loop yarn hanks on the bars | Sets the eye tab spacing and the snap hook size | VTR-DDR-001, item 7 |

## Value engineering

Value-engineering target: USD 1,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,437 (USD 63 under the target). Main cost drivers and savings worth trying:

- Stainless is most of the cost: the reel and carrier bars (USD 246), the lift screw set (USD 130) and the bearing tower (USD 125). The frame (base, tower, shield, far stand, tubes) is 304; only parts that enter the liquor are 316L.
- Bought drive parts (sprockets USD 97, chains USD 62, bushes USD 63) are about 15 % of the cost; the stainless pair on the arm costs twice the plated pair in the tower.
- Making the design constructable added about USD 40: the closed chain 2 case, the ratchet cover and the wider splash shield. They are guarding, so savings are sought elsewhere.
- Savings worth trying: a hot-dip galvanized mild steel near stand and far stand where only splash reaches (about USD 120 less, to be weighed against corrosion in lime and acid splash); a bought cast iron handwheel in place of a stainless one; carrier bar end plates cut from offcuts.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | Reel on two arms swinging on a static telescopic pivot tube across the pit, not on a turning shaft between end stands | Amish, pre-approval: "I pre-approve the batch runs along with any recommendations you come up with." | VTR-DDR-001, item 1 |
| 2026-10-03 | Reel axis across the pit, pointing at the operator; reel 1.18 m over the spokes, 0.6 m long; pits at least 1.9 m long | Amish, pre-approval (as above) | VTR-DDR-001, item 2 |
| 2026-10-03 | Self-locking lift screw with a handwheel in place of a free lift lever (safety, conservative) | Amish, pre-approval (as above) | VTR-DDR-001, item 3 |
| 2026-10-03 | Two-stage roller chain drive, 6 to 1, crank fixed 1.0 m above the floor | Amish, pre-approval (as above) | VTR-DDR-001, item 4 |
| 2026-10-03 | Ratchet and pawl on the crank shaft as the holding brake | Amish, pre-approval (as above) | VTR-DDR-001, item 5 |
| 2026-10-03 | 304 frame, 316L wetted parts, PTFE bushes in the liquor, UHMW-PE above it | Amish, pre-approval (as above) | VTR-DDR-001, item 6 |
| 2026-10-03 | Carrier bars with eye tabs and stainless snap hooks; yarn looped over the bars | Amish, pre-approval (as above) | VTR-DDR-001, item 7 |
| 2026-10-03 | Enclose both chains, the sprockets and the ratchet; add R12 (safety, conservative) | Amish, pre-approval (as above) | VTR-DDR-001, item 8 |
| 2026-10-03 | Two people present at any bath above 60 °C (safety, conservative) | Amish, pre-approval (as above) | VTR-DDR-001, item 9 |
| 2026-10-03 | Own chain drive rather than the hand capstan block; CalRig the first candidate for the proof load | Amish, pre-approval (as above) | VTR-DDR-001, item 10 |
| 2026-10-03 | R11 (lift) and R12 (guarding) added; pit length added to the assumptions | Amish, pre-approval (as above) | VTR-DDR-001, item 11 |
| 2026-10-03 | First co-design candidate to approach: a worker health NGO or tannery association in the Kanpur leather cluster, India (not agreed) | Amish, pre-approval (as above) | VTR-DDR-001, item 12 |
| 2026-10-03 | Value-engineering target kept at USD 1,500 | Amish, pre-approval: "I also accept any cost overruns or variations from the assumed scope cost." | VTR-DDR-001, item 13 |
| 2026-10-03 | Design for construction: torque tube, sprocket sizes, closed chain 2 case, ratchet cover, open far saddle with keeper, plug on the jackshaft tip, extension tube and clamp, wider shield and the other changes in VTR-DDR-002 | Amish, pre-approval (as above) | VTR-DDR-002 |
| 2026-10-03 | R8 accepted as not met for the prototype: two modules of 27.1 and 29.6 kg carried by two people (14.8 kg each at most); first setup about 29 minutes | Amish, pre-approval (as above) | VTR-CAL-001, section 9 |
