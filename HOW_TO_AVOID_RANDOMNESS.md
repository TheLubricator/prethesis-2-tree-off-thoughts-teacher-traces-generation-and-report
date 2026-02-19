# How Tree of Thoughts Avoids "Coin Flipping" - Original Paper's Approach

## 🎯 The Problem You Identified

You're absolutely right - your current implementation has **randomness at every depth**:
- Depth 1: Random chance of proposing `9*10` vs `6*9`
- Depth 2: Random chance of proposing `1.67*9` from `[1.67, 9, 9]`
- **Result:** Like flipping coins at each step - low success probability!

---

## 🧠 What the Original ToT Paper Did

The paper uses **THREE separate mechanisms** to avoid randomness:

### **1. PROPOSE Multiple Candidates (Not Just Random Sampling)**

**Your Current Approach:**
```python
# You generate ONE proposal at a time (stochastic)
response = gemini_codeact_generate(prompt, n=1, temperature=1.0)
# Temperature=1.0 means HIGH randomness
```

**Original ToT Approach:**
```python
# Generate MULTIPLE proposals simultaneously
proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
# Returns: ['2 + 8 = 10', '8 / 2 = 4', '14 + 2 = 16', ...]
# Gets ~5-10 different operations at once!
```

**Key Difference:**
- ❌ **You:** Generate 3 samples separately (might all be similar due to randomness)
- ✅ **Original:** Generate diverse batch in ONE call (forces different operations)

---

### **2. EVALUATE with LLM Reasoning (Not Just Distance to 24)**

**Your Current Approach:**
```python
# Hybrid evaluation (mostly based on distance to 24)
if abs(num - 24) < 0.01:
    return 100.0  # Perfect
elif 20 <= num <= 28:
    return 10.0   # Close range
# Plus LLM evaluation averaged in
```

**Original ToT Approach:**
```python
# LLM evaluates FEASIBILITY with reasoning
value_prompt = '''
10 14
10 + 14 = 24
sure                    # ← LLM knows this is IMMEDIATELY solvable

5 7 8
(8 - 5) * 7 = 21
likely                  # ← LLM knows numbers in good range

10 10 11
10 + 10 + 11 = 31
impossible              # ← LLM knows all sums too big
'''

# Convert to scores
value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}
```

**Key Difference:**
- ❌ **You:** Numeric distance + some LLM input (averaged)
- ✅ **Original:** LLM uses **reasoning** about combinability

---

### **3. SELECT Best Candidates (Greedy or Probability-Based)**

**Your Current Approach:**
```python
# Select top-k by value (greedy beam search)
viable_nodes.sort(key=lambda x: x.value, reverse=True)
selected_nodes = viable_nodes[:self.n_select_sample]  # Top 10
```

**Original ToT Approach - TWO OPTIONS:**

**Option A: Greedy Selection** (Same as yours)
```python
if args.method_select == 'greedy':
    select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:n_select_sample]
```

**Option B: Probability-Based Sampling** (More diverse!)
```python
if args.method_select == 'sample':
    ps = np.array(values) / sum(values)  # Convert to probabilities
    select_ids = np.random.choice(ids, size=n_select_sample, p=ps).tolist()
```

**Probability-based gives:**
- High-value states: More likely to be selected
- Medium-value states: Still have a chance
- Low-value states: Rare but possible
- **Result:** More exploration vs exploitation balance!

---

## 🎲 Why This Reduces "Coin Flipping"

### **Original ToT Strategy:**

```
State: [6, 9, 9, 10]
    ↓
[PROPOSE] Generate 8-10 operations in ONE prompt:
    ✅ 6+9=15
    ✅ 9-6=3
    ✅ 6*9=54
    ✅ 9*10=90    ← Got it!
    ✅ 10/6=1.67
    ✅ 9+10=19
    ✅ 10-9=1
    ✅ 9/6=1.5
    ↓
[EVALUATE] LLM reasoning on each:
    • [15, 9, 10]: "likely" (value: 1.0)  - Good range
    • [90, 6, 9]:  "sure" (value: 20.0)   - Can see 90/6=15!
    • [54, 9, 10]: "likely" (value: 1.0)  - Possible
    • [1.67, 9, 9]: "likely" (value: 1.0) - Possible
    ↓
[SELECT] Greedy top-5:
    1. [90, 6, 9]    ← This will lead to solution!
    2. [15, 9, 10]
    3. [1.67, 9, 9]
    4. [54, 9, 10]
    5. [19, 6, 9]
```

**Success Rate:** ~80-90% because:
1. ✅ Generates ALL major operations at once (not random)
2. ✅ LLM can reason about which are promising
3. ✅ Selects best candidates systematically

