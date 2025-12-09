from openai import OpenAI
from src.context.schema import UserContext

class StepSchema:
    @staticmethod
    def model_json_schema(): return {}

class Plan:
    @staticmethod
    def from_response(res): return res

PLANNING_PROMPT = "You are a deterministic planner..."

client = OpenAI()

def create_plan(context: UserContext) -> Plan:
    """
    Layer 2: Behavior
    Generates an inspectable plan without executing it.
    """
    
    context_str = context.model_dump_json()

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": PLANNING_PROMPT},
            {"role": "user", "content": context_str}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "create_step",
                    "description": "Add a step to execution plan",
                    "parameters": StepSchema.model_json_schema()
                }
            }
        ],
        tool_choice="auto" 
    )
    
    # Plan is now inspectable, not hidden in tool calls
    return Plan.from_response(response)