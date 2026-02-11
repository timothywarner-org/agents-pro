"""Test script for MCP server - verifies tools, resources, and prompts are accessible."""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_mvp.mcp_server.server import mcp


def test_tools():
    """Verify all expected tools are registered."""
    print("=" * 60)
    print("TOOLS TEST")
    print("=" * 60)

    expected_tools = [
        "fetch_github_issue",
        "list_mock_issues",
        "load_mock_issue",
        "run_agent_pipeline",
        "process_issue_file",
    ]

    # Get registered tool names from FastMCP
    registered_tools = []
    for name, tool_func in mcp._tools.items():
        registered_tools.append(name)
        print(f"✓ {name}")
        # Show docstring
        if tool_func.__doc__:
            doc = tool_func.__doc__.strip().split("\n")[0]
            print(f"  {doc}")

    print(f"\nTotal: {len(registered_tools)} tools registered")

    # Check if all expected tools are present
    missing = set(expected_tools) - set(registered_tools)
    if missing:
        print(f"\n❌ Missing tools: {missing}")
        return False

    print("✅ All tools present\n")
    return True


def test_resources():
    """Verify all expected resources are registered."""
    print("=" * 60)
    print("RESOURCES TEST")
    print("=" * 60)

    expected_resources = [
        "config://settings",
        "issues://mock/{filename}",
        "pipeline://schema",
        "pipeline://architecture",
    ]

    # Get registered resource patterns from FastMCP
    registered_resources = []
    for uri_template, resource_func in mcp._resources.items():
        registered_resources.append(uri_template)
        print(f"✓ {uri_template}")
        # Show docstring
        if resource_func.__doc__:
            doc = resource_func.__doc__.strip().split("\n")[0]
            print(f"  {doc}")

    print(f"\nTotal: {len(registered_resources)} resources registered")

    # Check if all expected resources are present
    missing = set(expected_resources) - set(registered_resources)
    if missing:
        print(f"\n❌ Missing resources: {missing}")
        return False

    print("✅ All resources present\n")
    return True


def test_prompts():
    """Verify all expected prompts are registered."""
    print("=" * 60)
    print("PROMPTS TEST")
    print("=" * 60)

    expected_prompts = [
        "analyze_github_issue",
        "review_implementation_plan",
        "generate_test_issue",
    ]

    # Get registered prompt names from FastMCP
    registered_prompts = []
    for name, prompt_func in mcp._prompts.items():
        registered_prompts.append(name)
        print(f"✓ {name}")
        # Show docstring
        if prompt_func.__doc__:
            doc = prompt_func.__doc__.strip().split("\n")[0]
            print(f"  {doc}")

    print(f"\nTotal: {len(registered_prompts)} prompts registered")

    # Check if all expected prompts are present
    missing = set(expected_prompts) - set(registered_prompts)
    if missing:
        print(f"\n❌ Missing prompts: {missing}")
        return False

    print("✅ All prompts present\n")
    return True


def test_server_metadata():
    """Verify server metadata is configured."""
    print("=" * 60)
    print("SERVER METADATA TEST")
    print("=" * 60)

    print(f"Server Name: {mcp.name}")
    print(f"Instructions: {mcp.instructions[:100]}...")

    if not mcp.name:
        print("❌ Server name not set")
        return False

    if not mcp.instructions:
        print("❌ Server instructions not set")
        return False

    print("✅ Metadata configured\n")
    return True


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "MCP SERVER VALIDATION TEST" + " " * 22 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    results = []

    results.append(("Server Metadata", test_server_metadata()))
    results.append(("Tools", test_tools()))
    results.append(("Resources", test_resources()))
    results.append(("Prompts", test_prompts()))

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = all(result for _, result in results)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n")

    if all_passed:
        print("🎉 All tests passed! MCP server is ready to use.")
        print("\nNext steps:")
        print("  1. Start server: agent-mcp")
        print("  2. Configure Claude Desktop (see .mcp/claude_desktop_config.json)")
        print("  3. Configure VS Code (see .vscode/mcp.json)")
        return 0
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
