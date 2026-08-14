#!/usr/bin/env python3
import os
import sys
import json
import re

# ==========================================
# Pure Python Fallback Implementations
# ==========================================

def parse_yaml_fallback(text):
    """
    A custom, lightweight YAML parser for a subset of YAML used in OKF.
    Handles nested dicts and lists based on line indentation.
    """
    lines = []
    for line in text.splitlines():
        # Strip trailing comments (only if space-padded before # or end of line)
        content = re.sub(r'\s+#.*$', '', line).rstrip()
        if content and not content.lstrip().startswith('#'):
            # tab-to-space normalization
            content_normalized = content.replace('\t', '    ')
            indent = len(content_normalized) - len(content_normalized.lstrip())
            lines.append((indent, content_normalized.lstrip()))
            
    if not lines:
        return {}

    def parse_block(index, parent_indent):
        if index >= len(lines):
            return None, index
        
        cur_indent, cur_line = lines[index]
        
        # Check if list item at this parent indent
        if cur_line.startswith('-'):
            list_res = []
            while index < len(lines):
                c_indent, c_line = lines[index]
                if c_indent < parent_indent:
                    break
                
                if c_line.startswith('-'):
                    item_content = c_line[1:].strip()
                    if not item_content:
                        # Block list of dicts or nested list
                        next_indent = -1
                        for lookup in range(index + 1, len(lines)):
                            if lines[lookup][0] > c_indent:
                                next_indent = lines[lookup][0]
                                break
                            elif lines[lookup][0] <= c_indent:
                                break
                        if next_indent != -1:
                            item_val, index = parse_block(index + 1, next_indent)
                            list_res.append(item_val)
                        else:
                            list_res.append(None)
                            index += 1
                    elif ':' in item_content and re.search(r':(\s|$)', item_content):
                        # Convert line into a dict entry and parse it as a dict under virtual deeper indent
                        lines[index] = (c_indent + 2, item_content)
                        dict_item, index = parse_block(index, c_indent + 2)
                        list_res.append(dict_item)
                    else:
                        # Standard list item
                        list_res.append(parse_scalar(item_content))
                        index += 1
                else:
                    break
            return list_res, index

        # Parse dict item
        dict_res = {}
        while index < len(lines):
            c_indent, c_line = lines[index]
            if c_indent < parent_indent:
                break
                
            match = re.match(r'^([^:]+):\s*(.*)$', c_line)
            if not match:
                index += 1
                continue
                
            key = match.group(1).strip()
            val_str = match.group(2).strip()
            
            if val_str:
                dict_res[key] = parse_scalar(val_str)
                index += 1
            else:
                # Key with nested block
                next_index = index + 1
                if next_index < len(lines) and lines[next_index][0] > c_indent:
                    nested_val, next_index = parse_block(next_index, lines[next_index][0])
                    dict_res[key] = nested_val
                    index = next_index
                else:
                    dict_res[key] = None
                    index += 1
                    
        return dict_res, index

    def parse_scalar(val_str):
        if val_str.lower() in ('true', 'yes', 'on'):
            return True
        if val_str.lower() in ('false', 'no', 'off'):
            return False
        if re.match(r'^-?\d+$', val_str):
            return int(val_str)
        if re.match(r'^-?\d+\.\d+$', val_str):
            return float(val_str)
        if val_str.startswith('[') and val_str.endswith(']'):
            items = val_str[1:-1].split(',')
            return [parse_scalar(item.strip()) for item in items if item.strip()]
        if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
            return val_str[1:-1]
        return val_str

    parsed_obj, _ = parse_block(0, lines[0][0])
    return parsed_obj


def validate_schema_fallback(data, schema, path=""):
    """
    A custom, lightweight JSON Schema Draft-07 validator.
    Supports type, properties, required, items, enum, pattern.
    """
    if not isinstance(schema, dict):
        return []
    
    errors = []
    
    # Check type
    expected_type = schema.get("type")
    if expected_type:
        if expected_type == "object" and not isinstance(data, dict):
            errors.append(f"{path}: expected object, got {type(data).__name__}")
        elif expected_type == "array" and not isinstance(data, list):
            errors.append(f"{path}: expected array, got {type(data).__name__}")
        elif expected_type == "string" and not isinstance(data, str):
            errors.append(f"{path}: expected string, got {type(data).__name__}")
        elif expected_type == "boolean" and not isinstance(data, bool):
            errors.append(f"{path}: expected boolean, got {type(data).__name__}")
            
    # Check enum
    enum_vals = schema.get("enum")
    if enum_vals is not None and data not in enum_vals:
        errors.append(f"{path}: value {repr(data)} not in enum {enum_vals}")
        
    # Check pattern (regex)
    pattern = schema.get("pattern")
    if pattern and isinstance(data, str):
        if not re.search(pattern, data):
            errors.append(f"{path}: '{data}' does not match pattern '{pattern}'")
            
    # Check required properties for object
    if isinstance(data, dict):
        required = schema.get("required", [])
        for req in required:
            if req not in data:
                errors.append(f"{path}: missing required property '{req}'" if path else f"missing required property '{req}'")
                
        # Check properties recursively
        properties = schema.get("properties", {})
        for prop_name, prop_schema in properties.items():
            if prop_name in data:
                subpath = f"{path}.{prop_name}" if path else prop_name
                errors.extend(validate_schema_fallback(data[prop_name], prop_schema, subpath))
                
    # Check array items
    if isinstance(data, list) and "items" in schema:
        item_schema = schema["items"]
        for idx, item in enumerate(data):
            errors.extend(validate_schema_fallback(item, item_schema, f"{path}[{idx}]"))
            
    return errors


