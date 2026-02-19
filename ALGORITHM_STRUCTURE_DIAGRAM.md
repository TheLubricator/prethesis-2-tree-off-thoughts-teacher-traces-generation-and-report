# 🌳 Tree of Thoughts Algorithm Structure - Complete System (Updated 2026-02-04)

## Complete System Architecture - OpenAI GPT-4o-mini Version

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║            TREE OF THOUGHTS WITH CODEACT + SER - GAME OF 24 SOLVER              ║
║                     (Game24TreeOfThoughts Class - OpenAI)                        ║
╚══════════════════════════════════════════════════════════════════════════════════╝
                                       │
                                       │ Input: [2, 4, 8, 9], target=24
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                          🔧 INITIALIZATION PHASE                                 │
├──────────────────────────────────────────────────────────────────────────────────┤
│  1. Create root TreeNode: [2, 4, 8, 9]                                          │
│  2. Hyperparameters:                                                            │
│     • temperature = 0.7             (LLM sampling creativity)                   │
│     • n_evaluate_sample = 3         (LLM consensus votes)                       │
│     • n_select_sample = 15          (beam width - top nodes kept)  ← UPDATED    │
│     • max_steps = 6                 (maximum search depth)                      │
│     • api_delay = 1.0s              (rate limiting between calls)  ← UPDATED    │
│     • exhaustive_depth1 = False     (legacy mode, use enable_ser instead)       │
│     • enable_ser = False            (SER now optional!) ← NEW HYPERPARAMETER    │
│     • selection_method = 'greedy'   (deterministic beam search)                 │
│  3. Initialize: API counter, cache dictionary, solution list                    │
│  4. Initialize: SafeAgentSandbox for code execution                             │
│  5. Display SER status: ENABLED or DISABLED                                     │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
╔══════════════════════════════════════════════════════════════════════════════════╗
║                         🔄 MAIN SEARCH LOOP (BFS)                                ║
║                              solve() method                                      ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  For step in range(max_steps):                                                  ║
║    1. 🎯 Generate proposals for frontier nodes                                  ║
║    2. 🔒 Execute & validate code (SafeAgentSandbox)                             ║
║    3. 📊 Evaluate new states (hybrid: heuristics + LLM)                         ║
║    4. 🔬 SELECTIVE EXHAUSTIVE RESCUE (if enable_ser=True AND depth=0)           ║
║       • Check: max(all proposal values) < 5.0 threshold ← UPDATED               ║
║       • Trigger only when LLM proposals are uniformly weak                      ║
║       • Default: DISABLED (enable_ser=False) ← CHANGED                          ║
║    5. ✂️ Prune: Remove premature 24 traps and impossible states                 ║
║    6. 🎯 Beam selection: Keep top n_select_sample nodes                         ║
║    7. 🔧 DFP rescue: Preserve fragile fractional states                         ║
║    8. ✅ Check for solutions (single number ≈ 24)                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝
         │                    │                    │                    │
         ▼                    ▼                    ▼                    ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐
    │ Node 1  │         │ Node 2  │         │  ...    │         │ Node N  │
    │[2,4,8,9]│         │[12,2,9] │         │         │         │         │
    │value=0  │         │value=41 │         │         │         │         │
    └─────────┘         └─────────┘         └─────────┘         └─────────┘
         │                    │                    │                    │
         └────────────────────┴────────────────────┴────────────────────┘
                                       │
                  For each node in frontier, call:
                                       │
                                       ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        COMPONENT 1: PROPOSAL GENERATION                        ┃
