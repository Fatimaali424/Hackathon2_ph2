---
description: "Task list for Todo Console Application implementation"
---

# Tasks: Todo Console Application

**Input**: Design documents from `/specs/002-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test requirements in feature specification, so test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with src/ and specs_history/ directories
- [x] T002 [P] Create src/main.py file for main application entry point
- [x] T003 [P] Create src/task_manager.py file for core task management functions
- [x] T004 [P] Create src/models.py file for task data model and storage

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement Task data model in src/models.py with id, title, description, completed fields
- [x] T006 [P] Implement in-memory storage using list of dictionaries in src/models.py
- [x] T007 [P] Implement ID generation strategy with auto-incrementing counter in src/models.py
- [x] T008 Create basic menu display function in src/main.py
- [x] T009 Implement input validation functions in src/task_manager.py for handling invalid inputs

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their todo list with title, description, and auto-generated ID

**Independent Test**: User can run the application and successfully add a new task with a title and optional description, receiving confirmation that the task was created

### Implementation for User Story 1

- [x] T010 [P] [US1] Implement add_task function in src/task_manager.py with title validation
- [x] T011 [P] [US1] Add task creation logic with auto-generated ID in src/task_manager.py
- [x] T012 [US1] Implement user input handling for adding tasks in src/main.py
- [x] T013 [US1] Add success confirmation message when task is created in src/main.py
- [x] T014 [US1] Implement error handling for empty titles in src/task_manager.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to view all their tasks with ID, title, description, and completion status

**Independent Test**: User can run the application and view a list of all tasks with their details

### Implementation for User Story 2

- [x] T015 [P] [US2] Implement get_all_tasks function in src/task_manager.py
- [x] T016 [US2] Implement task display formatting in src/main.py
- [x] T017 [US2] Add user input handling for viewing tasks in src/main.py
- [x] T018 [US2] Implement "no tasks" message when list is empty in src/main.py
- [x] T019 [US2] Format task display with ID, title, description, and status in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1)

**Goal**: Enable users to toggle task completion status by ID

**Independent Test**: User can select a task by ID and toggle its completion status, with confirmation of the status change

### Implementation for User Story 5

- [x] T020 [P] [US5] Implement toggle_task_completion function in src/task_manager.py
- [x] T021 [US5] Add validation for task existence before toggling in src/task_manager.py
- [x] T022 [US5] Implement user input handling for toggling tasks in src/main.py
- [x] T023 [US5] Add success confirmation for status change in src/main.py
- [x] T024 [US5] Implement error handling for invalid task IDs in src/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2, and 5 should all work independently

---

## Phase 6: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to update existing tasks by ID with new title or description

**Independent Test**: User can select a task by ID and update its title or description, with confirmation of the changes

### Implementation for User Story 3

- [x] T025 [P] [US3] Implement update_task function in src/task_manager.py
- [x] T026 [US3] Add validation for task existence before updating in src/task_manager.py
- [x] T027 [US3] Implement user input handling for updating tasks in src/main.py
- [x] T028 [US3] Add success confirmation for updates in src/main.py
- [x] T029 [US3] Implement error handling for invalid task IDs in src/task_manager.py

**Checkpoint**: At this point, User Stories 1, 2, 5, and 3 should all work independently

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable users to delete tasks by ID

**Independent Test**: User can select a task by ID and delete it, with confirmation that the task was removed

### Implementation for User Story 4

- [x] T030 [P] [US4] Implement delete_task function in src/task_manager.py
- [x] T031 [US4] Add validation for task existence before deletion in src/task_manager.py
- [x] T032 [US4] Implement user input handling for deleting tasks in src/main.py
- [x] T033 [US4] Add success confirmation for deletion in src/main.py
- [x] T034 [US4] Implement error handling for invalid task IDs in src/task_manager.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T035 [P] Add comprehensive error handling throughout all functions in src/task_manager.py
- [x] T036 [P] Implement graceful menu navigation in src/main.py
- [x] T037 Add proper exit handling in src/main.py
- [x] T038 [P] Add input sanitization for all user inputs in src/main.py
- [x] T039 Improve console output formatting in src/main.py
- [x] T040 Run manual tests per quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Implement add_task function in src/task_manager.py with title validation"
Task: "Add task creation logic with auto-generated ID in src/task_manager.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 5 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. Complete Phase 5: User Story 5
6. **STOP and VALIDATE**: Test core functionality independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 4 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 5
   - Developer D: User Story 3
   - Developer E: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence