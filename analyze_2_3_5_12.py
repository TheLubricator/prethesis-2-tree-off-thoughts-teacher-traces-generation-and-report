import json

# Load the JSON file
with open('game24_codeact_tree_20260201_130110.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("ANALYSIS: Why [2,3,5,12] FAILED")
print("=" * 80)

# Check depth 1 operations
print("\nDEPTH 1 OPERATIONS (what was proposed):")
print("-" * 80)
for i, node in enumerate(data['nodes'][1:6], 1):
    thought = node['codeact']['thought']
    state = node['state']
    print(f"{i}. {thought}")
    print(f"   Result: {state}")

print("\n" + "=" * 80)
print("THE SOLUTION REQUIRES:")
print("=" * 80)
print("Step 1: 5 / 2 = 2.5  →  [2.5, 3, 12]  ← MUST DO THIS FIRST!")
print("Step 2: 3 - 2.5 = 0.5  →  [0.5, 12]")
print("Step 3: 12 / 0.5 = 24  →  [24] ✓")

print("\n" + "=" * 80)
print("WHY IT FAILED:")
print("=" * 80)

# Check if 5/2 was proposed at depth 1
depth1_ops = [node['codeact']['thought'] for node in data['nodes'][1:6]]
has_5_div_2 = any('5' in op and '2' in op and '/' in op and 'Divide 5 by 2' in op for op in depth1_ops)

if not has_5_div_2:
    print("❌ MISSING OPERATION: '5 / 2 = 2.5' was NOT proposed at depth 1")
    print("   Without this first step, the solution path is impossible to reach!")
else:
    print("✓ Operation '5 / 2 = 2.5' WAS proposed at depth 1")

# Check if it appeared later
print("\n" + "=" * 80)
print("DID IT APPEAR LATER?")
print("=" * 80)

found_2_5_with_3_and_12 = False
for node in data['nodes']:
    state = node['state']
    if '2.5' in state and '3' in state and '12' in state:
        found_2_5_with_3_and_12 = True
        print(f"✓ Found state {state} at depth {node['depth']}")
        print(f"  Path: {node['path_history'][:200]}...")
        break

if not found_2_5_with_3_and_12:
    print("❌ State [2.5, 3, 12] was NEVER reached in the entire search tree!")
    print("   This means the solver never tried '5 / 2' as the first operation.")

# Check if 5/2 was done but in wrong context
print("\n" + "=" * 80)
print("WAS '5 / 2' DONE IN WRONG CONTEXT?")
print("=" * 80)

for node in data['nodes']:
    thought = node['codeact']['thought']
    if 'Divide 5 by 2' in thought or '5 / 2' in thought:
        state = node['state']
        depth = node['depth']
        print(f"✓ Found '5 / 2' at depth {depth}")
        print(f"  Result state: {state}")
        print(f"  ❌ PROBLEM: This doesn't include both 3 and 12!")
        break

print("\n" + "=" * 80)
print("ROOT CAUSE:")
print("=" * 80)
print("The LLM did NOT propose '5 / 2' as a depth-1 operation.")
print("Instead, it proposed operations like:")
print("  - 2 + 3 = 5")
print("  - 2 * 5 = 10")
print("  - 12 - 3 = 9")
print("  - 12 / 2 = 6")
print("  - 3 * 5 = 15")
print("\nThe operation '5 / 2' was never considered with BOTH 3 and 12 available.")
print("This is a SEARCH SPACE issue, not a Tree of Thought algorithmic issue.")

print("\n" + "=" * 80)
print("STATISTICS:")
print("=" * 80)
print(f"Total nodes explored: {data['metadata']['statistics']['total_nodes']}")
print(f"Solutions found: {data['metadata']['statistics']['solutions_found']}")
print(f"Max depth: 4 (reached depth 3 terminal states)")