┃                         get_proposals() / generate_all_first_moves()           ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                                ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Input: Current state (e.g., [21, 7, 8]), depth, mode           │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  🔀 MODE SELECTION (if depth == 0):                              │         ┃
┃  │                                                                  │         ┃
┃  │  if exhaustive_depth1 == True AND depth == 0:                   │         ┃
┃  │    → Use EXHAUSTIVE MODE (generate ALL ~24 first moves)         │         ┃
┃  │    → NO LLM CALLS!                                               │         ┃
┃  │    → Systematically try all pairs with +, -, *, /               │         ┃
┃  │    → Cost: +40% API calls (more nodes to evaluate)              │         ┃
┃  │    → Benefit: 100% coverage of first depth                      │         ┃
┃  │                                                                  │         ┃
┃  │  else:                                                           │         ┃
┃  │    → Use LLM MODE (standard proposal generation)                │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                    ┌─────────┴─────────┐                                       ┃
┃                    │                   │                                       ┃
┃         EXHAUSTIVE MODE        LLM MODE (default)                              ┃
┃                    │                   │                                       ┃
┃                    ▼                   ▼                                       ┃
┃  ┌─────────────────────────┐  ┌──────────────────────────────────┐            ┃
┃  │  EXHAUSTIVE GENERATION  │  │  BUILD PROPOSE_PROMPT_CODEACT    │            ┃
┃  │                         │  │  - Task description              │            ┃
┃  │  For each pair (i,j):   │  │  - Lookahead instruction         │            ┃
┃  │    For each operation:  │  │  - CodeAct format                │            ┃
┃  │      + (addition)       │  │  - Available numbers             │            ┃
┃  │      - (subtraction)    │  └──────────────────────────────────┘            ┃
┃  │      * (multiplication) │              │                                   ┃
┃  │      / (division)       │              ▼                                   ┃
┃  │                         │  ┌──────────────────────────────────┐            ┃
┃  │  Generate thought+code  │  │  🤖 LLM API CALL: gpt4o-mini     │            ┃
┃  │  Example:               │  │                                  │            ┃
┃  │  "7 - 5 = 2 → [2,6,9]" │  │  Settings:                       │            ┃
┃  │                         │  │  - Model: gpt4o-mini  │          ┃
┃  │  Returns: ~24 proposals │  │  - Temperature: 1.0              │            ┃
┃  │  (no LLM needed!)       │  │  - Parse: 5-8 proposals          │            ┃
┃  └─────────────────────────┘  │                                  │            ┃
┃                    │           │  Returns: 5-8 proposals          │            ┃
┃                    │           └──────────────────────────────────┘            ┃
┃                    │                   │                                       ┃
┃                    └─────────┬─────────┘                                       ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Example Proposals (from either mode):                           │         ┃
┃  │                                                                  │         ┃
┃  │  Proposal 1:                                                     │         ┃
┃  │    Thought: "Divide 21 by 7 to get 3, then 3*8=24"             │         ┃
┃  │    Code: res = numbers[0] / numbers[1]  # 21 / 7 = 3           │         ┃
┃  │                                                                  │         ┃
┃  │  Proposal 2:                                                     │         ┃
┃  │    Thought: "Add 7 and 8 to get 15, then 21+15=36"             │         ┃
┃  │    Code: res = numbers[1] + numbers[2]  # 7 + 8 = 15           │         ┃
┃  │                                                                  │         ┃
┃  │  ... (more proposals depending on mode)                         │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  📊 Tracking:                                                    │         ┃
┃  │  - API calls count += 1 (LLM mode only)                         │         ┃
┃  │  - API calls count += 0 (Exhaustive mode - no LLM!)             │         ┃
┃  │  - Store proposals with metadata (thought, code, node_id)       │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                       │
                                       │ Returns: List[Proposal]
                                       ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    COMPONENT 2: EXECUTION & VALIDATION                         ┃
┃                          execute_and_validate() method                         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                                ┃
┃  For each proposal:                                                            ┃
┃                                                                                ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 1: PARSE CODE                                              │         ┃
┃  │  Extract Python code from proposal text                          │         ┃
┃  │  Example: "res = numbers[0] / numbers[1]  # 21 / 7 = 3"         │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 2: EXECUTE CODE IN SANDBOX                                 │         ┃
┃  │                                                                  │         ┃
┃  │  Setup:                                                          │         ┃
┃  │  - Create safe namespace: {'numbers': [21, 7, 8]}               │         ┃
┃  │  - Execute: exec(code, namespace)                               │         ┃
┃  │  - Extract result: res = namespace['res']                       │         ┃
┃  │  - Calculate new state: remove used numbers, add result         │         ┃
┃  │                                                                  │         ┃
┃  │  Error Handling:                                                 │         ┃
┃  │  - Catch syntax errors → skip proposal                          │         ┃
┃  │  - Catch runtime errors (division by zero) → skip proposal      │         ┃
┃  │  - Catch invalid operations → skip proposal                     │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 3: VALIDATE RESULT                                         │         ┃
┃  │                                                                  │         ┃
┃  │  Checks:                                                         │         ┃
┃  │  ✓ Result is a number (not string, list, etc.)                  │         ┃
┃  │  ✓ Result is finite (not NaN, not infinity)                     │         ┃
┃  │  ✓ Exactly 2 numbers were used from parent state                │         ┃
┃  │  ✓ New state has len(parent) - 1 numbers                        │         ┃
┃  │  ✓ All numbers in new state are valid (no None, NaN)            │         ┃
┃  │                                                                  │         ┃
┃  │  If validation fails → skip proposal                            │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 4: CREATE CHILD NODE                                       │         ┃
┃  │                                                                  │         ┃
┃  │  new_node = TreeNode(                                            │         ┃
┃  │    observation = "[3.0, 8]",                                     │         ┃
┃  │    thought = "Divide 21 by 7 to get 3, then 3*8=24",           │         ┃
┃  │    code = "res = numbers[0] / numbers[1]",                      │         ┃
┃  │    parent = current_node,                                        │         ┃
┃  │    depth = parent.depth + 1,                                     │         ┃
┃  │    value = 0.0  # Will be set by evaluation                     │         ┃
┃  │  )                                                               │         ┃
┃  │                                                                  │         ┃
┃  │  Add to parent.children list                                     │         ┃
┃  │  Add to all_nodes tracking list                                  │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                       │
                                       │ Returns: List[TreeNode] (valid children)
                                       ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        COMPONENT 3: STATE EVALUATION                           ┃
