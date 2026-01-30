# Principle 8 – State is Explicit

> **No dicts or fragile memory blobs. Use structured, persistent state.**

In too many agent implementations, state is an after‑thought. It lives in loose `dict` objects, fragile context strings, or memory hacks bolted onto looped prompts. That may work for demos—but not for production.

In **Compositional Agentic Architecture**, **state is a first‑class citizen**.

---

## Why Explicit State Matters

| Pain when state is implicit                          | Benefit of explicit state                       |
| ---------------------------------------------------- | ----------------------------------------------- |
|  Debugging guesses & print‑statement archaeology     |  Deterministic snapshots & diffable transitions |
|  Resume / retry is flaky; conversations “forget”     |  Checkpoint → rewind → replay with confidence   |
|  Concurrency chaos (two agents mutate the same blob) |  Typed contracts & versioned persistence        |
|  Auditors can’t see what the agent “knew”            |  State records are inspectable & tamper‑evident |

---

## What Explicit State Looks Like

* **Typed models** – Pydantic / dataclass schemas, not free‑form dicts
* **Versioned storage** – JSON snapshots or DB tables with schema evolution
* **Clear separation**

  * **Agent state** – plan, progress, scratch‑pads
  * **Environment state** – external facts (CRM, ERP, sensor readings)
  * **Execution state** – current step, retries, errors
* **Delta tracking** – state changes are events, not silent in‑place mutation

```python
class AgentState(BaseModel):
    plan_id: UUID
    current_step: int
    retries: int = 0
    scratch: dict[str, Any] = {}
```

---

## Design Guidelines

1. **Never** pass anonymous dicts between layers—always typed objects.
2. **Checkpoint** before risky actions; store diff after each step.
3. Expose a **State API** so UI, eval, and observability layers can read it.
4. Use **optimistic locking / etags** for concurrent agent writes.
5. Log every mutation via the Observability bus.

---

## Anti‑Patterns

* `memory["last_tool"] = result` – hidden mutation inside prompts.
* Storing state only in the chat transcript—impossible to query.
* Overloading Redis key‑value blobs with ad‑hoc JSON.

---

## Principles Embodied

* **State is Explicit** – it’s data, not side‑effect.
* **Observable Everything** – state traces flow to the telemetry bus.
* **Composable Error Handling** – retries & rollbacks need reliable state.

---

> *“If you can’t see it, test it, or restore it, it’s not real state.”*
