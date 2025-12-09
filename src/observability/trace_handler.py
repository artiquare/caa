from langfuse import Langfuse

# Initialize Langfuse (assuming env vars are set)
langfuse = Langfuse()

class ObservableAgent:
    """
    Mixin/Wrapper to add observability to an existing agent class.
    """
    def run_observable(self, user_input: str):
        trace = langfuse.trace(name="agent_execution")
        
        # Context Layer
        with trace.span(name="context_construction") as span:
            context = self.build_context(user_input)
            span.update(
                input={"raw": user_input},
                output=context.model_dump(),
                metadata={"version": getattr(context, "schema_version", "1.0")}
            )
        
        # Behavior Layer
        with trace.span(name="planning") as span:
            plan = self.create_plan(context)
            span.update(
                input=context.model_dump(),
                output=plan.model_dump(),
                metadata={"plan_id": getattr(plan, "id", "unknown")}
            )
        
        # Execution Layer
        for i, step in enumerate(plan.steps):
            with trace.span(name=f"execute_step_{i}") as span:
                result = self.execute_step(step)
                span.update(
                    input=step.model_dump(),
                    output=result.model_dump(),
                    metadata={"tool": step.tool}
                )
        
        trace.update(
            output={"status": "complete"},
            metadata={"total_steps": len(plan.steps)}
        )