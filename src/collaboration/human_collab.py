# Using webhooks + queues
from fastapi import FastAPI
from celery import Celery

app = FastAPI()
celery = Celery('tasks', broker='redis://localhost')

class CollaborationLayer:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def request_approval(
        self, 
        plan: Plan, 
        context: Context,
        reason: str
    ) -> ApprovalResult:
        # Send to human
        approval_id = str(uuid.uuid4())
        await self.send_notification({
            "approval_id": approval_id,
            "plan": plan.dict(),
            "context": context.dict(),
            "reason": reason,
            "approve_url": f"{self.webhook_url}/approve/{approval_id}",
            "reject_url": f"{self.webhook_url}/reject/{approval_id}"
        })
        
        # Wait for response (with timeout)
        result = await self.wait_for_approval(approval_id, timeout=3600)
        return result

@app.post("/approve/{approval_id}")
async def approve_step(approval_id: str, modifications: Optional[dict] = None):
    # Resume agent with approval
    celery.send_task('resume_agent', args=[approval_id, True, modifications])
    return {"status": "approved"}