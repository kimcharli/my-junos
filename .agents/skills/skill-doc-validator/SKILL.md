---
name: skill-doc-validator
description: Validates that all local Zed Agent skill documents conform to naming conventions, directory matches, and frontmatter constraints.
---

# Skill Document Validation

Use this skill to inspect, validate, and verify that any local skill documents inside `.agents/skills/` are fully compliant with Zed's skill specifications.

---

## 1. Skill Folder & Structure Constraints

Every local skill must comply with the following structural conventions:
1. **Directory Path:** Must be located at `.agents/skills/<skill-name>/`.
2. **Main File:** Must contain a file named exactly `SKILL.md`.
3. **Directory Match:** The directory name `<skill-name>` must match the `name` field in the frontmatter exactly.

---

## 2. Naming & Frontmatter Constraints

The YAML frontmatter of `SKILL.md` must contain:
* **`name`** (Required): 1–64 characters, lowercase alphanumeric with single-hyphen separators. Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
* **`description`** (Required): 1–1024 characters. Actionable and specific.

### Schema Blueprint
```markdown
---
name: my-skill-name
description: Specific, actionable description of when to use this skill.
---
# Skill Title
... Instructions ...
```

---

## 3. Verification Steps

To validate all skills in the repository:
1. Scan `.agents/skills/` recursively for any subdirectories.
2. Ensure each subdirectory has a `SKILL.md` file.
3. Verify that the folder name matches the frontmatter `name` key exactly.
4. Check that the `description` exists and is within character boundaries.
5. Confirm there are no trailing or starting hyphens, and no duplicate hyphens in the `name`.
