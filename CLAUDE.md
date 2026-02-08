# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a **LangGraph learning project** used to study and practice the LangGraph framework for building stateful, multi-actor applications with LLMs.

**Current Status**: Phase 1 (Basics) completed with 96.7% test accuracy
**Learning Progress**: See [PROGRESS.md](../PROGRESS.md)

---

## Critical Rules

### When Answering LangGraph Questions

**MANDATORY**: When answering questions about LangGraph, you **MUST** use the `docs-langchain` MCP server to retrieve the latest official documentation. Do not rely on training knowledge alone.

Example usage:
```
Use mcp__docs-langchain__SearchDocsByLangChain to search for LangGraph documentation
```

### Documentation Sources

Always verify LangGraph information from:
1. **LangChain Docs MCP** (Primary) - `mcp__docs-langchain__SearchDocsByLangChain`
2. **Context7** (Secondary) - For general library documentation

---

## Project Structure

```
langgraph-learn/
├── 📄 Core Documentation (3 files only!)
│   ├── README.md              # Project overview and quick start
│   ├── LEARNING_PLAN.md       # Complete learning plan (5 phases)
│   └── PROGRESS.md            # Learning progress tracking
│
├── ⚙️ Configuration Files
│   ├── config.yaml            # LLM configuration (Zhipu GLM)
│   ├── pyproject.toml         # Python project configuration
│   └── .gitignore             # Git ignore rules
│
├── 🚀 Entry Point
│   └── main.py                # Project entry point
│
├── 📁 Working Directories
│   ├── .claude/               # Claude Code configuration (this file)
│   ├── docs/                  # Learning materials (lecture notes)
│   ├── examples/              # Code examples and exercises
│   │   ├── phase01_basics/    # ✅ Phase 1 completed
│   │   │   ├── demos/         # Demo code (6 files)
│   │   │   ├── exercises/     # Practice exercises (3 files)
│   │   │   └── quizzes/       # Quiz files (7 sets)
│   │   ├── phase02_core/      # Phase 2: Core features (pending)
│   │   └── phase03_advanced/  # Phase 3: Advanced patterns (pending)
│   └── scripts/               # Utility scripts
│
└── .venv/                     # Virtual environment (gitignored)
```

---

## Project Organization Standards

### 1. Root Directory Cleanliness

**CRITICAL**: Root directory must remain clean with minimal files.

**Allowed Files**:
- **Maximum 3-4 Markdown documents**: README.md, LEARNING_PLAN.md, PROGRESS.md
- **Configuration files**: config.yaml, pyproject.toml, .gitignore
- **Entry point**: main.py
- **Hidden directories**: .claude/, .git/, .venv/

**Prohibited**:
- ❌ Duplicate documentation (e.g., PROJECT_STRUCTURE.md + PROGRESS.md)
- ❌ Temporary files (e.g., XXX_SUMMARY.md, XXX_REPORT.md)
- ❌ Unused configuration files (e.g., .env.example if not using environment variables)

**Maintenance Checklist**:
- [ ] Root directory has ≤ 4 MD files
- [ ] No duplicate content across documents
- [ ] All unused files deleted
- [ ] Tool-specific files in hidden directories (e.g., CLAUDE.md → .claude/)

---

### 2. Code File Standardization

**File Naming Convention**:
```
Demo files:      01_xxx_demo.py        (sequential numbering)
Exercise files:  01_xxx_exercise.py    (sequential numbering)
Quiz files:      01_xxx_quiz.md        (sequential numbering)
```

**Standard Header Template**:
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[Title]
[Description]

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：演示代码 / 练习代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0

运行方式：
    python [filepath]

学习要点：
    - [Key point 1]
    - [Key point 2]
