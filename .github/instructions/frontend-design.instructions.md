---
name: frontend-design
description: Use this skill when the user asks to design/build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Frontend Design Rules

## Design Principles
- Design with clear intent: one strong visual direction per screen.
- Prioritize hierarchy: title, primary action, supporting content.
- Make layouts responsive by default for mobile and desktop.
- Match motion to meaning: use a few purposeful animations, not many small effects.

## Hard Constraints
- No generic AI look: avoid cookie-cutter hero + cards + CTA patterns.
- No purple gradients.
- Avoid overused defaults: Inter, Roboto, Arial, and system-only font stacks.
- Avoid low-contrast text and tiny tap targets.
- Do not rely on flat single-color backgrounds when a richer visual layer is appropriate.

## Style Direction
- Use distinctive typography and consistent spacing rhythm.
- Use CSS variables for theme colors and tokens.
- Prefer bold accents with controlled neutral surfaces.
- Use background depth (subtle gradients, patterns, or shapes) that fits the concept.

## Code Generation Guidance
- Produce complete, runnable code for the requested files.
- Keep changes scoped to requested files and existing project patterns.
- For Jinja2 projects, prefer CSS-first solutions and minimal JS.
- If adding styles, keep naming and structure consistent with the codebase.

