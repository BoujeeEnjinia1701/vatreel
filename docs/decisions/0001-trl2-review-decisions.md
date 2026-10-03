---
doc_id: VTR-DDR-001
title: VatReel TRL 2 review decisions
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
  change: TRL 2 review decisions made under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** accepted
- **Decided by:** Amish Chadha, by pre-approval: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost."

## Context

The TRL 2 review (`docs/REVIEW.md`, TRL 2 section) turned the scaffold's concept, a portable hand-cranked reel set across a pit, into a formulated concept with a massing model and concept media. Formulating it raised the choices below. Under the pre-approval every recommendation is decided rather than left as "Proposed, awaiting Amish". Choices that touch safety take the conservative option and say what evidence would relax it.

## Options considered and decisions

*Table 1. Decisions made on 2026-10-03.*

| # | Item | Options | Decision |
| --- | --- | --- | --- |
| 1 | How the reel spans the pit | (a) reel shaft between end stands on opposite rims, telescoping for 1.0 to 2.5 m; (b) a static telescopic pivot tube across the pit, with the reel on two arms that swing on it | (b): only a static tube telescopes; the reel stays 0.6 m long next to the operator's rim. A turning telescopic shaft would expose a rotating, sliding joint over the pit |
| 2 | Reel axis | (a) along the rim; (b) across the pit, pointing at the operator | (b): the 0.6 m reel fits a 1.0 m wide pit, and its 1.18 m diameter lies along the pit's length (pits at least 1.9 m long) |
| 3 | Depth setting and lift | (a) a lift lever with a pawl quadrant; (b) a self-locking lead screw with a handwheel acting on a lever on the arm frame | (b), the conservative choice: a 55 kg reel and load cannot drop into a hot bath, and the depth can be set anywhere. Evidence that would relax it: a lever with a double pawl proof-loaded to 1.5 x and shown faster in trials |
| 4 | Drive | (a) one chain from crank to reel (crank height changes with depth); (b) two chains, crank to a jackshaft on the pivot line, jackshaft to reel along the arm | (b): the crank stays 1.0 m above the floor at every depth; ratio 6 to 1 |
| 5 | Holding brake | (a) friction band; (b) ratchet and pawl on the crank shaft | (b): positive, no adjustment, holds 1.5 x with large margins |
| 6 | Materials | (a) painted mild steel; (b) 304 frame, 316L for wetted parts; (c) all 316L | (b): 316L wherever liquor reaches; 304 for the frame; glass-filled PTFE bushes in the liquor, UHMW-PE above it. Coupon tests (R6) may move parts between grades |
| 7 | Carriers | (a) spring clip bars; (b) carrier bars with eye tabs and stainless snap hooks; yarn hanks looped over the bars | (b): no springs in the liquor; hides toggled through a punched hole at one edge, the usual tannery practice. Workers confirm the method with the first partner |
| 8 | Guarding | (a) guard only the crank end; (b) enclose both chains, the sprockets and the ratchet | (b), conservative: chain 1 inside the tower, chain 2 in a closed case, ratchet under a cover. R12 added. Evidence to relax: none expected |
| 9 | Hot baths | (a) one operator; (b) two people present whenever the bath is above 60 °C | (b), conservative operating rule written into the build plan's safety stops. Evidence to relax: trials showing no scald exposure at the crank position |
| 10 | Shared blocks | (a) adopt the proposed hand capstan block; (b) VatReel's own chain drive; CalRig for the proof load | (b): the capstan block assumes a fixed drum; CalRig is the first candidate for the R5 test at TRL 4 |
| 11 | Requirements | Keep R1 to R10; add a lift requirement and a guarding requirement | R11 (self-locking lift, 100 N at the handwheel, every bar above the rim) and R12 (guarding) added; pit length of 1.9 m added to the assumptions |
| 12 | First co-design partner | Tannery cluster association; worker health NGO; craft-dyeing cooperative | First candidate to approach: a worker health NGO or tannery association in the Kanpur leather cluster, India. A candidate, not an agreed partner |
| 13 | Value-engineering target | Keep USD 1,500 | Kept; `budget_usd` unchanged. Cost overruns are accepted by the pre-approval |

## Consequences

- VTR-PRC-001, VTR-REQ-001 and VTR-PRB-001 move to v0.2 with these decisions; the TRL 2 concept media are drawn from the massing model.
- The TRL 3 calculations (VTR-CAL-001) size the arm, drive, lift screw and frame; making the design constructable is recorded in VTR-DDR-002.
- No TRL 4 work (building, testing, test plans or purchasing lists) follows from this record.

> **Safety:** Items 3, 8 and 9 are safety choices and take the conservative option. The design is an open engineering reference, not certified equipment.