"""
```

**Code Style Requirements**:
- Use `main()` function for all scripts
- Add `if __name__ == "__main__":` guard
- Remove redundant code (e.g., `pass` after `return`)
- Add UTF-8 encoding support for Windows:
  ```python
  if os.name == 'nt':
      import io
      sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
  ```

---

### 3. Documentation Standards

**Adding New Documents**:
1. Check for duplicate content with existing docs
2. Define clear purpose and target audience
3. Update all cross-references

**Deleting Documents**:
1. Use `grep` to find all references: `grep -r "FILENAME" .`
2. Update or remove all references
3. Verify project still works

**Document Content Guidelines**:
- README.md: Project overview, quick start, structure
- LEARNING_PLAN.md: Complete 5-phase learning roadmap
- PROGRESS.md: Progress tracking, test scores, completion status

---

## Teaching Methods (Important!)

### 教学流程

**Follow "Explain → Practice → Test" Cycle**:

1. **Explain Phase**
   - Teach concepts simply (one at a time)
   - Use conversational guidance, step by step
   - Use examples and analogies
   - One concept per session

2. **Practice Phase**
   - Create fill-in-the-blank exercises
   - Let user write code
   - Check and correct errors
   - Run code to see results

3. **Test Phase**
   - Create quiz questions to verify understanding
   - Save quiz results to `quizzes/` directory
   - Ensure mastery before moving on

### 内容控制原则

**❌ DON'T**:
- Don't teach multiple new concepts at once
- Don't create too many files and confuse the user
- Don't include too many TODOs in exercises

**✅ DO**:
- Teach one core concept at a time
- Give exercises or tests immediately after teaching
- Wait for user mastery before continuing
- Keep conversational, confirm understanding frequently

### 文件组织规范

**按学习阶段和知识点组织代码**：

```
examples/phase01_basics/
├── exercises/            # 练习题（需要用户填空）
├── demos/                # 演示代码（完整代码，学习参考）
└── quizzes/              # 测试题（复习和检查掌握情况）
```

**文件类型说明**：
- `exercises/` - Has TODO fill-in-the-blanks, user completes
- `demos/` - Complete demo code, user runs and learns
- `quizzes/` - Multiple choice questions for checking knowledge

---

## Quiz/Test Format Requirements

### 选择题格式

**CRITICAL**: Answers and explanations must be at the **END** of the document

**Question Format**:
```markdown
### Question 1: What is XXX?

A. Option 1
B. Option 2
C. Option 3
D. Option 4

**Your Answer**: ___

---

(At the end of document)

## 📊 Correct Answers & Explanations

**Question 1: B**
- **Explanation**: XXX
```

**Why This Format?**:
- When editing MD files, folded content expands and shows answers
- When previewing MD files, folded content is also visible
- Answers at the end truly test the user's knowledge

**Quiz Content**:
1. Usage instructions (how to take quiz, how to view answers)
2. Questions section (clean, no answers)
3. Answers & explanations (at the end)
4. Score statistics and grading criteria
5. Wrong answer review guide

---

## Lecture Notes Standards

### 每个阶段结束时必须编写讲义

1. **讲义内容要求**：
   - Clear concept explanations (use analogies)
   - Complete code examples
   - Flowcharts and execution steps
   - Common problems and solutions
   - Practice checklist

2. **讲义组织结构**：
   ```
   docs/
   ├── README.md                    # 总索引
   └── phase01_basics/              # 按阶段组织
       ├── README.md                # 阶段索引
       ├── 01_core_concepts.md      # 按知识点组织
       ├── 02_api_usage.md
       └── ...
   ```

3. **讲义命名规范**：
   - Use numeric prefix: `01_`, `02_`, `03_`
   - Use underscores: `core_concepts.md`
   - Descriptive names: clearly explain content

4. **何时编写讲义**：
   - After completing a topic's teaching
   - After user completes exercises
   - Summarize at phase end

---

## Progress Tracking

**Update progress files promptly**:
- Update PROGRESS.md after each completed task
- Mark which are demos, which are exercises
- Record pending exercises

---

## Windows Compatibility

**All example files must start with**:
```python
import sys
import os
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

## Development Guidelines

- When demonstrating LangGraph concepts, always reference official documentation
- Keep examples simple and focused on specific LangGraph features
- Use **Python** for development
- Use type hints (PEP 484) for better code clarity and IDE support
- Document any custom nodes, edges, or graph patterns with explanations

---

## Current Learning Status

**Phase 1: Basics** ✅ Completed (2025-02-08)
- Test scores: 87/100 (96.7% average)
- Skills mastered: State, Nodes, Edges, Tools, LLM configuration
- Completed: 6 demos, 3 exercises, 7 quiz sets

**Phase 2: Core Features** ⏸️ Pending
- Persistence & Checkpoints
- Streaming
- Human-in-the-loop

**Phase 3: Advanced Patterns** ⏸️ Pending
- RAG Agent
- Multi-agent Systems
- Parallel Execution

---

## Maintenance Checklist

Run this checklist after any major changes:

- [ ] Root directory ≤ 4 MD files
- [ ] No duplicate content across documents
- [ ] All code files have standard headers
- [ ] File numbering is sequential
- [ ] Unused files deleted
- [ ] Document references updated
- [ ] PROGRESS.md reflects current status
- [ ] All Python files have main() functions
- [ ] Windows UTF-8 support added

---

**Last Updated**: 2025-02-08
**Project Phase**: Phase 1 Complete
**Maintenance Standard**: Clean root directory, standardized code files
