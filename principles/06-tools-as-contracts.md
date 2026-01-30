# Tools as Contracts

**Principle 6 of the Arti Agent Stack**

---

## Definition

In Compositional Agentic Architecture (CAA), tools are **contracts** – clearly defined interfaces with specific intent, typed inputs/outputs, and predictable behavior.

> Treat tools like APIs, **not** prompts.

---

## Why It Matters

LLM agents often fail because their "tools" are brittle, untyped, or ambiguous. If a tool can accept *anything* and return *anything*, the agent becomes untrustworthy and untestable.

**Contracts bring:**

| Benefit       | Result in production                 |
| ------------- | ------------------------------------ |
| Reliability   | Agents know exactly what to expect   |
| Composability | Tools can be reused across workflows |
| Observability | Calls are auditable & reproducible   |
| Testability   | Unit‑test tools independent of LLM   |

---

## How to Apply It

1. **Typed Interfaces** – Define inputs/outputs with Pydantic, JSON‑Schema, or protobuf.
2. **Declare Intent** – Document purpose, side‑effects, and limits.
3. **Structured Returns** – Never free‑text. Return `{status, result, metadata}`.
4. **Error Contracts** – Invalid inputs → structured errors (`ErrorCode`, `details`).
5. **Traceable Side‑Effects** – External writes must emit events for observability.

```python
class LookupCustomerArgs(BaseModel):
    customer_id: str

class LookupCustomerResult(BaseModel):
    found: bool
    customer: Optional[Customer]

@tool(name="lookup_customer", args_model=LookupCustomerArgs, return_model=LookupCustomerResult)
async def lookup_customer(args: LookupCustomerArgs) -> LookupCustomerResult:
    ...
```

---

## Anti‑Patterns vs Good Practice

| ❌ Anti‑Pattern                       | ✅ Contract‑Driven Tool                     |
| ------------------------------------ | ------------------------------------------ |
| `def tool(data: dict) -> str:`       | `def tool(args: TypedArgs) -> TypedResult` |
| Returns raw string or nothing        | Returns structured object w/ status        |
| Glosses over network/database errors | Raises/returns structured error type       |
| Hidden global state or side‑effects  | Emits trace event with correlation‑id      |

---

## Key Benefits

* **Less hallucination** – Tool behaviour is anchored in ground truth.
* **Versioning** – Interface changes are explicit & backward‑compatible.
* **Modularity** – Swap tool implementations without touching prompts.

> **Plumbing needs specs.**  A tool without a contract is a latent bug.

---

### Checklist

* [ ] Typed input & output models
* [ ] Docstring describing intent & constraints
* [ ] Structured error handling
* [ ] Observability hook emits `ActionTrace`
* [ ] Version tag for backward compatibility

---

Tools are not the magic behind your agent – they’re the plumbing. Design them like you would any critical API.
