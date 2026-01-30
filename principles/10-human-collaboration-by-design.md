# Human Collaboration by Design

**Principle 10 of the Arti Agent Stack — Compositional Agentic Architecture**

Agentic systems are not meant to replace humans — they are built to **collaborate** with them. Real‑world environments are noisy, unpredictable, and full of edge cases. Seamless human‑AI interaction is therefore *essential, not optional*.

---

## Key Tenets

### 🔄 Interruptible
Agents must allow for manual **pause, intervention, or override** at any point in execution. If a human needs to step in, the system should support this with minimal disruption.

* Interrupts are not exceptions — they’re expected.
* Design execution checkpoints that allow for safe pausing.

### ▶️ Resumable
After human review or modification, agents should be able to **resume** from a known, valid state. This requires persistent state management and version‑controlled context.

* No fragile stack traces or ephemeral session state.
* Resume from checkpoints or restore context from logs.

### 🧾 Auditable
Every decision, input, output, and action must be **traceable** for trust, validation, compliance, and debugging.

* Logs should show what the agent saw, what it chose to do, and *why*.
* Human decisions and overrides become part of the execution trace.

---

## Why It Matters
In operations, human expertise doesn’t disappear — it moves **up the stack**. Agents must support escalation, approval, and review flows. Systems that assume full autonomy will fail when trust is needed most.

Design for collaboration:

* Supervisor mode & escalation paths
* Editor/reviewer workflows
* Comprehensive audit trails

---

## Implementation Checklist

* [ ] Define interrupt points & UI hooks.
* [ ] Persist state before any human‑blocking checkpoint.
* [ ] Log human actions with correlation‑ids.
* [ ] Provide “resume” and “rollback” APIs.
* [ ] Measure *time‑to‑approval* and *override frequency*.

---

> **“The best agents don’t replace humans. They work *with* them.”**