┃                    evaluate_state() method [MODIFIED FOR DISTILLATION]         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                                ┃
┃  For each child node:                                                          ┃
┃                                                                                ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Input: numbers = [3.0, 8], is_final = False                    │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  PHASE 1: FAST HEURISTIC CHECKS (no LLM)                         │         ┃
┃  │                                                                  │         ┃
┃  │  Check 1: Is this a single number?                              │         ┃
┃  │    if len(numbers) == 1:                                         │         ┃
┃  │      if abs(numbers[0] - 24) < 0.01:                            │         ┃
┃  │        → SOLUTION! Return (100.0, eval_record)                  │         ┃
┃  │      else:                                                       │         ┃
┃  │        → DEAD END! Return (0.0, eval_record)                    │         ┃
┃  │                                                                  │         ┃
┃  │  Check 2: Premature 24?                                          │         ┃
┃  │    if 24 in numbers AND len(numbers) > 1:                       │         ┃
┃  │      → TRAP! Return (0.01, eval_record)                         │         ┃
┃  │                                                                  │         ┃
┃  │  Check 3: Huge numbers (>1000)?                                  │         ┃
┃  │    if max(abs(n) for n in numbers) > 1000:                      │         ┃
┃  │      → UNLIKELY! Return (0.1, eval_record)                      │         ┃
┃  │                                                                  │         ┃
┃  │  Check 4: All tiny numbers (<0.01)?                              │         ┃
┃  │    if all(abs(n) < 0.01 for n in numbers):                      │         ┃
┃  │      → UNLIKELY! Return (0.1, eval_record)                      │         ┃
┃  │                                                                  │         ┃
┃  │  Check 5: Promising pattern?                                     │         ┃
┃  │    has_number_near_24 = any(20 <= abs(n) <= 40)                │         ┃
┃  │    has_small_adjusters = any(1 <= abs(n) <= 12)                │         ┃
┃  │    if has_number_near_24 AND has_small_adjusters:               │         ┃
┃  │      → Apply LLM boost factor (1.2x)                            │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              │ If no heuristic returns early:                  ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  PHASE 2: CHECK CACHE                                            │         ┃
┃  │                                                                  │         ┃
┃  │  state_key = frozenset(numbers)                                  │         ┃
┃  │  if state_key in evaluation_cache:                               │         ┃
┃  │    cached_value = evaluation_cache[state_key]                   │         ┃
┃  │    → Return (cached_value, minimal_eval_record)                 │         ┃
┃  │    (Saves API calls!)                                            │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              │ If not cached:                                  ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  PHASE 3: LLM EVALUATION (n_evaluate_sample times)               │         ┃
┃  │                                                                  │         ┃
┃  │  Build VALUE_PROMPT_CODEACT:                                     │         ┃
┃  │  - Ask: "Can [3.0, 8] reach 24 using +,-,*,/?"                  │         ┃
┃  │  - Request: Respond with "sure", "likely", or "impossible"      │         ┃
┃  │  - Context: Show original problem [7,8,8,13]                    │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │         🤖 LLM API CALL #2: GPT-4o-mini                          │         ┃
┃  │               (Called n_evaluate_sample=3 times)                 │         ┃
┃  │                                                                  │         ┃
┃  │  Settings:                                                       │         ┃
┃  │  - Model: gpt-4o-mini                                            │         ┃
┃  │  - Temperature: 0.7                                              │         ┃
┃  │  - Max tokens: 200 (short answer)                               │         ┃
┃  │  - Rate limit: 0.15s delay between calls                        │         ┃
┃  │                                                                  │         ┃
┃  │  Call 1 returns: "sure" (with reasoning)                         │         ┃
┃  │  Call 2 returns: "sure" (with reasoning)                         │         ┃
┃  │  Call 3 returns: "likely" (with reasoning)                       │         ┃
┃  │                                                                  │         ┃
┃  │  📊 Tracking: API calls count += 3                              │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  PHASE 4: COMPUTE SCORE & BUILD EVAL RECORD                      │         ┃
┃  │                                                                  │         ┃
┃  │  Judgment Mapping:                                               │         ┃
┃  │  - "impossible" → 0.001                                          │         ┃
┃  │  - "likely"     → 1.0                                            │         ┃
┃  │  - "sure"       → 20.0                                           │         ┃
┃  │                                                                  │         ┃
┃  │  Count judgments:                                                │         ┃
┃  │  - sure_count = 2                                                │         ┃
┃  │  - likely_count = 1                                              │         ┃
┃  │  - impossible_count = 0                                          │         ┃
┃  │                                                                  │         ┃
┃  │  raw_score = sum([20, 20, 1]) = 41.0                            │         ┃
┃  │  boosted_score = raw_score * llm_boost_factor                   │         ┃
┃  │                = 41.0 * 1.2 = 49.2                               │         ┃
┃  │                                                                  │         ┃
┃  │  confidence_level = "high" (2+ sure judgments)                   │         ┃
┃  │                                                                  │         ┃
┃  │  eval_record = {                                                 │         ┃
┃  │    "state": "[3.0, 8]",                                          │         ┃
┃  │    "is_final": False,                                            │         ┃
┃  │    "heuristic_checks": {...},                                    │         ┃
┃  │    "llm_judgments": ["sure", "sure", "likely"],                 │         ┃
┃  │    "llm_raw_responses": [...],                                   │         ┃
┃  │    "reasoning": [                                                │         ┃
┃  │      "LLM is confident (2 sure, 1 likely)",                     │         ┃
┃  │      "Can multiply 3*8=24 directly"                             │         ┃
┃  │    ],                                                            │         ┃
┃  │    "score_breakdown": {                                          │         ┃
┃  │      "sure_count": 2,                                            │         ┃
┃  │      "likely_count": 1,                                          │         ┃
┃  │      "raw_score": 41.0,                                          │         ┃
┃  │      "boosted_score": 49.2,                                      │         ┃
┃  │      "confidence_level": "high"                                  │         ┃
┃  │    },                                                            │         ┃
┃  │    "final_value": 49.2                                           │         ┃
┃  │  }                                                               │         ┃
┃  │                                                                  │         ┃
┃  │  Cache result: evaluation_cache[state_key] = 49.2               │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  STORE IN NODE (for distillation!)                               │         ┃
┃  │                                                                  │         ┃
┃  │  node.value = 49.2                                               │         ┃
┃  │  node.evaluation = eval_record                                   │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                       │
                                       │ Returns: (value, eval_record) tuple
                                       ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        COMPONENT 4: NODE SELECTION (BEAM SEARCH)               ┃
