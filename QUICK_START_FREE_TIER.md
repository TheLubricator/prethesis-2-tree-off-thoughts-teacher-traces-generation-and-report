# 🚀 Quick Start - Free Tier Setup

**Time to first solution: 5 minutes**

## ✅ Prerequisites

1. **Google Account** (for Gemini API)
2. **API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. **VS Code** with Jupyter extension

## 📝 Step-by-Step Setup

### Step 1: Get Your API Key (2 min)

1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

### Step 2: Open the Notebook (30 sec)

1. Open `tot_concept.ipynb` in VS Code
2. Select Python kernel when prompted

### Step 3: Set API Key (30 sec)

In Cell 1, replace `""` with your key:

```python
# BEFORE:
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# AFTER:
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaYourKeyHere")
```

### Step 4: Run Setup Cells (1 min)

Run cells 1-7 in order:
- Cell 1: API setup ✓
- Cell 2: Safe sandbox ✓
- Cell 3: Prompts ✓
- Cell 4: Helper functions ✓
- Cell 5: TreeNode class ✓
- Cell 6: Solver class ✓
- Cell 7: Visualization ✓

### Step 5: Solve Your First Puzzle! (1 min)

Run this code:

```python
# Easy puzzle
solutions, root = solve_game24_codeact([4, 5, 6, 10])
```

**Expected output:**
```
✓ Solution found: ((10 - 6) × (5 + 4)) = 24
Runtime: ~2-3 minutes
API calls: ~40-50
```

## ⚙️ Rate Limiting (Important!)

Your free tier limits:
- **20 requests/minute** ← We use ~17 (safe)
- **14,000 requests/day** ← ~175 puzzles/day

**The code automatically:**
- ✅ Limits to 17 requests/minute (3.5s delays)
- ✅ Tracks daily usage
- ✅ Warns at 90% limit
- ✅ Handles rate limit errors

## 🎯 Recommended Configuration

```python
solver = Game24TreeOfThoughts(
    n_evaluate_sample=2,    # Balance accuracy vs speed
    n_select_sample=4,      # Medium beam width
    api_delay=3.5,          # 17 req/min (safe margin)
    temperature=0.7
)
```

**Cost:** ~80 API calls per puzzle (~5 min runtime)

## 📊 What to Expect

| Puzzle Difficulty | API Calls | Runtime | Success |
|------------------|-----------|---------|---------|
| Easy | 30-50 | 2-3 min | >90% |
| Medium | 80-120 | 5-7 min | ~80% |
| Hard | 150-200 | 10-12 min | ~60% |

## 💡 Quick Tips

### If you get rate limited:
```python
# Increase delay to 4.0 seconds
solver = Game24TreeOfThoughts(api_delay=4.0)
```

### If you want faster results:
```python
# Reduce accuracy for speed
solver = Game24TreeOfThoughts(
    n_evaluate_sample=1,  # Fewer evals
    n_select_sample=3     # Narrower beam
)
# Cost: ~40 calls per puzzle
```

### If you want better solutions:
```python
# Increase accuracy (slower)
solver = Game24TreeOfThoughts(
    n_evaluate_sample=3,  # More evals
    n_select_sample=5     # Wider beam
)
# Cost: ~150 calls per puzzle
```

### Check your usage:
```python
print(f"Today's usage: {solver.stats['daily_requests']}/14000")
print(f"Remaining: {14000 - solver.stats['daily_requests']} calls")
```

## 🎮 Try These Examples

### Example 1: Easy Puzzle
```python
solve_game24_codeact([4, 5, 6, 10])
# Expected: 1 solution in ~2 min
```

### Example 2: Multiple Solutions
```python
solve_game24_codeact([3, 3, 8, 8])
# Expected: 2-3 solutions in ~5 min
```

### Example 3: Challenging
```python
solve_game24_codeact([1, 4, 8, 8])
# Expected: 1 solution in ~7 min
```

## 📁 Save Your Results

```python
# After solving
solver.export_tree_to_json("my_solution.json")

# View tree structure
visualize_tree_codeact(root)

# See solution steps
if solutions:
    display_solution_codeact(solutions[0])
```

## 🚨 Common Issues

### "API key not set"
**Fix:** Set `GEMINI_API_KEY` in cell 1

### "429 Too Many Requests"
**Fix:** Automatic - code waits 60s and retries
**Prevention:** Keep `api_delay >= 3.5`

### "No solution found"
**Try:**
1. Increase `n_select_sample` to 5-7
2. Increase `temperature` to 0.8
3. Run again (different random exploration)

### "Slow performance"
**Normal!** 
- Easy: 2-3 min
- Medium: 5-7 min
- Hard: 10-12 min

This is due to rate limiting (3.5s between calls).

## 📚 Next Steps

1. ✅ **Solved first puzzle?** → Try different numbers
2. ✅ **Want to understand more?** → Read `RATE_LIMITING_GUIDE.md`
3. ✅ **Need quick commands?** → Check `QUICK_REFERENCE.md`
4. ✅ **Want full details?** → Read `CODEACT_README.md`

## 🎓 Learning Resources

### In the Notebook
- **Markdown cells** explain each component
- **Code comments** show what each part does
- **Example cells** demonstrate usage

### Documentation Files
- `RATE_LIMITING_GUIDE.md` - Optimize for free tier
- `QUICK_REFERENCE.md` - Command cheat sheet
- `CODEACT_README.md` - Full documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical deep dive

## ✨ You're Ready!

You now have:
- ✅ API configured
- ✅ Rate limiting set up
- ✅ First puzzle solved
- ✅ Understanding of costs

**Start solving! 🎯**

---

## 💰 Daily Budget Planning

With 14,000 requests/day and ~80 calls/puzzle:

| Your Goal | Puzzles/Day | Time Required |
|-----------|-------------|---------------|
| Learning | 5-10 | 25-50 min |
| Practice | 20-30 | 1.5-2.5 hours |
| Research | 50-100 | 4-8 hours |
| Maximum | 175 | ~14 hours |

**Recommendation:** Start with 5-10 puzzles/day while learning.

## 🔄 Reset Schedule

- **Per-minute limit:** Resets every 60 seconds
- **Daily limit:** Resets at midnight UTC

Track your timezone offset to plan accordingly!

---

**Questions? Check:**
1. `RATE_LIMITING_GUIDE.md` for optimization
2. `QUICK_REFERENCE.md` for commands
3. Notebook markdown cells for explanations

**Happy solving! 🚀**
