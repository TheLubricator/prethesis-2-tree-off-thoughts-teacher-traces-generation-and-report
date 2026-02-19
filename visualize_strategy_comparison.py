import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Data collection
base_dir = Path(r"g:\class codes\tree-of-thought-llm\tot_concept finished trees-temp 1  general prompt")

strategy1_files = [
    ("game24_codeact_tree_20260131_162843.json", "[1,4,8,8]"),
    ("game24_codeact_tree_20260201_004023.json", "[3,3,8,8]"),
    ("game24_codeact_tree_20260201_011421.json", "[4,5,6,10]"),
    ("game24_codeact_tree_20260201_020942.json", "[1,4,8,8]"),
    ("game24_codeact_tree_20260201_023410.json", "[2,3,5,12]")
]

temp07_dir = base_dir / "temperature 0.7 multiplication prompt added probablistic selection"
strategy2_files = [
    ("game24_codeact_tree_20260201_113821.json", "[6,9,9,10]"),
    ("game24_codeact_tree_20260201_115322.json", "[1,3,8,8]"),
    ("game24_codeact_tree_20260201_121221.json", "[1,4,8,8]"),
    ("game24_codeact_tree_20260201_123613.json", "[4,5,6,10]"),
    ("game24_codeact_tree_20260201_130110.json", "[2,3,5,12]")
]