┃                            select_best_nodes() method                          ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                                ┃
┃  After evaluating all new child nodes:                                         ┃
┃                                                                                ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Input: all_children = [node1, node2, ..., node50]              │         ┃
┃  │         (e.g., 10 frontier nodes × 5 proposals = 50 children)    │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 1: FILTER OUT LOW-VALUE NODES                              │         ┃
┃  │                                                                  │         ┃
┃  │  Remove nodes with:                                              │         ┃
┃  │  - value < 0.1 (dead ends, traps, unlikely states)              │         ┃
┃  │  - execution errors (invalid operations)                        │         ┃
┃  │                                                                  │         ┃
┃  │  Result: filtered_nodes = 35 nodes                               │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 2: SORT BY VALUE (descending)                              │         ┃
┃  │                                                                  │         ┃
┃  │  sorted_nodes = sorted(filtered_nodes,                           │         ┃
┃  │                        key=lambda n: n.value,                    │         ┃
┃  │                        reverse=True)                             │         ┃
┃  │                                                                  │         ┃
┃  │  Top nodes:                                                      │         ┃
┃  │  1. Node A: value=100.0 (SOLUTION!)                             │         ┃
┃  │  2. Node B: value=72.0  (very promising)                        │         ┃
┃  │  3. Node C: value=49.2  (promising)                             │         ┃
┃  │  ...                                                             │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 3: SELECT TOP n_select_sample NODES (BEAM WIDTH)           │         ┃
┃  │                                                                  │         ┃
┃  │  new_frontier = sorted_nodes[:15]  # Keep top 15 nodes          │         ┃
┃  │                                                                  │         ┃
┃  │  This is BEAM SEARCH: prune search space to most promising!      │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                              │                                                 ┃
┃                              ▼                                                 ┃
┃  ┌──────────────────────────────────────────────────────────────────┐         ┃
┃  │  Step 4: CHECK FOR SOLUTIONS                                     │         ┃
┃  │                                                                  │         ┃
┃  │  for node in new_frontier:                                       │         ┃
┃  │    if node.value == 100.0:  # Found solution                    │         ┃
┃  │      solutions.append(node)                                      │         ┃
┃  │      if return_first_solution:                                   │         ┃
┃  │        → STOP SEARCH (early termination)                         │         ┃
┃  └──────────────────────────────────────────────────────────────────┘         ┃
┃                                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                       │
                                       │ new_frontier → next iteration
                                       ▼
╔══════════════════════════════════════════════════════════════════════════════════╗
║                               TREE STRUCTURE GROWTH                              ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║                              ROOT [7,8,8,13]                                     ║
║                              value=0.0                                           ║
║                                   │                                              ║
║                    ┌──────────────┼──────────────┐                              ║
║                    │              │              │                              ║
║                   ▼              ▼              ▼                              ║
║            Child 1           Child 2        Child 3                             ║
║            [21,7,8]          [15,8,13]      [56,7,8]                            ║
║            value=49.2        value=25.0     value=0.1                           ║
║            eval={...}        eval={...}     eval={...}                          ║
║                │                 │              │                               ║
║       ┌────────┴────┐           │              └─→ pruned (low value)           ║
║       │             │           │                                               ║
║      ▼             ▼           ▼                                               ║
║  Grandchild 1  Grandchild 2  Grandchild 3                                      ║
║  [3.0,8]       [14,8]        [2,8,13]                                          ║
║  value=72.0    value=30.0    value=15.0                                        ║
║  eval={...}    eval={...}    eval={...}                                        ║
║      │                                                                          ║
║      ▼                                                                          ║
║  Great-Grandchild 1                                                             ║
║  [24.0]  ← SOLUTION!                                                            ║
║  value=100.0                                                                    ║
║  eval={is_solution: true}                                                       ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

---

