"""
Demo script to demonstrate PyHop plugin functionality.

This script shows how to:
1. Import and use the PyHop framework
2. Work with example plugins
3. Process data through transforms
4. Execute actions
"""

from pyhop import plugin_registry
from examples.uppercase_transform import UpperCaseTransform
from examples.calculated_field_transform import CalculatedFieldTransform
from examples.filewriter_action import FileWriterAction


def demo_transform_plugins():
    """Demonstrate transform plugin functionality."""
    print("=" * 60)
    print("TRANSFORM PLUGIN DEMONSTRATION")
    print("=" * 60)

    # Demo 1: UpperCase Transform
    print("\n1. UpperCase Transform")
    print("-" * 40)

    transform = UpperCaseTransform()
    transform.init()

    # Sample data
    test_rows = [
        {"name": "john doe", "city": "boston", "country": "usa"},
        {"name": "jane smith", "city": "london", "country": "uk"},
        {"name": "bob johnson", "city": "paris", "country": "france"},
    ]

    print(f"Plugin ID: {transform.get_id()}")
    print(f"Plugin Name: {transform.get_name()}")
    print(f"Description: {transform.get_description()}\n")

    print("Input rows:")
    for row in test_rows:
        print(f"  {row}")

    print("\nProcessing...")
    results = []
    for row in test_rows:
        result = transform.process_row(row.copy())
        results.append(result)

    print("\nOutput rows:")
    for row in results:
        print(f"  {row}")

    transform.dispose()

    # Demo 2: Calculated Field Transform
    print("\n\n2. Calculated Field Transform")
    print("-" * 40)

    calc_transform = CalculatedFieldTransform()
    calc_transform.configure("quantity", "unit_price", "total_price")
    calc_transform.init()

    # Sample data with numeric fields
    sales_rows = [
        {"product": "Widget", "quantity": 5, "unit_price": 10.00},
        {"product": "Gadget", "quantity": 3, "unit_price": 25.50},
        {"product": "Doohickey", "quantity": 10, "unit_price": 5.75},
    ]

    print(f"Plugin ID: {calc_transform.get_id()}")
    print(f"Configuration: {calc_transform.quantity_field} × {calc_transform.price_field} = {calc_transform.output_field}\n")

    print("Input rows:")
    for row in sales_rows:
        print(f"  {row}")

    print("\nProcessing...")
    calc_results = []
    for row in sales_rows:
        result = calc_transform.process_row(row.copy())
        calc_results.append(result)

    print("\nOutput rows:")
    for row in calc_results:
        print(f"  {row}")

    calc_transform.dispose()


def demo_action_plugins():
    """Demonstrate action plugin functionality."""
    print("\n\n" + "=" * 60)
    print("ACTION PLUGIN DEMONSTRATION")
    print("=" * 60)

    # Demo 1: File Writer Action
    print("\n1. FileWriter Action")
    print("-" * 40)

    action = FileWriterAction()
    action.set_parameter("filepath", "/tmp/pyhop_demo.txt")
    action.set_parameter("message", "Hello from PyHop demo!")
    action.set_parameter("append", False)

    print(f"Plugin ID: {action.get_id()}")
    print(f"Plugin Name: {action.get_name()}")
    print(f"Description: {action.get_description()}\n")

    print("Parameters:")
    for key, value in action.get_parameters().items():
        print(f"  {key}: {value}")

    print("\nExecuting action...")
    success = action.execute()

    if success:
        print("✓ Action completed successfully!")
        print(f"Check the file at: {action.get_parameter('filepath')}")
    else:
        print("✗ Action failed!")


def demo_plugin_registry():
    """Demonstrate plugin registry functionality."""
    print("\n\n" + "=" * 60)
    print("PLUGIN REGISTRY DEMONSTRATION")
    print("=" * 60)

    print("\nRegistered plugins:")
    all_plugins = plugin_registry.list_plugins()
    for plugin_id in all_plugins:
        plugin_class = plugin_registry.get_plugin_class(plugin_id)
        if plugin_class:
            temp = plugin_class("temp", "")
            print(f"  - {plugin_id} ({temp.get_category()})")

    print("\nTransform plugins:")
    transforms = plugin_registry.list_plugins(category="Transform")
    for plugin_id in transforms:
        print(f"  - {plugin_id}")

    print("\nAction plugins:")
    actions = plugin_registry.list_plugins(category="Action")
    for plugin_id in actions:
        print(f"  - {plugin_id}")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  PyHop - Python Plugins for Apache Hop".center(58) + "║")
    print("║" + "  Demonstration Script".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")

    try:
        # Run demonstrations
        demo_transform_plugins()
        demo_action_plugins()
        demo_plugin_registry()

        print("\n\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("\nFor more information:")
        print("  - Documentation: docs/")
        print("  - Examples: examples/")
        print("  - Templates: templates/")
        print("  - Repository: https://github.com/metaodi/pyhop")
        print()

    except Exception as e:
        print(f"\n\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
