#!/usr/bin/env python3
"""Validate JSON documents against the contract-focused JSON Schema subset used by star-list."""
import argparse
import json
import re
from pathlib import Path

def _matches_type(value, expected):
    if expected == "object": return isinstance(value, dict)
    if expected == "array": return isinstance(value, list)
    if expected == "string": return isinstance(value, str)
    if expected == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number": return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean": return isinstance(value, bool)
    if expected == "null": return value is None
    return False

def _path(parent, key):
    if isinstance(key, int):
        return f"{parent}[{key}]"
    return f"{parent}.{key}" if parent != "$" else f"$.{key}"

SUPPORTED_KEYWORDS={
    "$schema","title","type","required","properties","additionalProperties",
    "anyOf","const","enum","items","minItems","maxItems","uniqueItems",
    "minLength","pattern","minimum","maximum"
}

def validate(value, schema, path="$"):
    errors=[]
    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    unsupported=sorted(set(schema)-SUPPORTED_KEYWORDS)
    if unsupported:
        errors.extend(f"{path}: unsupported schema keyword {key!r}" for key in unsupported)

    if "anyOf" in schema:
        branches=schema.get("anyOf")
        if not isinstance(branches, list) or not branches:
            errors.append(f"{path}: anyOf must contain schemas")
        elif not any(not validate(value, branch, path) for branch in branches):
            errors.append(f"{path}: does not satisfy anyOf")
            return errors

    expected=schema.get("type")
    if expected is not None:
        allowed=expected if isinstance(expected, list) else [expected]
        if not any(_matches_type(value, item) for item in allowed):
            errors.append(f"{path}: expected type {'|'.join(map(str,allowed))}")
            return errors

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in enum")

    if isinstance(value, dict):
        required=schema.get("required",[])
        if isinstance(required, list):
            for key in required:
                if key not in value:
                    errors.append(f"{_path(path,key)}: required property missing")
        properties=schema.get("properties",{})
        if isinstance(properties, dict):
            for key, child_schema in properties.items():
                if key in value:
                    errors.extend(validate(value[key],child_schema,_path(path,key)))
        additional=schema.get("additionalProperties",True)
        known=set(properties) if isinstance(properties,dict) else set()
        for key, child in value.items():
            if key in known:
                continue
            if additional is False:
                errors.append(f"{_path(path,key)}: additional property not allowed")
            elif isinstance(additional,dict):
                errors.extend(validate(child,additional,_path(path,key)))

    if isinstance(value, list):
        if "minItems" in schema and len(value)<schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items")
        if "maxItems" in schema and len(value)>schema["maxItems"]:
            errors.append(f"{path}: expected at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            seen=set()
            for item in value:
                marker=json.dumps(item,sort_keys=True,ensure_ascii=False)
                if marker in seen:
                    errors.append(f"{path}: duplicate array item")
                    break
                seen.add(marker)
        items=schema.get("items")
        if isinstance(items,dict):
            for index,item in enumerate(value):
                errors.extend(validate(item,items,_path(path,index)))

    if isinstance(value,str):
        if "minLength" in schema and len(value)<schema["minLength"]:
            errors.append(f"{path}: string shorter than {schema['minLength']}")
        pattern=schema.get("pattern")
        if pattern is not None:
            try:
                if re.search(pattern,value) is None:
                    errors.append(f"{path}: string does not match {pattern!r}")
            except re.error as exc:
                errors.append(f"{path}: invalid schema pattern: {exc}")

    if isinstance(value,(int,float)) and not isinstance(value,bool):
        if "minimum" in schema and value<schema["minimum"]:
            errors.append(f"{path}: value below minimum {schema['minimum']}")
        if "maximum" in schema and value>schema["maximum"]:
            errors.append(f"{path}: value above maximum {schema['maximum']}")

    return errors

def main():
    ap=argparse.ArgumentParser(description="Validate a JSON document against a star-list JSON contract.")
    ap.add_argument("schema",type=Path)
    ap.add_argument("document",type=Path)
    args=ap.parse_args()
    try:
        schema=json.loads(args.schema.read_text())
        document=json.loads(args.document.read_text())
    except (OSError,json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
    errors=validate(document,schema)
    if errors:
        print("ERRORS:")
        print("\n".join(errors[:100]))
        raise SystemExit(1)
    print(f"OK: {args.document} matches {args.schema}")

if __name__=="__main__":
    main()
