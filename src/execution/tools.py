from typing import Protocol, Any

class ToolProtocol(Protocol):
    name: str
    def execute(self, params: dict) -> Any: ...

# CAA: Wrap tools with contracts
class CAAToolExecutor:
    def __init__(self, mcp_tool: Tool):
        self.tool = mcp_tool
        self.contract = ToolContract.from_mcp(mcp_tool)
    
    async def execute(self, params: dict, context: Context) -> ExecutionResult:
        # 1. Validate against contract
        validated_params = self.contract.validate(params)
        
        # 2. Execute with timeout
        try:
            result = await asyncio.wait_for(
                self.tool.call(validated_params),
                timeout=self.contract.timeout
            )
        except TimeoutError:
            return ExecutionResult.failure("timeout")
        except Exception as e:
            return ExecutionResult.failure(str(e))
        
        # 3. Validate output
        validated_result = self.contract.validate_output(result)
        
        # 4. Return structured result
        return ExecutionResult(
            tool=self.tool.name,
            input=params,
            output=validated_result,
            context_id=context.id,
            timestamp=datetime.now()
        )