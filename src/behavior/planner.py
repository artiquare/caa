# Using OpenAI function calling for planning
from openai import OpenAI

client = OpenAI()

# CAA: Planning is separate from execution
def create_plan(context: UserContext) -> Plan:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": PLANNING_PROMPT},
            {"role": "user", "content": context.to_prompt()}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "create_step",
                    "description": "Add a step to execution plan",
                    "parameters": StepSchema.to_json_schema()
                }
            }
        ]
    )
    
    # Plan is now inspectable, not hidden in tool calls
    return Plan.from_response(response)