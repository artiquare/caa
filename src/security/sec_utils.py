# Using standard auth + PII detection
from typing import Any
import re

class SecurityLayer:
    def __init__(self, auth_provider, pii_detector):
        self.auth = auth_provider
        self.pii = pii_detector
    
    def sanitize_context(self, context: Context) -> Context:
        # Remove PII before model sees it
        sanitized = context.copy()
        sanitized.query = self.pii.redact(context.query)
        sanitized.metadata = self.pii.redact_dict(context.metadata)
        return sanitized
    
    def authorize_tool(self, tool: str, user: User) -> bool:
        # Check if user can execute this tool
        return self.auth.has_permission(user, f"tool.{tool}.execute")
    
    def log_action(self, user: User, tool: str, params: dict, result: Any):
        # Audit trail
        audit_log.write({
            "user": user.id,
            "tool": tool,
            "timestamp": datetime.now(),
            "params": self.sanitize_for_audit(params),
            "success": result.success
        })