---

## 📊 Comparison: Your Approach vs Original

| Aspect | Your CodeAct | Original ToT | Impact |
|--------|--------------|--------------|--------|
| **Proposal** | 3 separate samples | 1 batch of 8-10 ops | Original more diverse |
| **Temperature** | 1.0 (high random) | 0.7 (moderate) | Original more stable |
| **Evaluation** | Hybrid (distance + LLM) | LLM reasoning only | Original more strategic |
| **LLM calls** | 3× per state | 1× per batch | Original more efficient |
| **Selection** | Greedy only | Greedy OR probabilistic | Original more flexible |

---

## 💡 Why Your Approach Still Has Merit

**Your CodeAct advantages:**
1. ✅ **Code execution** - More reliable than text reasoning
2. ✅ **Strict validation** - Prevents invalid operations (original can't do this!)
3. ✅ **Hybrid evaluation** - Numeric closeness is objective
4. ✅ **Free tier compatible** - Uses Gemini, not GPT-4

**Original ToT advantages:**
1. ✅ **Better diversity** - Batch proposals reduce randomness
2. ✅ **Smarter evaluation** - LLM reasoning about feasibility
3. ✅ **Proven approach** - Published research with benchmarks

---

## 🚀 How to Improve Your Implementation

### **Fix 1: Generate More Proposals Per Call**

**Current:**
```python
# Generate 3 samples separately
for _ in range(self.n_evaluate_sample):
    response = gemini_codeact_generate(prompt, n=1, temperature=1.0)
```

**Improvement:**
```python
# Modify prompt to request MULTIPLE operations
PROPOSE_PROMPT_CODEACT = '''
Current numbers: {numbers}

Generate 5-7 different possible next operations:
1. [Operation 1]
2. [Operation 2]
...

For EACH operation, provide thought, code, and result.
'''

# Parse multiple operations from ONE response
response = gemini_codeact_generate(prompt, n=1, temperature=0.7)
# Extract all operations from the response
```

**Benefit:** Get diverse operations in ONE call (reduces randomness)

---

### **Fix 2: Lower Temperature for More Consistency**

**Current:**
```python
temperature=1.0  # High randomness
```

**Improvement:**
```python
temperature=0.7  # Moderate diversity (same as original paper)
```

**Benefit:** More consistent proposals while keeping creativity

---

### **Fix 3: Improve LLM Evaluation Prompt**

**Current:**
```python
VALUE_PROMPT_CODEACT = '''
Evaluate if {numbers} can reach 24.
Think step-by-step...
'''
```

**Improvement:**
```python
VALUE_PROMPT_CODEACT = '''
Evaluate if {numbers} can reach 24 (sure/likely/impossible)

Examples:
10 14
10 + 14 = 24
sure

5 7 8
(8 - 5) * 7 = 21 (close)
Numbers in reasonable range
likely

1 3 3
Max: 1 * 3 * 3 = 9 (too small)
impossible

{numbers}
'''
```

**Benefit:** LLM gives structured reasoning (not just free-form)

---

### **Fix 4: Add Probabilistic Selection Option**

**Current:**
```python
# Only greedy selection
selected_nodes = viable_nodes[:self.n_select_sample]
```

**Add:**
```python
def select_nodes(self, nodes, method='greedy'):
    if method == 'greedy':
        return sorted(nodes, key=lambda x: x.value, reverse=True)[:self.n_select_sample]
    elif method == 'sample':
        values = [n.value for n in nodes]
        probs = np.array(values) / sum(values)
        indices = np.random.choice(len(nodes), size=self.n_select_sample, p=probs)
        return [nodes[i] for i in indices]
```

**Benefit:** More exploration, less likely to miss good paths

---

## 🎯 Recommended Priority

1. **High Priority:** Lower temperature to 0.7 (easy, immediate impact)
2. **Medium Priority:** Improve LLM evaluation prompt (better guidance)
3. **Low Priority:** Batch proposals (requires refactoring)

The temperature change alone should significantly improve consistency!

---

## 📚 Key Takeaway

**Original ToT doesn't avoid randomness entirely** - it **manages** it better:
1. Generates diverse candidates **systematically** (batch proposals)
2. Evaluates candidates **strategically** (LLM reasoning)
3. Selects candidates **intelligently** (greedy or probabilistic)

Your implementation can adopt these strategies while **keeping** the advantages of:
- Code execution reliability
- Strict validation
- Free tier compatibility

**The coin flips still exist, but you stack the odds in your favor!** 🎲✅
