import json

def print_tree(node, indent=0):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                print("  " * indent + f"{key}:")
                print_tree(value, indent + 1)
            else:
                try:
                    serialized_value = json.dumps(value)
                    print("  " * indent + f"{key}: {serialized_value}")
                except TypeError:
                    print("  " * indent + f"{key}: [Non-serializable]")
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                print_tree(item, indent)
            else:
                try:
                    serialized_item = json.dumps(item)
                    print("  " * indent + f"- {serialized_item}")
                except TypeError:
                    print("  " * indent + "- [Non-serializable]")