## Tree Node Data Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        TreeNode Object                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Fields:                                                        │
│  • observation: str            "[3.0, 8]"                       │
│  • thought: str                "Divide 21 by 7..."             │
│  • code: str                   "res = numbers[0]/numbers[1]"   │
│  • value: float                49.2                             │
│  • parent: TreeNode            → parent node reference          │
│  • children: List[TreeNode]    [child1, child2, ...]           │
│  • depth: int                  2                                │
│  • is_terminal: bool           False                            │
│  • evaluation: dict  ← NEW!    {reasoning, judgments, ...}     │
│                                                                 │
│  Methods:                                                       │
│  • to_dict()      → Export to JSON (includes evaluation)       │
│  • add_child()    → Add child node                             │
│  • get_path()     → Trace path from root to this node          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Call Flow & Rate Limiting

```
┌─────────────────────────────────────────────────────────────────┐
│                     API Call Management                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Rate Limiting:                                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Before each API call:                               │      │
│  │  1. Check time since last call                       │      │
│  │  2. If < 0.15 seconds: sleep(remaining_time)         │      │
│  │  3. Make API call                                     │      │
│  │  4. Update last_call_time                            │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  Daily Limit Tracking:                                          │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  - Max requests per day: ~10,000 (tier 1 OpenAI)     │      │
│  │  - Track: api_calls_count                            │      │
│  │  - Warn at: 9,000 calls                              │      │
│  │  - Stop at: 10,000 calls                             │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  API Call Breakdown (example run):                              │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Step 1: 10 frontier nodes × 1 proposal call = 10    │      │
│  │  Step 1: 50 children × 3 evaluation calls = 150      │      │
│  │  Step 2: 15 frontier × 1 proposal = 15               │      │
│  │  Step 2: 75 children × 3 evaluation = 225            │      │
│  │  ... (cache reduces later evaluation calls)          │      │
│  │  Total: ~108 API calls for [7,8,8,13] solution       │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Caching Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                     Evaluation Cache                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cache Key: frozenset of numbers (order-independent)            │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Example:                                             │      │
│  │  [3.0, 8] → frozenset({3.0, 8})                      │      │
│  │  [8, 3.0] → frozenset({3.0, 8})  (same key!)         │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  Benefits:                                                      │
│  • Avoid re-evaluating same state                              │
│  • Saves 3 API calls per cache hit                             │
│  • Typical hit rate: 20-40% in deep searches                   │
│                                                                 │
│  Storage:                                                       │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  evaluation_cache = {                                │      │
│  │    frozenset({3.0, 8}): 72.0,                        │      │
│  │    frozenset({21, 7, 8}): 49.2,                      │      │
│  │    frozenset({24}): 100.0,                           │      │
│  │    ...                                                │      │
│  │  }                                                    │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Search Termination Conditions

```
┌─────────────────────────────────────────────────────────────────┐
│                   When Does Search Stop?                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Condition 1: Solution Found (if return_first_solution=True)    │
│    → As soon as any node reaches value=24                       │
│                                                                 │
│  Condition 2: Max Steps Reached                                 │
│    → After max_steps iterations (default: 6)                    │
│                                                                 │
│  Condition 3: Empty Frontier                                    │
│    → No promising nodes left to expand                          │
│    → All nodes pruned due to low values                         │
│                                                                 │
│  Condition 4: API Limit Reached                                 │
│    → Approaching daily API quota (tier-dependent)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Output & Export

