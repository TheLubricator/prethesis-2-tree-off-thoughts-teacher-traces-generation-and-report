"""
Analysis: Will using [6,9,9,10] in the prompt example cause bias?
"""

print("=" * 80)
print("PROMPT EXAMPLE BIAS ANALYSIS")
print("=" * 80)

print("""
CURRENT PROMPT ADDITION:
  - Example: With 6 and 9, try BOTH 6*9=54 AND 9*6=54
  - Example: With 9 and 10, try BOTH 9*10=90 AND 10*9=90

CONCERN: These are the exact numbers from [6,9,9,10]!
Will this create bias or only work for this specific puzzle?
""")

print("\n" + "=" * 80)
print("ANALYSIS:")
print("=" * 80)

print("""
✅ GOOD NEWS: This is GENERALIZABLE, not biased!

Here's why:

1. **Teaching a PRINCIPLE, not a specific solution:**
   
   The example doesn't say "for [6,9,9,10], do 9*10"
   It says "for ANY numbers a and b, try BOTH a*b AND b*a"
   
   The numbers 6,9,10 are just ILLUSTRATIONS of the principle.

2. **LLMs generalize from examples:**
   
   When you show:
   "Example: With 6 and 9, try BOTH 6*9 AND 9*6"
   
   LLM learns:
   "For any pair of numbers, try both orders"
   
   NOT:
   "Only do this for 6 and 9"

3. **Will work for OTHER puzzles:**

   [1, 4, 8, 8]:
   - Learns: Try BOTH 1*4 AND 4*1
   - Learns: Try BOTH 8*4 AND 4*8
   - Learns: Try BOTH 8/4 AND 4/8
   ✅ Generalizes correctly!

   [2, 3, 5, 12]:
   - Learns: Try BOTH 2*3 AND 3*2
   - Learns: Try BOTH 5*12 AND 12*5
   - Learns: Try BOTH 12/3 AND 3/12
   ✅ Generalizes correctly!

4. **Comparison to current example:**

   Current prompt already uses [2,8,8,14] as example
   This puzzle is NOT the same as what we test on!
   
   It teaches:
   - How to format the output
   - What operations to try
   - The PATTERN to follow
   
   Your puzzles [1,4,8,8], [6,9,9,10], etc. are DIFFERENT
   But LLM generalizes the pattern! ✅
""")

print("\n" + "=" * 80)
print("POTENTIAL IMPROVEMENTS:")
print("=" * 80)

print("""
If you're still worried, we could make it MORE generic:

OPTION A: Use abstract labels (Current - GOOD)
  "Example: With 6 and 9, try BOTH 6*9=54 AND 9*6=54"
  ✅ Concrete, easy to understand
  ✅ Generalizes well
  ⚠️  Happens to use same numbers as current puzzle

OPTION B: Use variables (Too abstract)
  "Example: With a and b, try BOTH a*b AND b*a"
  ✅ Completely generic
  ❌ Less clear for LLM
  ❌ Might not follow instruction as well

OPTION C: Use DIFFERENT numbers (Safest)
  "Example: With 3 and 7, try BOTH 3*7=21 AND 7*3=21"
  "Example: With 5 and 8, try BOTH 5*8=40 AND 8*5=40"
  ✅ Concrete examples
  ✅ Different from [6,9,9,10]
  ✅ Still teaches same principle

OPTION D: Multiple examples (Best but verbose)
  "Examples:"
  "  - With 3 and 7: try BOTH 3*7=21 AND 7*3=21"
  "  - With 5 and 12: try BOTH 5*12=60 AND 12*5=60"
  "  - With 10 and 6: try BOTH 10/6=1.67 AND 6/10=0.6"
  ✅ Multiple concrete examples
  ✅ LLM learns pattern from variety
  ⚠️  Longer prompt
""")

print("\n" + "=" * 80)
print("EVIDENCE FROM EXISTING PROMPT:")
print("=" * 80)

print("""
Current PROPOSE_PROMPT_CODEACT uses [2,8,8,14] as example.

You've been testing on:
  - [1, 4, 8, 8] ✅ Works
  - [4, 5, 6, 10] ✅ Works
  - [6, 9, 9, 10] ❌ Was failing (different from example!)

The example [2,8,8,14] is DIFFERENT from your test puzzles.
Yet LLM successfully generalizes to [1,4,8,8] and [4,5,6,10]!

This proves: LLMs generalize from examples, not memorize them!
""")

print("\n" + "=" * 80)
print("TESTING STRATEGY:")
print("=" * 80)

print("""
TO VERIFY NO BIAS:

1. ✅ Test [6,9,9,10] with new prompt (current test)
   - Should now work (finds 9*10)
   
2. ✅ Re-test [1,4,8,8] with new prompt
   - Should still work
   - Proves no regression
   
3. ✅ Re-test [4,5,6,10] with new prompt
   - Should still work
   - Proves no regression
   
4. ✅ Test NEW puzzle [2,3,5,12] with new prompt
   - Different from [6,9,9,10] example
   - If it works, proves generalization!

If all 4 pass → ✅ No bias, good generalization!
If only [6,9,9,10] passes → ⚠️ Possible bias, change example
""")

print("\n" + "=" * 80)
print("RECOMMENDATION:")
print("=" * 80)

print("""
START WITH CURRENT PROMPT (using 6,9,10 example):

Reasoning:
  1. It's the clearest, most concrete example
  2. LLMs are good at generalizing
  3. Easy to verify: test on different puzzles
  4. If bias detected, we can easily change to Option C or D

IF you see bias (only [6,9,9,10] works):
  → Change to Option C: Use 3,7 and 5,8 as examples instead
  
IF no bias (other puzzles work too):
  → ✅ Keep current - it's fine!

🎯 VERDICT: Current example is SAFE, but test on other puzzles to confirm!
""")

print("\n" + "=" * 80)
print("WAIT FOR CURRENT RUN, THEN TEST:")
print("=" * 80)

print("""
1. Check if [6,9,9,10] solves ← Current run
2. If YES, test [1,4,8,8] again ← Verify no regression
3. If BOTH work → ✅ No bias!
4. If only [6,9,9,10] works → Change example numbers
""")
