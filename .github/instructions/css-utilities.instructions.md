---
description: CSS utility classes and styling practices for this Python/Jinja2 project.
---

# CSS Utility Rules

## Core Usage
- Use utility classes from app/static/css/app.css.
- Compose classes in markup for layout, spacing, color, and typography.
- Prefer existing classes before creating new ones.

## Strict Constraints
- Do not use inline styles.
- Do not add one-off CSS in templates.
- Do not create duplicate utilities with different names.
- Keep utilities single-purpose and low-specificity.

## Reuse First
- Reuse established class groups (layout, spacing, sizing, color, type, border, shadow, animation).
- If a needed utility does not exist, add it once to app/static/css/app.css and reuse it.
- Keep naming consistent with existing patterns.

## AI Generation Behavior
- Generate class-based markup, not style attributes.
- Keep changes minimal and scoped to requested files.
- Match current utility naming and composition patterns.
- Favor predictable, maintainable class combinations over custom CSS blocks.