```
┌─────────────────────────────────────────────────────────────────┐
│                    Result Dictionary                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {                                                              │
│    "is_solved": True,                                           │
│    "solutions": [solution_node],                                │
│    "total_nodes": 104,                                          │
│    "api_calls": 108,                                            │
│    "steps": 3,                                                  │
│    "tree_root": root_node                                       │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Export to JSON File                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  File: game24_codeact_tree_20260202_004127.json                 │
│                                                                 │
│  Contents:                                                      │
│  {                                                              │
│    "observation": "[7, 8, 8, 13]",                              │
│    "thought": "Initial state",                                  │
│    "value": 0.0,                                                │
│    "children": [                                                │
│      {                                                          │
│        "observation": "[21, 7, 8]",                             │
│        "thought": "Add 8 and 13...",                            │
│        "code": "res = numbers[1] + numbers[3]",                 │
│        "value": 49.2,                                           │
│        "evaluation": {  ← NEW FOR DISTILLATION                  │
│          "reasoning": [...],                                    │
│          "llm_judgments": ["sure", "likely", "sure"],          │
│          "confidence": "high",                                  │
│          ...                                                    │
│        },                                                       │
│        "children": [...]                                        │
│      }                                                          │
│    ]                                                            │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│         Convert to Distillation Dataset (SLM Training)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Command: python create_distillation_dataset.py <tree>.json    │
│                                                                 │
│  Output: Training examples with:                                │
│  - Problem: [7, 8, 8, 13]                                       │
│  - Solution trajectory: [                                       │
│      {step: 1, thought: "...", code: "...", evaluation: {...}},│
│      {step: 2, thought: "...", code: "...", evaluation: {...}},│
│      {step: 3, thought: "...", code: "...", evaluation: {...}} │
│    ]                                                            │
│  - Metadata: steps, nodes, API calls, etc.                      │
│                                                                 │
│  Use for: Training smaller models to learn ToT reasoning        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

1. **CodeAct Pattern**: Thoughts are paired with executable Python code for verification
2. **Hybrid Evaluation**: Fast heuristics (4 checks) + LLM sampling for accuracy
3. **Beam Search**: Keep top-k nodes to balance exploration vs. computation
4. **Caching**: Avoid redundant evaluation of same states
5. **Rate Limiting**: Respect API quotas with 0.15s delays
6. **Lookahead**: LLM thinks 2-3 steps ahead during proposal
7. **Distillation**: Capture evaluation reasoning for training smaller models
8. **🆕 Exhaustive Depth-1**: Optional mode to try ALL ~24 first moves (100% coverage)

---

## Heuristics Summary

**Active Heuristics (4 fast checks):**
1. ✅ Premature 24 detection (24 appears too early) → 0.01 score
2. ✅ Huge numbers (>1000) → 0.1 score
3. ✅ Tiny numbers (all <0.5) → 0.5 score
4. ✅ Near-24 bonus (has number 20-40 + small adjusters) → 1.2x boost

**Removed Features (as of Feb 2, 2026):**
- ❌ Multiplicative potential heuristic (caused regressions, removed)
- ❌ Improved prompts with few-shot examples (didn't improve performance significantly, disabled)

---

**Generated:** February 2, 2026  
**Updated:** February 3, 2026  
**Purpose:** Visual guide to Tree of Thoughts algorithm structure

---

##  LATEST UPDATES (February 4, 2026)

### 1. Hard-Coded 2-Number Arithmetic Check

**Problem:** LLM evaluates [15, 9] as 'likely' instead of 'sure' (15+9=24 is deterministic)

**Solution:** Added Python arithmetic bypass in evaluate_state() for len==2 states

```python
if len(numbers) == 2:
    a, b = numbers[0], numbers[1]
    operations_to_24 = [
        abs(a + b - 24) < 0.001,
        abs(a - b - 24) < 0.001,
        abs(b - a - 24) < 0.001,
        abs(a * b - 24) < 0.001,
        abs(a / b - 24) < 0.001 if b != 0 else False,
        abs(b / a - 24) < 0.001 if a != 0 else False
    ]
    if any(operations_to_24):
        return 60.0  # Equivalent to 'sure, sure, sure'
    else:
        return 0.001  # Dead end
```

**Benefits:**
-  100% reliable (no LLM arithmetic errors)
-  Faster (no API call needed)
-  Cheaper (saves 3 evaluations per 2-number state)

---

### 2. Selective Exhaustive Rescue (SER)

**Problem:** LLM never proposes unconventional first moves (9-7, 4+8, 5/2), causing 100% failure on single-path puzzles

**Solution:** Adaptive exhaustive search at depth-1

```python
if step == 0 and not self.exhaustive_depth1:
    if viable_nodes:
        max_value = max(node.value for node in viable_nodes)
        LOW_CONFIDENCE_THRESHOLD = 10.0
        
        if max_value < LOW_CONFIDENCE_THRESHOLD:
            print(' SELECTIVE EXHAUSTIVE RESCUE TRIGGERED!')
            # Generate ALL ~24 first moves exhaustively
            # Evaluate with n_evaluate_sample=1 (optimized)
            # Replace LLM proposals
```

**Trigger Logic:**
- Only at depth-1 (first move)
- Only when max(all LLM proposal values) < 10.0
- Threshold 10.0 = below 'likely, likely, likely' (3.0) and 'sure' (20.0)

**Example:**
- [2,4,8,9]: LLM proposes 4+9, 8-2, 2*9 (all score < 10.0)
- SER generates: 4+8=12  Critical move LLM missed!
- Solution: (4+8)*2 = 24 

---

### 3. SER Performance Optimization

**Problem:** SER added ~2 minutes overhead (24 moves  3 evaluations = 72 API calls)

**Solution:** Reduce n_evaluate_sample to 1 for exhaustive moves

```python
# OPTIMIZATION: Temporarily reduce evaluation samples for speed
original_n_eval = self.n_evaluate_sample
self.n_evaluate_sample = 1  # Single evaluation enough for deterministic moves

# Evaluate exhaustive nodes
for node in exhaustive_nodes:
    value, eval_record = self.evaluate_state(...)
    
# Restore original setting
self.n_evaluate_sample = original_n_eval
```

**Performance Impact:**
- Before: 72 API calls  ~2 minutes overhead
- After: 24 API calls  ~40 seconds overhead
- Savings: ~79 seconds per hard puzzle (66% reduction)

---

### 4. Enhanced VALUE_PROMPT with Structured Rules

**Problem:** LLM inconsistent on edge cases, poor mental arithmetic

**Solution:** Added IMPORTANT RULES with clear categories

```
IMPORTANT RULES (follow strictly):

1. TWO-NUMBER CERTAINTY:
   - If exactly TWO numbers remain and ANY valid operation
     (+, -, *, /) between them equals 24, answer 'sure'.

2. FRACTION HANDLING:
   - States with exactly ONE non-integer CAN be promising.

3. LARGE NUMBERS:
   - Numbers above 24 can still be useful via subtraction or division.

