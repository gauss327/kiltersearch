

# Vector-First Climbing Problem Retrieval (Concise README)

Stay **vector-first** while handling vibe-y queries (“spanny”, “tension”, “few holds”, “AAARGH!”). 
Embed each problem once; normalize any user query into the same token language; then do cosine similarity.

## 1) Per-Problem: one fused embedding text
Concatenate and embed:

A) Control tags (facts computed in code)
[TAGS] SPAN=HIGH MAXMOVE=VERY_HIGH P90MOVE=HIGH SPREAD_HULL=0.31 RADIUS=0.44
HOLDS=7 STEEPNESS=40D STYLE=SLOPER,CRIMP,UNDERCLING FEET_DENSITY=LOW

- Bucket metrics into {LOW, MEDIUM, HIGH, VERY_HIGH}; include a few rounded numbers in consistent units.

B) Synonym pack (same for every problem)
synonyms: spanny reachy long-reach big move tension burly thuggy sparse few holds techy scrunchy

C) Human summary (LLM-written, fact-bounded)
summary: Reachy with a very big move (~0.39 of the board diagonal) and overall high spacing.
Scarce feet → body tension; crimps and a positive sloper up high.

Stored field:
embedding_text = tags + "\n" + synonym_pack + "\n" + "summary: " + human_summary

---

## 2) Query normalization → still a single vector
Normalize any user text into your token language (LLM or rules), then embed.

Format:
[WANTS] TENSION=HIGH SPAN=HIGH MAXMOVE=HIGH FEET_DENSITY=LOW STEEPNESS=HIGH
synonyms: tension burly lockoff core-intensive steep
free-text: problems that require a bunch of tension

Token weighting (optional): repeat important tokens to bias the embedding
SPAN=VERY_HIGH SPAN=VERY_HIGH MAXMOVE=HIGH

---

## 3) Metrics to compute (code, not LLM)
Normalize to 0–1 (where applicable); keep raw counts too.

Span/Reach: span_index, max_move_norm, p90_move_norm
Spread: hull_area_ratio, radius_ratio, anisotropy
Sparsity: hand_hold_count, hand_density, nn_p90
Hold mix: sloper_ratio, crimp_ratio, undercling_ratio, jug_ratio, bad_hold_ratio
Feet context: foot_density_near_hands, kickboard_only_start
Steepness: angle_deg (or normalized)
(Optional) Complexity: agreement, path_move_p90

Bucket into LOW/MEDIUM/HIGH/VERY_HIGH → fill [TAGS].

---

## 4) Dual-index variant (optional, still vector-only)
Semantic index: embed summary (+ synonyms)
Control index: embed tags (+ numbers)
Score: 0.6*cos(q_sem, p_sem) + 0.4*cos(q_ctrl, p_ctrl)

---

## 5) Prompt guardrails
Summary generation (offline, per problem):
- Inputs: numeric JSON + buckets + style tags
- Rules: Use only provided numbers/labels; include one evidence phrase (e.g., “Top move ≈ 0.39 of board diagonal (very high)”). Keep 2–4 sentences.

Query normalizer (runtime):
- Map slang → tokens; return:
  [WANTS] … 
  synonyms: … 
  free-text: …

---

## 6) Example
Problem embedding_text:
[TAGS] SPAN=HIGH MAXMOVE=VERY_HIGH P90MOVE=HIGH SPREAD_HULL=0.31 RADIUS=0.44 HOLDS=7
STEEPNESS=40D STYLE=SLOPER,CRIMP,UNDERCLING FEET_DENSITY=LOW
synonyms: spanny reachy long-reach big move tension burly sparse few holds techy scrunchy
summary: Reachy set with one very big move (~0.39 diagonal) and generally high spacing.
Scarce feet mean core tension through the middle.

User query → normalized:
[WANTS] HOLDS=LOW SPARSE=HIGH INTENSITY=HIGH MAXMOVE=HIGH SPAN=HIGH
synonyms: few holds sparse burly thuggy big move reachy
free-text: few holds, kinda burly

Retrieval:
- Embed both texts
- Cosine search (or dual-index blend)
- Return top matches with the summaries

---

## 7) Checklist
[ ] Compute metrics → bucket → build [TAGS]
[ ] Define fixed token schema + synonym pack
[ ] Build & store embedding_text per problem
[ ] Implement query normalizer → normalized text → embed
[ ] Choose single-index or dual-index scoring
[ ] (Optional) repeat tokens for “very/ultra” emphasis
[ ] Log matched tokens to explain results

Why it works: Buckets + tokens give lexical anchors; synonyms cover phrasing; summaries add context.
Everything stays pure vector at retrieval while remaining accurate and explainable.
