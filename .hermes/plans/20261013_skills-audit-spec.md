# Hermes Skills Audit and Remediation Specification

Status: active
Owner: default profile
Scope root: /home/alexa/.hermes/skills

## Objective

Audit every discovered `SKILL.md` under the active Hermes skill root, run the skill-judge rubric for every file, publish a machine-readable and human-readable audit report, apply only evidence-backed quality enhancements, validate every changed skill, and re-judge every skill after remediation.

## Required invariants

1. Composer Modes must remain registered as:
   `[composer-modes] register ver=v2.0.1 default=agent modes=ask,agent,plan,debug enforce=True`
2. Every discovered skill receives a `/skill-judge`-equivalent score using the installed `skill-judge` rubric.
3. The audit includes all `SKILL.md` paths, while duplicate names, backups, generated copies, protected/bundled skills, and hub-installed skills are classified rather than silently removed.
4. No Hermes source update, dependency update, external publication, destructive deletion, or production action is performed.
5. All edits are limited to auditable skill content/reference files and generated reports; rollback is through git or the recorded patch manifest.
6. Every changed skill is validated from disk and re-judged; no score is claimed from stale `skill_view` cache.

## Acceptance criteria

- Baseline inventory and duplicate/protection classification saved.
- Audit report covers every discovered skill with path, name, score, dimensions, rating, and findings.
- Remediation manifest records each changed and skipped skill with reason.
- Changed skills pass structural validation and have a post-remediation score.
- Final aggregate report reconciles counts programmatically.
- Composer registration invariant is verified from live Hermes evidence.
- Repository green command is run after file changes: `bun run check` and `npm run check` when available.

## Non-goals

- Updating Hermes or installed hub sources.
- Deleting duplicate or placeholder skills without a separate explicit approval.
- Inventing content, APIs, commands, or references to inflate scores.
- Treating a heuristic score as proof that a workflow actually works.
