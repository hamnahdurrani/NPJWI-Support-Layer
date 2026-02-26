from pydantic import BaseModel

# Inbound: Public Evaluator -> Support Layer
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: list[ChatMessage]
    model: str | None = None


# Outbound to NPJWI: Support Layer -> NPJWI
class UserInput(BaseModel):
    type: str = "Text"
    text: str

class EvaluationRequest(BaseModel):
    requestType: str = "EvaluationRequest"
    usageKey: str
    userID: str
    accessCode: str
    userInput: UserInput


# Outbound to Public Evaluator: Support Layer -> Public Evaluator
class ResponseMessage(BaseModel):
    role: str = "assistant"
    content: str

class Choice(BaseModel):
    index: int = 0
    message: ResponseMessage

class ChatCompletionResponse(BaseModel):
    choices: list[Choice]