def load_stats(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {
        'total_nodes': data['metadata']['statistics']['total_nodes'],
        'api_calls': data['metadata']['statistics']['api_calls'],
        'solution_found': data['metadata']['statistics']['solutions_found'] > 0
    }

# Collect data
s1_data = []
s1_puzzles = []
for filename, puzzle in strategy1_files:
    path = base_dir / filename
    if path.exists():
        stats = load_stats(path)
        s1_data.append(stats)
        s1_puzzles.append(puzzle)

s2_data = []
s2_puzzles = []
for filename, puzzle in strategy2_files:
    path = temp07_dir / filename
    if path.exists():
        stats = load_stats(path)
        s2_data.append(stats)
        s2_puzzles.append(puzzle)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Tree of Thought Strategy Comparison', fontsize=16, fontweight='bold')

# 1. Success Rate
ax1 = axes[0, 0]
s1_success = sum(1 for d in s1_data if d['solution_found'])
s2_success = sum(1 for d in s2_data if d['solution_found'])
s1_rate = s1_success / len(s1_data) * 100 if s1_data else 0
s2_rate = s2_success / len(s2_data) * 100 if s2_data else 0

strategies = ['Strategy 1\n(Temp 1.0, Greedy)', 'Strategy 2\n(Temp 0.7, Probabilistic)']
success_rates = [s1_rate, s2_rate]
colors = ['#e74c3c', '#27ae60']

bars = ax1.bar(strategies, success_rates, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('Success Rate Comparison', fontsize=13, fontweight='bold')
ax1.set_ylim(0, 100)
ax1.axhline(y=74, color='gray', linestyle='--', linewidth=2, label='Original ToT Paper (74%)')
ax1.legend()

# Add percentage labels on bars
for bar, rate in zip(bars, success_rates):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{rate:.1f}%',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

ax1.grid(axis='y', alpha=0.3)

# 2. Average Nodes
ax2 = axes[0, 1]
s1_avg_nodes = sum(d['total_nodes'] for d in s1_data) / len(s1_data) if s1_data else 0
s2_avg_nodes = sum(d['total_nodes'] for d in s2_data) / len(s2_data) if s2_data else 0

avg_nodes = [s1_avg_nodes, s2_avg_nodes]
bars = ax2.bar(strategies, avg_nodes, color=['#3498db', '#9b59b6'], alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_ylabel('Average Nodes', fontsize=12, fontweight='bold')
ax2.set_title('Search Tree Size', fontsize=13, fontweight='bold')

# Add value labels
for bar, nodes in zip(bars, avg_nodes):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{nodes:.1f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

ax2.grid(axis='y', alpha=0.3)

# 3. Average API Calls
ax3 = axes[1, 0]
s1_avg_api = sum(d['api_calls'] for d in s1_data) / len(s1_data) if s1_data else 0
s2_avg_api = sum(d['api_calls'] for d in s2_data) / len(s2_data) if s2_data else 0

avg_api = [s1_avg_api, s2_avg_api]
bars = ax3.bar(strategies, avg_api, color=['#e67e22', '#1abc9c'], alpha=0.7, edgecolor='black', linewidth=2)
ax3.set_ylabel('Average API Calls', fontsize=12, fontweight='bold')
ax3.set_title('Computational Cost', fontsize=13, fontweight='bold')

# Add value labels
for bar, api in zip(bars, avg_api):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{api:.1f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

ax3.grid(axis='y', alpha=0.3)

# 4. Puzzle-by-Puzzle Success
ax4 = axes[1, 1]

# Common puzzles
common_puzzles = {
    '[1,4,8,8]': {'s1': True, 's2': True},
    '[4,5,6,10]': {'s1': True, 's2': True},
    '[2,3,5,12]': {'s1': False, 's2': False},
}

puzzle_names = list(common_puzzles.keys()) + ['[6,9,9,10]\n(NEW)']
x = np.arange(len(puzzle_names))
width = 0.35

s1_results = [1 if common_puzzles[p]['s1'] else 0 for p in list(common_puzzles.keys())] + [0]
s2_results = [1 if common_puzzles[p]['s2'] else 0 for p in list(common_puzzles.keys())] + [1]

bars1 = ax4.bar(x - width/2, s1_results, width, label='Strategy 1', color='#e74c3c', alpha=0.7, edgecolor='black')
bars2 = ax4.bar(x + width/2, s2_results, width, label='Strategy 2', color='#27ae60', alpha=0.7, edgecolor='black')

ax4.set_ylabel('Solved (1) / Failed (0)', fontsize=12, fontweight='bold')
ax4.set_title('Puzzle-by-Puzzle Results', fontsize=13, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(puzzle_names, fontsize=9)
ax4.set_ylim(0, 1.2)
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

# Add emoji indicators
for i, (bar1, bar2, result1, result2) in enumerate(zip(bars1, bars2, s1_results, s2_results)):
    if result1:
        ax4.text(bar1.get_x() + bar1.get_width()/2., result1 + 0.05, '✓', 
                ha='center', fontsize=16, color='green')
    else:
        ax4.text(bar1.get_x() + bar1.get_width()/2., 0.05, '✗', 
                ha='center', fontsize=16, color='red')
    
    if result2:
        ax4.text(bar2.get_x() + bar2.get_width()/2., result2 + 0.05, '✓', 
                ha='center', fontsize=16, color='green')
    else:
        ax4.text(bar2.get_x() + bar2.get_width()/2., 0.05, '✗', 
                ha='center', fontsize=16, color='red')

plt.tight_layout()

# Save figure
output_path = Path(r"g:\class codes\tree-of-thought-llm\strategy_comparison_visualization.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Visualization saved to: {output_path}")

# Display summary
print("\n" + "=" * 80)
print("STRATEGY COMPARISON SUMMARY")
print("=" * 80)
print(f"\nStrategy 1 (Temp 1.0, Greedy, General Prompt):")
print(f"  Success Rate: {s1_rate:.1f}% ({s1_success}/{len(s1_data)} puzzles)")
print(f"  Avg Nodes: {s1_avg_nodes:.1f}")
print(f"  Avg API Calls: {s1_avg_api:.1f}")

print(f"\nStrategy 2 (Temp 0.7, Probabilistic, Enhanced Prompt):")
print(f"  Success Rate: {s2_rate:.1f}% ({s2_success}/{len(s2_data)} puzzles)")
print(f"  Avg Nodes: {s2_avg_nodes:.1f}")
print(f"  Avg API Calls: {s2_avg_api:.1f}")

print(f"\nImprovements:")
print(f"  Success Rate: {s2_rate - s1_rate:+.1f}%")
print(f"  Nodes: {s2_avg_nodes - s1_avg_nodes:+.1f} ({(s2_avg_nodes/s1_avg_nodes - 1)*100:+.1f}%)")
print(f"  API Calls: {s2_avg_api - s1_avg_api:+.1f} ({(s2_avg_api/s1_avg_api - 1)*100:+.1f}%)")

print("\n" + "=" * 80)

plt.show()
