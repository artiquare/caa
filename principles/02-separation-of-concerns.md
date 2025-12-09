# Principle 2 – Separation of Concerns

> **Prompting ≠ Context ≠ Tools ≠ State.** Keep the cognitive parts of the system *decoupled* so each can evolve – and fail – independently.

---

## Why it matters

| Pain when everything lives in one loop                                                                          | Benefit when responsibilities are isolated                                                     |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Prompt templates concatenate live data, tool calls, and control‑flow – break one and the whole agent collapses. | Each concern can be unit‑tested, versioned, and replaced without domino failures.              |
| Debugging is guess‑and‑check; you don’t know whether the *prompt*, the *tool*, or the *memory* mis‑behaved.     | Clear blame: prompt tests fail? Fix prompt. Tool contract violated? Fix tool.                  |
| Teams step on each other – prompt engineers edit the same file execution engineers touch.                       | Independent pipelines: prompt library, tool SDK, context builders evolve on their own cadence. |

---

## Anti‑pattern in many frameworks

* **Monolithic agent loop** – prompt building, tool invocation, and state mutations live in one `while True`.
* **String soup context** – runtime string concat inside Jinja templates.
* **Untyped memory** – random keys dropped into a dict passed around by reference.

Result → *brittle demos* that implode in production.

---

## The CAA / Arti approach

| Concern                 | Lives in                       | Contract                            |
| ----------------------- | ------------------------------ | ----------------------------------- |
| **Prompting**           | `prompts/…` (versioned module) | `render(params) -> str`             |
| **Context**             | Context Layer                  | `RawInput -> ContextObject` (typed) |
| **Planning / Behavior** | Behavior Layer                 | `ContextObject -> ExecutionPlan`    |
| **Execution / Tools**   | Execution Layer                | `Tool(input) -> Output` (typed)     |
| **State**               | State Layer                    | `StateChange -> Snapshot`           |

Each box emits telemetry to the Observability bus, enabling end‑to‑end lineage.

---

## Practical checklist

* [ ] **No string concatenation** inside tool code.
* [ ] **Typed dataclasses / Pydantic** for all cross‑layer messages.
* [ ] **Prompt rendering** happens *once* in the Prompt module, never in Execution.
* [ ] **Tool SDK** has *zero* knowledge of LLMs or prompts.
* [ ] **State mutations** only through explicit StateChange objects.

---

## Pay‑offs

* **Debuggability** – isolate & replay just the misbehaving layer.
* **Reusability** – prompts & tools become libraries, not one‑offs.
* **Parallel work** – front‑end, prompt, and backend teams push in parallel.
* **Compliance & audit** – regulators can inspect each concern separately.

> *“Complexity isn’t the enemy – **entanglement** is. Separate concerns, and the system stays legible.”*
