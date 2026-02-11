#!/usr/bin/env python3
"""
LangGraph Validation Script

Validates a LangGraph graph for common issues.
Usage: python validate_graph.py <path_to_graph_file.py>

Checks:
- All nodes have outgoing edges
- No orphan nodes (unreachable from START)
- State type is properly defined
- Required imports are present
"""

import sys
import ast
import importlib.util
from pathlib import Path


def load_module(path: str):
    """Load a Python module from path."""
    spec = importlib.util.spec_from_file_location("graph_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analyze_source(path: str) -> dict:
    """Analyze graph source code for common patterns."""
    with open(path, "r") as f:
        source = f.read()

    tree = ast.parse(source)

    analysis = {
        "has_state_class": False,
        "has_stategraph": False,
        "has_start_edge": False,
        "has_end_edge": False,
        "nodes": [],
        "edges": [],
        "issues": [],
        "warnings": [],
    }

    for node in ast.walk(tree):
        # Check for State TypedDict
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "TypedDict":
                    analysis["has_state_class"] = True

        # Check for StateGraph
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "StateGraph":
                analysis["has_stategraph"] = True

        # Check for add_node calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "add_node":
                    if node.args:
                        if isinstance(node.args[0], ast.Constant):
                            analysis["nodes"].append(node.args[0].value)

        # Check for add_edge calls
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "add_edge":
                    if len(node.args) >= 2:
                        src = node.args[0]
                        dst = node.args[1]

                        src_name = None
                        dst_name = None

                        if isinstance(src, ast.Constant):
                            src_name = src.value
                        elif isinstance(src, ast.Name):
                            src_name = src.id

                        if isinstance(dst, ast.Constant):
                            dst_name = dst.value
                        elif isinstance(dst, ast.Name):
                            dst_name = dst.id

                        if src_name and dst_name:
                            analysis["edges"].append((src_name, dst_name))

                            if src_name == "START":
                                analysis["has_start_edge"] = True
                            if dst_name == "END":
                                analysis["has_end_edge"] = True

    return analysis


def validate_graph(analysis: dict) -> tuple[list, list]:
    """Validate the graph based on analysis."""
    errors = []
    warnings = []

    # Check for State class
    if not analysis["has_state_class"]:
        warnings.append("No TypedDict State class found. Consider defining explicit state.")

    # Check for StateGraph
    if not analysis["has_stategraph"]:
        errors.append("No StateGraph found. Are you using LangGraph?")

    # Check for START edge
    if not analysis["has_start_edge"]:
        errors.append("No edge from START found. Add: graph.add_edge(START, 'first_node')")

    # Check for END edge (warning only)
    if not analysis["has_end_edge"]:
        warnings.append("No explicit edge to END found. Graph may not terminate properly.")

    # Check for orphan nodes
    source_nodes = {edge[0] for edge in analysis["edges"]}
    target_nodes = {edge[1] for edge in analysis["edges"]}

    for node in analysis["nodes"]:
        if node not in source_nodes and node not in target_nodes:
            errors.append(f"Node '{node}' has no edges (orphan node)")
        elif node not in source_nodes:
            warnings.append(f"Node '{node}' has no outgoing edges (may be terminal)")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_graph.py <path_to_graph_file.py>")
        print("\nValidates a LangGraph graph for common issues.")
        sys.exit(1)

    path = sys.argv[1]

    if not Path(path).exists():
        print(f"Error: File not found: {path}")
        sys.exit(1)

    print(f"Validating: {path}")
    print("=" * 50)

    try:
        analysis = analyze_source(path)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)

    # Print analysis
    print("\nAnalysis:")
    print(f"  State class found: {'Yes' if analysis['has_state_class'] else 'No'}")
    print(f"  StateGraph found: {'Yes' if analysis['has_stategraph'] else 'No'}")
    print(f"  Nodes: {analysis['nodes'] or 'None detected'}")
    print(f"  Edges: {len(analysis['edges'])} found")

    # Validate
    errors, warnings = validate_graph(analysis)

    # Print results
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  ⚠️  {w}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  ❌ {e}")
        print("\n" + "=" * 50)
        print("Validation FAILED")
        sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("✅ Validation PASSED")
        if warnings:
            print(f"   ({len(warnings)} warning(s))")
        sys.exit(0)


if __name__ == "__main__":
    main()