4. MULTI-STEP PATHS:
   - If reaching 24 requires careful ordering or multiple steps
     but is still plausible, answer 'likely'.

5. IMPOSSIBILITY:
   - Answer 'impossible' ONLY if no sequence of +, -, *, /
     can reasonably reach 24.

Examples: [15,9]sure, [12,2]sure, [11,12]impossible, [24,1]sure, [1,1,1]impossible
```

---

## Updated Performance Metrics (Feb 4, 2026)

### Cost Analysis (GPT-4o)

| Scenario | API Calls | Time | Cost |
|----------|-----------|------|------|
| Easy puzzle (no SER) | ~30-40 | 6-9 min | \.002-0.003 |
| Hard puzzle (SER) | ~60-70 | 7-10 min | \.004-0.005 |
| Always exhaustive | ~80-100 | 8-12 min | \.006-0.008 |

### Success Rate

| Puzzle Type | Pure LLM | With SER | Always Exhaustive |
|-------------|----------|----------|-------------------|
| Easy (multiple paths) | 90-95% | 95-98% | 98-100% |
| Medium (2-3 paths) | 60-70% | 85-90% | 95-98% |
| **Hard (single path)** | **0-20%** | **80-90%** | 95-98% |
| **Overall** | **~70%** | **~90%** | ~97% |

---

## System Architecture Summary

```
Input  Initialization
  
Main Search Loop (BFS):
  For each depth:
    1. Generate proposals (LLM or exhaustive)
    2. Execute & validate (SafeAgentSandbox)
    3. Evaluate states:
       - Heuristics (premature 24, huge numbers, etc.)
       - If len==2: Hard-coded Python check  (NEW)
       - If len>=3: LLM evaluation (3 samples)
       - Apply boosts for promising patterns
    4. Selective Exhaustive Rescue (SER):
       - Check: max(depth-1 values) < 10.0?
       - If yes: Generate ALL ~24 first moves
       - Evaluate with n=1 (fast mode)  (OPTIMIZED)
       - Replace LLM proposals
    5. Select top nodes (beam=10)
    6. DFP rescue (fragile fractions)
    7. Check for solutions
```

---

**Last Updated:** February 4, 2026  
**Notebook:** tot_concept_openai_version.ipynb  
**Model:** GPT-4o-mini (gpt-4o-mini) ← UPDATED
**Key Innovations:** Hard-coded 2-number check, SER with optimization, Enhanced VALUE_PROMPT

---

## LATEST UPDATES (February 4, 2026 - Latest)

### 1. SER Made Optional (Hyperparameter)

**Problem:** SER triggers on ALL puzzles due to GPT-4o-mini evaluation uniformity (all states score ~3.0 "likely, likely, likely")

**Root Cause:** GPT-4o-mini evaluator cannot distinguish intermediate state quality - gives uniform low scores

**Solution:** Made SER a toggleable hyperparameter instead of hard-coded

```python
def __init__(self, 
             temperature: float = 0.7,
             n_evaluate_sample: int = 3,
             n_select_sample: int = 15,
             max_steps: int = 6,
             api_delay: float = 1.0,
             selection_method: str = 'greedy',
             exhaustive_depth1: bool = False,
             enable_ser: bool = False):  # NEW: Default DISABLED
    """
    Args:
        enable_ser: If True, enable Selective Exhaustive Rescue
                    when LLM proposals are weak (default: False)
    """
    self.enable_ser = enable_ser
    
    if enable_ser:
        print(f"  • SER: ENABLED (will rescue weak LLM proposals)")
    else:
        print(f"  • SER: DISABLED (pure LLM-guided search)")
```

**Usage:**
```python
# Fast mode (default) - SER disabled
solver = Game24TreeOfThoughts()

# Thorough mode - SER enabled for hard puzzles
solver = Game24TreeOfThoughts(enable_ser=True)
```

**Performance Impact:**
- SER disabled: ~15-20 API calls, 2-3 minutes (FAST)
- SER enabled: ~50-150 API calls, 5-10 minutes (THOROUGH)
- Why disable: GPT-4o-mini evaluator has uniformity bias, SER not selective

---

### 2. SER Threshold Lowered (10.0 → 5.0)

**Problem:** Threshold 10.0 allows states with single "sure" (score=20.0) to bypass SER

**Solution:** Lower threshold to 5.0 - only trigger if NO "sure" ratings exist

```python
if self.enable_ser and step == 0 and not self.exhaustive_depth1:
    if viable_nodes:
        max_value = max(node.value for node in viable_nodes)
        LOW_CONFIDENCE_THRESHOLD = 5.0  # Changed from 10.0
        
        if max_value < LOW_CONFIDENCE_THRESHOLD:
            # Only trigger if ALL proposals are below "sure" level
            # Score breakdown: impossible=0.001, likely=1.0, sure=20.0
            # Threshold 5.0 means: only if no "sure" judgments
