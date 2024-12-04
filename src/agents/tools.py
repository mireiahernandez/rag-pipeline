from mistralai.models import Tool, Function
from typing import List


def get_knowledge_base_tool() -> Tool:
    """
    Creates a Tool instance for querying the knowledge base.

    Returns:
        Tool: A properly formatted Mistral Tool instance
    """
    return Tool(
        type="function",
        function=Function(
            name="query_knowledge_base",
            description="Retrieves relevant documents from the knowledge base",
            parameters={
                "type": "object",
                "properties": {
                    "rewritten_query": {
                        "type": "string",
                        "description": (
                            "The rewritten query to search for. "
                            "Ensure this query is optimized for search and "
                            "more effective than the original query."
                            "Include synonyms and alternative phrasing if "
                            "necessary."
                        )
                    }
                },
                "required": ["rewritten_query"]
            }
        )
    )


def get_default_tools() -> List[Tool]:
    """
    Returns a list of all available default tools.

    Returns:
        List[Tool]: List of all available tools
    """
    return [
        get_knowledge_base_tool()
    ]
