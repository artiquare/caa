# Using Pydantic (Python)
from pydantic import BaseModel, Field, field_validator

class UserContext(BaseModel):
    user_id: str
    industry: str = Field(..., description="NAICS code")
    query: str
    metadata: dict = {}
    # Explicit versioning is a great CAA touch
    schema_version: str = "1.2.0" 
    
    @field_validator('industry')
    @classmethod
    def validate_industry(cls, v: str) -> str:
        if not v.startswith('NAICS'):
            raise ValueError('Industry must be a valid NAICS code')
        return v

# Using TypeScript
interface UserContext {
  userId: str;
  industry: str; # NAICS code
  query: str;
  metadata: Record<str, any>;
  version: "1.2.0";
}