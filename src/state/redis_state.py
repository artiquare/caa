# Using Redis for state
import redis
from pydantic import BaseModel

class AgentState(BaseModel):
    agent_id: str
    conversation_id: str
    current_step: int
    plan: Plan
    executed_steps: List[ExecutionResult]
    context_snapshot: Context
    
    class Config:
        # Pydantic v2
        json_schema_extra = {"version": "1.0.0"}

class StateManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def save_checkpoint(self, state: AgentState):
        key = f"agent:{state.agent_id}:state"
        self.redis.set(key, state.json())
        self.redis.expire(key, 86400)  # 24h TTL
    
    def load_checkpoint(self, agent_id: str) -> AgentState:
        key = f"agent:{agent_id}:state"
        data = self.redis.get(key)
        return AgentState.parse_raw(data)
    
    def resume_from_step(self, agent_id: str, step: int):
        state = self.load_checkpoint(agent_id)
        state.current_step = step
        return state