# ==========================================
# Main Validation Logic
# ==========================================

def stringify_datetimes(obj):
    import datetime
    if isinstance(obj, dict):
        return {k: stringify_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [stringify_datetimes(x) for x in obj]
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        # Convert datetime objects to ISO 8601 strings
        return obj.isoformat().replace('+00:00', 'Z')
    return obj

def load_yaml(content):
    try:
        import yaml
        data = yaml.safe_load(content)
    except ImportError:
        data = parse_yaml_fallback(content)
    return stringify_datetimes(data)

def validate_data(data, schema):
    try:
        import jsonschema
        jsonschema.validate(instance=data, schema=schema)
        return []
    except ImportError:
        return validate_schema_fallback(data, schema)
    except Exception as e:
        return [str(e)]

def extract_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Matches markdown frontmatter blocks delimited by ---
    # We must match exactly at the beginning of the file
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, None
    
    frontmatter = match.group(1)
    body = match.group(2)
    return frontmatter, body

def main():
    print("=" * 60)
    print("Google OKF v0.2 JUNOS Knowledge Validator")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    schemas_dir = os.path.join(root_dir, 'schemas')
    knowledge_dir = os.path.join(root_dir, 'knowledge')
    
    frontmatter_schema_path = os.path.join(schemas_dir, 'okf-frontmatter-schema.json')
    
    try:
        with open(frontmatter_schema_path, 'r', encoding='utf-8') as f:
            frontmatter_schema = json.load(f)
    except Exception as e:
        print(f"[-] Failed to load validation schema from {schemas_dir}: {e}")
        sys.exit(1)
        
    validation_passed = True
    total_files_checked = 0
    total_errors = 0
    
    print("[+] Scanning knowledge directory recursively for OKF Markdown (.md) files...")
    
    for dirpath, dirnames, filenames in os.walk(knowledge_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                total_files_checked += 1
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, root_dir)
                print(f"\n[~] Checking OKF Document: {rel_path}")
                
                frontmatter_str, body = extract_frontmatter(filepath)
                if frontmatter_str is None:
                    print("  [-] Error: Missing or malformed YAML frontmatter (must start with ---, have body, end with ---).")
                    total_errors += 1
                    validation_passed = False
                    continue
                
                # Parse frontmatter
                try:
                    data = load_yaml(frontmatter_str)
                except Exception as e:
                    print(f"  [-] Error parsing frontmatter YAML: {e}")
                    total_errors += 1
                    validation_passed = False
                    continue
                    
                if not data:
                    print("  [-] Error: Frontmatter is empty")
                    total_errors += 1
                    validation_passed = False
                    continue
                
                # Validate frontmatter against schema
                schema_errors = validate_data(data, frontmatter_schema)
                if schema_errors:
                    print(f"  [-] Frontmatter failed schema validation:")
                    for err in schema_errors:
                        print(f"      * {err}")
                        total_errors += 1
                    validation_passed = False
                    continue
                
                print("  [+] YAML Frontmatter complies with OKF v0.2 schema.")
                
                doc_type = data.get("type")
                
                # Custom block checking based on type
                if doc_type == "JUNOS Base Config":
                    # Check that the markdown body contains a codeblock of type set
                    # Matches both ```set ... ``` and ```set\n...```
                    if not re.search(r'```set\s*\n.*?\n```', body, re.DOTALL):
                        print("  [-] Error: Base configuration missing a valid '```set ... ```' codeblock in the body.")
                        total_errors += 1
                        validation_passed = False
                    else:
                        print("  [+] JUNOS Configuration set codeblock found.")
                        
                elif doc_type == "JUNOS Audit":
                    # For audit items, verification_method and checks must be defined
                    missing = []
                    if "verification_method" not in data:
                        missing.append("verification_method")
                    if "checks" not in data:
                        missing.append("checks")
                        
                    if missing:
                        print(f"  [-] Error: Audit item frontmatter is missing required fields: {', '.join(missing)}")
                        for m in missing:
                            total_errors += 1
                        validation_passed = False
                    else:
                        print("  [+] Compliance audit validation metrics found in frontmatter.")
                        
                elif doc_type == "Apstra Configuration":
                    # Check that the markdown body contains a valid json API payload codeblock
                    if not re.search(r'```json\s*\n.*?\n```', body, re.DOTALL):
                        print("  [-] Error: Apstra configuration missing a valid '```json ... ```' API payload codeblock in the body.")
                        total_errors += 1
                        validation_passed = False
                    else:
                        print("  [+] Apstra API configuration JSON payload codeblock found.")
                        
                elif doc_type == "meta":
                    print("  [+] Meta-knowledge tracking document validated successfully.")
                    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print(f"Total Files Checked:   {total_files_checked}")
    print(f"Total Errors Found:    {total_errors}")
    print("=" * 60)
    
    if validation_passed and total_files_checked > 0:
        print("[+] SUCCESS: All OKF markdown files are completely conformant!")
        sys.exit(0)
    else:
        print("[-] FAILURE: Found validation issues in the repository.")
        sys.exit(1)

if __name__ == '__main__':
    main()
