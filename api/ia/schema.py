from pydantic import BaseModel, Field

class MetadataSchema(BaseModel):
    """Schema representing metadata related to language model processing."""
    
    output_tokens: int = Field(description="The number of tokens generated as output by the language model.")
    input_tokens: int = Field(description="The number of tokens received as input by the language model.")
    llm_model: str = Field(description="The name of the language model used.")

class AnalyseSchema(BaseModel):
    """Schema representing the analysis of a chatbot conversation, including satisfaction, summary, and improvement points."""
    
    satisfaction: int = Field(description="The satisfaction level of the conversation, rated from 0 to 10.")
    summary: list[str] = Field(description="The key points of the conversation.")
    improvement: list[str] = Field(description="The main areas for improvement in the chatbot's behavior.")
    metadata: MetadataSchema = Field(description="Metadata containing token usage and model information.")

class CreateAnalysisSchema(BaseModel):
    """Schema representing the creation of a analysis of a chatbot conversation"""
    session_id: int = Field(description="The session identifier related to the analysis")
    summary: str
    improvement: str
    satisfaction: int
    input_tokens: int
    output_tokens: int
    llm_model: str
    
    @classmethod
    def from_analyse(cls, session_id: int, analyse: AnalyseSchema):
        """Converts AnalyseSchema to CreateAnalysisSchema"""
        return cls(
            session_id=session_id,
            satisfaction=analyse.satisfaction,
            summary='\n'.join(analyse.summary),
            improvement='\n'.join(analyse.improvement),
            output_tokens=analyse.metadata.output_tokens,
            input_tokens=analyse.metadata.input_tokens,
            llm_model=analyse.metadata.llm_model,
        )