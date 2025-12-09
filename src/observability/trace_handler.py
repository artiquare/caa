# Using Langfuse
from langfuse import Langfuse

langfuse = Langfuse()

class ObservableAgent:
    def run(self, user_input: str):
        trace = langfuse.trace(name="agent_execution")
        
        # Context Layer
        with trace.span(name="context_construction") as span:
            context = self.build_context(user_input)
            span.update(
                input={"raw": user_input},
                output=context.dict(),
                metadata={"version": context.version}
            )
        
        # Behavior Layer
        with trace.span(name="planning") as span:
            plan = self.create_plan(context)
            span.update(
                input=context.dict(),
                output=plan.dict(),
                metadata={"plan_id": plan.id}
            )
        
        # Execution Layer
        for i, step in enumerate(plan.steps):
            with trace.span(name=f"execute_step_{i}") as span:
                result = self.execute_step(step)
                span.update(
                    input=step.dict(),
                    output=result.dict(),
                    metadata={"tool": step.tool}
                )
        
        trace.update(
            output={"status": "complete"},
            metadata={"total_steps": len(plan.steps)}
        )