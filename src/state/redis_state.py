import redis
from typing import List
from pydantic import BaseModel
# Assuming these exist in your other modules
from some.model import Plan, ExecutionResult, Context 

class AgentState(BaseModel):
    agent_id: str
    conversation_id: str
    current_step: int
    plan: Plan
    executed_steps: List[ExecutionResult]
    context_snapshot: Context
    
    model_config = {
        "json_schema_extra": {"version": "1.0.0"}
    }

class StateManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def save_checkpoint(self, state: AgentState):
        key = f"agent:{state.agent_id}:state"
        self.redis.set(key, state.model_dump_json())
        self.redis.expire(key, 86400)  # 24h TTL
    
    def load_checkpoint(self, agent_id: str) -> AgentState:
        key = f"agent:{agent_id}:state"
        data = self.redis.get(key)
        if not data:
            return None
        return AgentState.model_validate_json(data)
    
    def resume_from_step(self, agent_id: str, step: int):
        state = self.load_checkpoint(agent_id)
        if state:
            state.current_step = step
        return state