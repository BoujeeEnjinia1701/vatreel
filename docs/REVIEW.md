# Review note: VatReel

## Session 2026-10-03: TRL 1 to TRL 3 under Amish's pre-approval (kit 1.7.0)

Amish Chadha, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Every choice below is therefore decided, not proposed, and recorded in VTR-DDR-001, VTR-DDR-002 and the register VTR-DEC-001. Nothing was built or tested.

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md` from `.kit/CLAUDE.md`; `.kit/PHASE.yaml` as installed).

### TRL 2: concept formulated

**What was done**

- `docs/01-problem.md` (VTR-PRB-001 v0.2): pit length and liquor level added to the environment; first co-design candidate; questions for the site survey; safety note.
- `docs/03-requirements.md` (VTR-REQ-001 v0.2): R1 to R10 confirmed; R11 (self-locking lift) and R12 (guarding) added.
- `docs/02-concept.md` (VTR-PRC-001 v0.2): how it works, components, key design choices, first-order numbers, safety.
- Concept model and media: `cad/src/concept_media.py` generates `media/hero.png`, `media/concept-blueprint.png` and `.pdf`, `media/model.glb`, `media/viewer.html`, `media/cutaway.png`, `media/exploded.png` and `media/flow.png` (drive train; values marked as estimates). The media were regenerated from the TRL 3 constructable model below.
- `bom/bom.csv` with the main components and indicative costs.

**Results.** The scaffold's concept (end stands on opposite rims carrying a reel shaft across the pit, with a lift lever) could not span 1.0 to 2.5 m without a turning telescopic shaft over the pit, and a lift lever could not lift a 55 kg reel and load through the 1.3 m needed. The formulated concept carries the reel on two arms that swing on a static telescopic pivot tube across the pit; a two-stage chain keeps the crank at 1.0 m at every depth; a self-locking screw sets the arm angle.

**Requirements not met at TRL 2.** None identified at concept level; R8 (masses) was flagged for the TRL 3 check.

**Decisions made under the pre-approval (VTR-DDR-001).** Reel on swinging arms; reel axis across the pit; self-locking lift screw in place of a lever (safety, conservative); two-stage chain drive 6 to 1; ratchet brake; 304 frame and 316L wetted parts with PTFE and UHMW-PE bushes; carrier bars with snap hooks; all chains and the ratchet enclosed (safety, conservative); two people at any bath above 60 °C (safety, conservative); own drive, not the hand capstan block, and CalRig as the first proof-load candidate; R11 and R12 added; first co-design candidate a worker health NGO or tannery association in the Kanpur leather cluster (a candidate, not agreed); value-engineering target kept at USD 1,500.

**Safety concerns.** Corrosive and hot liquor, the open pit edge, moving machinery, a 55 kg suspended load over the pit.

### TRL 3: proof of concept on paper

**What was done**

- `docs/04-calcs/01-sizing.md` (VTR-CAL-001 v0.2) and `docs/04-calcs/sizing.py`: depth and positions, spans, drive, brake, lift screw, structure at 1.5 x, support, masses and setup time, splash sight lines, heat and corrosion, cost, results against every requirement.
- `cad/src/model.py`: parametric build123d model, 45 components, with fit checks (`--check`: no overlaps, every joint touching, clear of the frame and pit walls at the lifted, shallowest and deepest positions: PASS). STEP and STL in `cad/step/` and `cad/stl/` (assembly, near arm, far arm, reel, carrier bars, bearing tower, far stand).
- `cad/src/sheets.py`: general arrangement VTR-DWG-001 Rev P2.
- `bom/bom.csv`: 23 lines, every line priced with a supplier type.
- `cad/src/product_model.py` (appearance model) and render scenes for the Mac: hero, exploded and detail exported with `.kit/export_views.py`.
- Constructable design and build plan: `docs/decisions/0002-design-for-construction.md` (VTR-DDR-002), `cad/src/build_plan_media.py`, `docs/05-build-plan.md` (VTR-BLD-001) with 16 making sketches (`cad/drawings/VTR-DWG-101` to `116`), 11 joint close-ups and 13 step pictures in `docs/05-build-plan/`; `docs/06-design-decisions.md` (VTR-DEC-001).
- `project.yaml`: trl 3, trl_target 3, design_state constructable, trl_evidence listing the files. README updated (hero render first, build plan link and section).

**Key results (VTR-CAL-001).**

| Quantity | Value |
| --- | --- |
| Lowest carrier bar below the rim | 300 to 1,000 mm, any depth; top bar 100 to 800 mm above the rim |
| Pits served | 1.0 to 2.52 m wide, at least 1.89 m long |
| Crank force, 25 kg on one bar | 90 N (R2 100 N) |
| Ratchet at 1.5 x | 602 N tooth force, 12.5 MPa |
| Lift screw | Self-locking (lead 4.23 deg, friction 8.83 deg); 63 turns; 79 N at the handwheel at 1.5 x; buckling factor 2.7 |
| Lowest margin at 1.5 x | Spoke 106 MPa, factor 1.6 on yield; bracket 118 MPa, factor 1.7 |
| Mass | 171 kg; heaviest carry 29.6 kg by two people |
| Cost | Value-engineering target: USD 1,500. Estimated cost of the constructable design: USD 1,437 (USD 63 under the target) |

**Requirements not met.**

- **R8 (portability): not met as written.** Two modules weigh 27.1 kg (pivot tube with arm frame) and 29.6 kg (reel with bars); both are two-person carries at 14.8 kg each at most. First setup is about 29 minutes against 15. Accepted for the prototype under the pre-approval (VTR-DEC-001).
- **R6 (corrosion): at risk.** Only a coupon test can show it; the 304 chain 2 in chloride pickling liquor is the weak point.

**Decisions made under the pre-approval.** All TRL 2 decisions above (VTR-DDR-001); the eighteen design-for-construction changes (VTR-DDR-002); R8 accepted as not met for the prototype. Open decisions: none. Seven items to confirm when parts are bought are in VTR-DEC-001.

**Build plan findings (design changes made for construction, VTR-DDR-002).**

1. The arm tie tube would have bent at about 280 MPa: replaced by a torque tube round the pivot line (29 MPa).
2. 12-tooth sprockets cannot be bored 30 or 40 mm: 15/30 and 17/51 teeth, ratio still 6 to 1.
3. Chain 2 guard plate replaced by a closed case.
4. Tower bottom closed; ratchet and pawl under a cover with the release lever outside.
5. Far bearing is an open saddle with a keeper, so the reel drops in without anyone reaching 0.9 m over the pit; near bearing split with a bolted cap.
6. Pivot tube carried on the jackshaft tip by a plug; two collars locate the arm frame.
7. Extension tube 1.55 m pinned inside the pivot tube; far stand clamps through a split sleeve; spans 1.0 to 2.52 m.
8. Splash shield widened to 1.32 m and lowered to 60 mm with a hole for the jackshaft; base frame lengthened to 1.75 m to carry it.
9. Tower braces bolted and lowered (tower 23.2 kg; clears the ratchet cover).
10. Spiders on hub sleeves with hexagon ties; carrier bars bolted with end plates and eye tabs; axle sprocket hub moved to the wall side.
11. 1.5 m loading hooks stored on the base; a 3.6 m assembly bar through the hollow axle for carrying the reel; a thirteen-step assembly order.

**Appearance model deviations (`cad/src/product_model.py`).** Added for the renders only: snap hooks on the eye tabs, two goat skins and a yarn hank hanging from three bars, the pit cut into a concrete floor with brown liquor 150 mm below the rim, and a 1.75 m mannequin at the crank. Every main dimension comes from `model.py`.

**Render scenes.** `python3 .kit/export_views.py /home/claude/renders/vatreel` wrote `vatreel__hero`, `vatreel__exploded` and `vatreel__detail` (.npz and .json each) and `vatreel__jobs.json`. Photoreal renders, captions and cards are made on Amish's Mac; until then `media/render-hero.png` is missing and the check warns.

**Safety concerns.**

- Corrosive liquor and hot dye baths (to 98 °C): hands stay out by design, but gloves, eye protection and boots stay in use; two people at hot baths.
- Open pit edge: the stands sit back from the edge; nobody works from boards or the frame over the pit; the shield is not a guardrail.
- Moving machinery: chains, sprockets and ratchet enclosed; the reel itself is open in the pit and is never approached unless stopped, ratcheted and wound up. The guard openings still need an ISO 13857 check by a competent person (R12, TRL 4).
- Suspended load: the self-locking screw and the ratchet hold the reel; the far keeper and near cap must be closed before use.
- Setup lifts of up to 15 kg per person over a pit edge; stainless weld fume during the build.

**Recommended next step.** The design is ready for TRL 4 when the portfolio phase allows it: build to VTR-BLD-001, run the first checks over a water tank, coupon-test the wetted materials in the partner's liquors, then trial with the first co-design partner. Suggestions for later, not in the repo: a lighter reel (25 x 5 spokes, if a finer check that counts the tie ring allows it) to bring the reel under 25 kg; galvanized mild steel stands to save about USD 120.

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (VTR-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (VTR-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (VTR-REQ-001 v0.1): 10 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
