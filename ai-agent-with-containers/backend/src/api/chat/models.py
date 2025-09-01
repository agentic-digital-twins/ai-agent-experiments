from sqlmodel import SQLModel, Field

class ChatMessagePayload(SQLModel):
    # validation model for incoming chat message payloads
    message: str = Field(..., description="The content of the chat message")
    # role: str = Field(..., description="The role of the message sender, e.g., 'user' or 'assistant'")
    # conversation_id: int = Field(..., description="The ID of the conversation this message belongs to")
    # agent_id: int = Field(..., description="The ID of the agent handling this message")
    # response_to_id: int | None = Field(default=None, description="The ID of the message this is a response to, if applicable")
    # metadata: str | None = Field(default=None, description="Additional metadata for the message, stored as a JSON string")

class ChatMessage(SQLModel, table=True):
    # database table, model for chat messages
    message: str = Field(..., description="The content of the chat message")
    id: int | None = Field(default=None, primary_key=True)  
    # role: str = Field(..., description="The role of the message sender, e.g., 'user' or 'assistant'")
    # timestamp: str = Field(..., description="The timestamp when the message was created")
    # conversation_id: int = Field(..., description="The ID of the conversation this message belongs to")
    # agent_id: int = Field(..., description="The ID of the agent handling this message")
    # response_to_id: int | None = Field(default=None, description="The ID of the message this is a response to, if applicable")
    # metadata: str | None = Field(default=None, description="Additional metadata for the message, stored as a JSON string")

