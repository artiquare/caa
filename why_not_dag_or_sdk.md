# Why Not DAGs or SDKs?

Modern agentic systems demand both **flexibility** and **control**. In our experience building cognitive automation across complex real-world environments, we found that both DAG-based architectures and SDK-first agent frameworks consistently fall short.

This is why we moved away from them entirely.

---

## ❌ DAGs: Overengineered and Inflexible

Directed Acyclic Graphs (DAGs) were a tempting early abstraction. But in practice, they became a **rigid, brittle representation of business logic**:

* **Hard to refactor** – Every change to flow logic means editing node connections and dependencies.
* **Poor readability** – Visual graphs look nice in theory, but quickly become unreadable in real workflows.
* **Bakes logic into structure** – Instead of separating behavior from architecture, DAGs entangle them.
* **No state discipline** – The infamous "state dict" or fragile JSON blob becomes the only way to pass context.

In the end, DAGs turn dynamic processes into static flowcharts — the exact opposite of what agentic systems should be.

---

## ❌ SDKs: Oversimplified and Opaque

On the flip side, SDK-based frameworks (especially those pushed by LLM vendors) try to abstract away the complexity — but swing too far in the other direction:

* **Too much magic** – Routing, tool usage, retries, context — all hidden behind black-box decorators or prompt wrappers.
* **LLM-centric logic** – Delegates core execution to stochastic models with no control flow guarantees.
* **Difficult to audit** – Hard to debug, test, or trace failures in production.
* **Not composable** – You can't easily extract or reuse components. You have to adopt their full stack or nothing.

These SDKs may make for great demos. But when complexity scales — they crack.

---

## ✅ What We Do Instead

CAA (Compositional Agentic Architecture) is our answer:

* **Explicit control flow** (not inferred by the model)
* **Layered separation** between context, memory, execution, and tools
* **Observable systems** with typed state and versioned prompts
* **Composable agents** with clear responsibilities

We don’t just build agents. We build **software systems that behave like agents**.

---

## 📚 Related Reading

* [Everyone’s Building AI Agent Frameworks – Most Are Getting It Wrong](https://www.artiquare.com/ai-agent-frameworks-critical-analysis/)
* [Beyond Frameworks: Building Production-Grade Agent Systems](https://www.artiquare.com/production-grade-agent-systems-arti/)

---

> Agentic AI isn’t about graphs or SDKs. It’s about **designing for complexity** — and doing it with the discipline of software engineering.
