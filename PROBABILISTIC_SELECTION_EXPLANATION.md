# Probabilistic Selection - What It Does

## 🎲 **How Probabilistic Selection Works**

### **Greedy Selection (Previous):**
```
States at depth 1 with values:
  [1.67, 9, 9]  → value: 3.0  ✅ Always selected (top 10)
  [15, 9, 10]   → value: 3.0  ✅ Always selected
  [54, 9, 10]   → value: 3.0  ✅ Always selected
  [19, 6, 9]    → value: 3.0  ✅ Always selected
  [3, 9, 10]    → value: 3.0  ✅ Always selected
  
All 5 have same value → All selected every time
Result: DETERMINISTIC - same path every run
```

### **Probabilistic Selection (New):**
```
States with same values → Convert to probabilities:
  Each state: 3.0 / 15.0 = 20% probability

Sample 10 states with replacement:
  Run 1: Might select [1.67,9,9] twice, skip [15,9,10]
  Run 2: Might select [15,9,10] three times, skip [1.67,9,9]
  Run 3: Different combination again
  
Result: STOCHASTIC - different paths each run
```

## 🎯 **Why This Might Help**

### **The Current Problem:**
With greedy selection, from `[1.67, 9, 9]`:
- LLM proposes operations at depth 2
- Always picks top-k by value
- **Same operations explored every time**
- Never finds `1.67*9=15` if it's not in top proposals

### **With Probabilistic Selection:**
From the same 5 depth-1 states:
- **Sometimes** explores from `[1.67, 9, 9]` (might find `1.67*9=15`)
- **Sometimes** explores from `[15, 9, 10]` (different path!)
- **Sometimes** explores from `[54, 9, 10]` (another path!)
- **Sometimes** explores from `[19, 6, 9]` (yet another!)

**More diversity in which paths get explored!**

## 📊 **Expected Behavior**

### **Run 1 (Probabilistic):**
```
Depth 1: Samples [1.67,9,9], [15,9,10], [54,9,10] (random)
  ↓
Depth 2: Explores different states than greedy
  ↓
Might find solution through alternate path!
```

### **Run 2 (Probabilistic):**
```
Depth 1: Samples [15,9,10], [19,6,9], [3,9,10] (different random)
  ↓
Depth 2: Completely different exploration
  ↓
Another chance to find solution!
```

## 🎲 **Key Insight from Original ToT Paper**

From `src/tot/methods/bfs.py`:
```python
if args.method_select == 'sample':
    ps = np.array(values) / sum(values)  # Normalize to probabilities
    select_ids = np.random.choice(ids, size=n_select, p=ps)
```

**What this means:**
- States with value 20.0 → 20/total probability (HIGH chance)
- States with value 3.0 → 3/total probability (MEDIUM chance)
- States with value 0.01 → 0.01/total probability (LOW chance)

**Result:** High-value states explored more often, but not exclusively!

## ⚠️ **What Won't Change**

Probabilistic selection **won't** change:
- ❌ The operations proposed by LLM at each depth
- ❌ The fact that `9*10` is never proposed initially
- ❌ Temperature (still 0.7)

It **will** change:
- ✅ Which states get explored at each depth
- ✅ The search path through the tree
- ✅ Chances of finding alternate solution paths

## 🎯 **Success Scenarios**

### **Scenario 1: Depth 2 Exploration**
```
Depth 1: [1.67, 9, 9] still proposed (same as greedy)
Depth 2: Probabilistic might explore different operations
         Might try 9*1.67 instead of just 9+1.67
         Could find 15, then 15+9=24! ✅
```

### **Scenario 2: Alternate Path**
```
Depth 1: [15, 9, 10] gets selected (probabilistic)
Depth 2: Might find 15+9=24 directly? 
         (No, that leaves 10... but explores different space)
```

### **Scenario 3: Lucky Combination**
```
Multiple runs with probabilistic = multiple different tree explorations
Eventually hits the right combination of states/operations
Success through statistical diversity!
```

## 📈 **Expected Improvement**

**Greedy:**
- Success rate: ~30% (deterministic, same path)
- Needs exactly right operations at each depth

**Probabilistic:**
- Success rate: ~40-50% (stochastic, tries multiple paths)
- Can succeed through alternate routes

## 🚀 **Next Steps**

1. **Run cell 10** with probabilistic selection
2. **Watch the output** - you'll see "🎲 Probabilistic top X selected"
3. **Check the results** - did it find a different path?
4. **If still fails:** Try running 2-3 more times (different random explorations)

The randomness is now our **friend** - it means multiple attempts give different results! 🎲
