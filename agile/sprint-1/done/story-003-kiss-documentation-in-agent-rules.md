# [STORY-003] KISS documentation in agent rules

## Summary

Update project and agent guidance (`.cursorrules`, `AGENTS.md`, `.cursor/rules/project.mdc`) so that "follow KISS" is explicitly stated for future iterations: simplest implementation that meets requirements, avoid unnecessary abstraction and extra complexity.

## Description

The PoC and project principles require KISS. To keep future work aligned, agent and Cursor guidance must state this explicitly so that any new story or feature is implemented with minimal abstraction and minimal moving parts. This story is the concrete "document KISS" task from the plan.

**Scope:**
- In `.cursorrules`: add or strengthen one line that states KISS (e.g. "Follow KISS: prefer the simplest implementation that meets the requirements; avoid unnecessary abstraction and extra complexity.").
- In `AGENTS.md`: in the Persona or Code style (or both), add an explicit KISS sentence so AI assistants read it.
- In `.cursor/rules/project.mdc`: in "What this project is" or "Code style" or "Boundaries", add the same KISS statement so Cursor rules always apply it.
- Do not add long new sections; integrate into existing structure. No new files unless the project has no `.cursor/rules` file.

**ESP32 Marauder:** N/A — documentation only.

## Acceptance criteria

- [x] `.cursorrules` contains an explicit KISS statement (short, actionable).
- [x] `AGENTS.md` contains an explicit KISS statement in a section that agents are instructed to follow.
- [x] `.cursor/rules/project.mdc` (or the single project rule file in use) contains the same or equivalent KISS statement.
- [x] Wording is consistent: "simplest implementation that meets requirements", "avoid unnecessary abstraction", "avoid extra complexity" (or equivalent).

## Definition of done

- Edits merged. All three (or two, if one file is missing) locations updated. No other content removed or altered beyond adding/clarifying KISS.

## Subtasks / notes

- Keep the phrase reusable: e.g. "Follow KISS: prefer the simplest implementation that meets the requirements; avoid unnecessary abstraction and extra complexity."
