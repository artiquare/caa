# Using Pydantic (Python) V2
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any

class UserContext(BaseModel):
    user_id: str
    industry: str = Field(..., description="NAICS code")
    query: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Explicit versioning is a great CAA touch
    schema_version: str = "1.2.0" 
    
    @field_validator('industry')
    @classmethod
    def validate_industry(cls, v: str) -> str:
        if not v.startswith('NAICS'):
            raise ValueError('Industry must be a valid NAICS code')
        return v