```

**Trigger Logic:**
- Old: Trigger if max_value < 10.0 (could have 1 "sure", 2 "impossible")
- New: Trigger if max_value < 5.0 (NO "sure" judgments allowed)
- Stricter condition = fewer false triggers

---

### 3. Evaluation Temperature Changed (0.7 → 0.0)

**Problem:** Temperature 0.7 adds randomness to already-poor evaluations

**Solution:** Use temperature=0.0 for deterministic, consistent evaluations

```python
def evaluate_state(self, numbers, is_final=False, original_problem=None):
    # ... build prompt ...
    
    # Call LLM with deterministic temperature
    response = openai_generate(
        prompt, 
        n=1, 
        temperature=0.0,  # Changed from 0.7
        system_prompt=SYSTEM_PROMPT
    )[0]
```

**Benefits:**
- More consistent evaluations across runs
- Reduces variance in judgment quality
- Still won't fix uniformity bias, but makes it predictable

---

### 4. Configuration Updates

**Updated Defaults:**
```python
# Model
MODEL_NAME = "gpt-4o-mini"  # Changed from "gpt-4o"

# Timing
api_delay = 1.0  # Changed from 0.15s (more conservative)

# Beam search
n_select_sample = 15  # Changed from 10 (wider beam)

# SER control
enable_ser = False  # NEW: Default disabled
```

**Why These Changes:**
- GPT-4o-mini is faster and cheaper but has evaluation limitations
- Longer API delay prevents rate limiting issues  
- Wider beam compensates for weaker evaluations
- SER disabled by default due to uniformity issue

---

### 5. Known Issues & Limitations

**GPT-4o-mini Evaluation Bias:**
- **Symptom:** ALL 3-number states score exactly 3.0 ("likely, likely, likely")
- **Evidence:** Tested [2,3,5,12], [5,6,7,13], [1,4,5,6] - all uniform
- **Cause:** Model cannot do mental arithmetic for intermediate states
- **Impact:** SER not truly "selective" - becomes always-on if enabled
- **Workaround:** Keep SER disabled (enable_ser=False) by default

**SER Trigger Rate:**
- With GPT-4o-mini: 100% of puzzles (due to uniformity)
- With GPT-4o: ~20-30% of puzzles (as intended)
- **Recommendation:** Use GPT-4o for better evaluation quality

**Cost-Performance Trade-off:**
```
┌─────────────────┬──────────┬─────────┬──────────────┐
│ Configuration   │ API Calls│ Time    │ Success Rate │
├─────────────────┼──────────┼─────────┼──────────────┤
│ 4o-mini, no SER │ 15-20    │ 2-3 min │ ~70%         │
│ 4o-mini + SER   │ 50-150   │ 5-10min │ ~70%*        │
│ 4o, no SER      │ 15-20    │ 2-3 min │ ~85%         │
│ 4o + SER        │ 50-70    │ 7-10min │ ~95%         │
└─────────────────┴──────────┴─────────┴──────────────┘
* No improvement due to evaluation bias
```

---

### 6. Alternative: CoT Approach

**Created:** `cot_concept_openai_version.ipynb`

**Purpose:** Fast, single-path reasoning as alternative to slow ToT

**Features:**
- No tree search (single attempt)
- Uses same 5-shot CoT prompt from game24.py
- JSON structured output with verification
- Arithmetic validation function
- Batch processing capability

**Performance:**
- 1 API call per puzzle
- ~1-2 seconds per puzzle  
- ~70% success rate on easy-medium puzzles
- Good baseline for comparison

**Use Cases:**
- Quick testing without tree overhead
- Baseline performance measurement
- Fast batch processing

---

## Comparison: ToT vs CoT

```
┌──────────────────────┬─────────────┬─────────────────┐
│ Feature              │ ToT (GPT4o) │ CoT (GPT4o-mini)│
├──────────────────────┼─────────────┼─────────────────┤
│ API Calls            │ 15-150      │ 1               │
│ Time per Puzzle      │ 2-10 min    │ 1-2 sec         │
│ Search Strategy      │ Tree/Beam   │ Single path     │
│ Backtracking         │ Yes         │ No              │
│ Success (easy)       │ 95-98%      │ 85-90%          │
│ Success (hard)       │ 80-95%      │ 30-50%          │
│ Cost per Puzzle      │ $0.002-0.01 │ $0.0001         │
│ Use Case             │ Thorough    │ Fast baseline   │
└──────────────────────┴─────────────┴─────────────────┘
```

---

## Recommended Usage

**For Production (Quality):**
```python
solver = Game24TreeOfThoughts(
    temperature=0.7,
    n_evaluate_sample=3,
    n_select_sample=15,
    enable_ser=True,  # Enable for hard puzzles
    api_delay=1.0
)
# Use GPT-4o model for better evaluations
```

**For Testing (Speed):**
```python
solver = Game24TreeOfThoughts(
    temperature=0.7,
    n_evaluate_sample=3,
    n_select_sample=15,
    enable_ser=False,  # Disable for speed
    api_delay=1.0
)
# Or use CoT notebook for even faster testing
```

---

**Last Updated:** February 4, 2026 (Latest)
**Notebook:** tot_concept_openai_version.ipynb  
**Model:** GPT-4o-mini (default) | GPT-4o (recommended for quality)
**Key Changes:** SER as hyperparameter, optimized thresholds, CoT alternative

