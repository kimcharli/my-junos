# Decision: Context Budget & Where Repository Knowledge Lives — 2026-08-18

- **Status**: Decided and executed on 2026-08-18.
- **Read this when**: restructuring `AGENTS.md`, adding a new rules/docs file, wondering why the
  authoring contract is split across three places, or considering "why not just put it all in
  `AGENTS.md`".
- **Do not** link this from `AGENTS.md` in a way that implies it must be read to author a
  document. It is reference material for repository-structure decisions only.

---

## Problem

Every authoring session opened with the same throwaway discovery: `ls -la`, `find knowledge`,
`grep "^id:"`, `cat schemas/*`. That cost tokens and turns, and it was still incomplete — the
validator enforces markdown-body rules that appear in neither the schema nor the skills, so a
session could do all that discovery and *still* fail validation on the first commit attempt.

The obvious fix was "write it all down in `AGENTS.md`". That fix has a hidden cost, which is
the subject of this decision.

## Key finding: not all documentation costs the same

Zed injects `AGENTS.md` into the model's system prompt **on every session, before the user
types anything**, whether or not the session touches `knowledge/`. Skill bodies are *lazy*:
only the short `description` is always resident; the body loads when the skill is invoked.
Files like `MANIFEST.md` cost nothing until read. Script *execution* costs nothing at all —
only whatever the script prints into the transcript.

Measured at the time of the decision (~4 chars/token):

| Artifact | Size | Billing model | Per-session cost |
| --- | --- | --- | --- |
| `AGENTS.md` | 7.2 KB | auto-injected, every session | ~1,800 tok, unconditional |
| `MANIFEST.md` | 3.7 KB | read on demand | ~925 tok, only when read |
| `junos-okf` SKILL.md | 4.8 KB | lazy; description always resident | ~30 tok until invoked |
| `knowledge-builder` SKILL.md | 3.9 KB | lazy | ~30 tok until invoked |
| `okf_manifest.py --check` | — | only its stdout | ~15 tok |

At 7.2 KB, `AGENTS.md` had become the largest fixed cost in the repository — and it duplicated
the frontmatter contract already present in the `junos-okf` skill. The duplicated copy was
billed every session; the skill copy was free until needed.

## Rulings

1. **Tier documentation by billing model, not by topic.**
   * *Always-injected* (`AGENTS.md`): only what a session needs to avoid a wrong first move —
     repo map, where to claim IDs, the workflow, and the gotchas that cause a failed round
     trip. Target ~2 KB. Every line here is a recurring tax.
   * *Lazy* (skills, `MANIFEST.md`, this file): everything detailed. Costs nothing until
     relevant.
   * *Free* (scripts): anything that can be executed rather than read.

2. **Prefer executable rules over written rules.** A constraint encoded in a tool costs zero
   context, because the agent never needs to know it — it runs the tool and the tool either
   does the right thing or emits a targeted error. This is strictly better than prose, which
   goes stale silently. Precedent: both authoring skills drifted to instructing `timestamp:`,
   a field that is not in the schema, while `generated` *is* required — following either skill
   verbatim produced a document that failed validation. Generated skeletons cannot drift that
   way.

3. **`tools/okf_new.py` scaffolds new documents.** It allocates the next free ID, stamps every
   required frontmatter field, and includes the per-type body stub the validator demands. This
   removes the frontmatter contract from the context budget entirely.

4. **Validator error messages are the enforcement surface.** Rules the validator already
   reports precisely do not need to be restated in always-injected prose.

5. **This decision document lives in `specs/`, not `knowledge/`.** It is repository process,
   not JUNOS domain knowledge; putting it under `knowledge/` would require an OKF frontmatter
   block and a `KP-META-*` ID, and would pollute the manifest inventory with meta-process
   material.

## Outcome

Fixed per-session cost reduced from ~1,800 to roughly ~500 tokens, with correctness improved
rather than traded away: the contract moved from prose that can rot into a generator and a
validator that cannot.

## Rejected alternatives

* **Put everything in `AGENTS.md`.** Rejected: unconditional cost on every session, including
  the many that never author a document.
* **An init script that "runs at session start for free".** Rejected as unavailable: Zed has no
  session-start script hook, and more fundamentally, a script's output only helps the agent by
  entering the context, at which point it is billed like anything else. The workable form of
  this idea is a script that *performs the work* (scaffolding, validation) rather than one that
  *explains how to do the work*.
* **Delete `AGENTS.md` and rely solely on skills.** Rejected: skills load on invocation, so a
  session can begin authoring without ever triggering one. A small always-resident file is what
  guarantees the first move is correct.
