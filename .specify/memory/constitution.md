<!-- Sync Impact Report:
Version change: N/A -> 1.0.0
Added sections: All principles and sections based on user input
Removed sections: Template placeholders
Modified principles: N/A (new constitution)
Templates requiring updates: N/A (new constitution created)
Follow-up TODOs: None
-->
# Todo In-Memory Python Console App Constitution

## Core Principles

### Simplicity
Console app must be intuitive and easy to use

### Clean code
Readable, maintainable, well-structured Python code

### Modularity
Separate functions for each feature (add, view, update, delete, mark complete)

### In-memory data handling
No external database; all tasks stored in runtime memory

### Reliability
Accurate task operations without data corruption

### Python Standards
Python version 3.13+ with list of dictionaries for task storage

## Key Standards

- Python version: 3.13+
- Data structure: List of dictionaries for storing tasks
- Task model: Each task must have unique ID, title, description, completion status
- Console interface: Clear prompts and output formatting
- Code organization:
  - src/ for Python source files
  - specs_history/ for all specification files
  - README.md for setup and usage instructions
  - CLAUDE.md for Claude Code instructions
- Testing: Each feature must be tested interactively in the console

## Development Constraints

- No manual coding: All implementations must be generated

## Governance

- All implementations must follow the defined principles
- Code reviews must verify compliance with all principles
- Changes to constitution require explicit approval
- Versioning follows semantic versioning (MAJOR.MINOR.PATCH)
- All team members must acknowledge and agree to these principles

**Version**: 1.0.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-03
