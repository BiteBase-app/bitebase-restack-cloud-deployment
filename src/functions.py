from restack_ai.function import function, FunctionFailure, log, function_info, heartbeat

@function.defn()
async def analyze_email(email_content: str) -> str:
    log.debug("Starting email analysis")
    log.info("Processing email", email_length=len(email_content))
    log.warning("Email contains sensitive content", content_type="PII")
    log.error("Failed to parse email", error_code=500)
    log.critical("System failure", component="email_analyzer")
    return "Analyzed email content"

@function.defn()
async def my_custom_function(param: str) -> str:
    log.info("Executing my_custom_function", param=param)
    return f"Processed {param}"

@function.defn()
async def another_custom_function(param: str) -> str:
    log.info("Executing another_custom_function", param=param)
    return f"Processed {param}"

@function.defn()
async def lookup_sales(sales_data: str) -> str:
    log.info("Looking up sales data", sales_data=sales_data)
    return f"Sales data: {sales_data}"

@function.defn()
async def llm_chat(chat_input: str) -> str:
    log.info("Processing chat input", chat_input=chat_input)
    return f"Chat response: {chat_input}"

@function.defn()
async def tool_hn_search(query: str) -> str:
    log.info("Searching Hacker News", query=query)
    return f"Hacker News results for {query}"

@function.defn()
async def openai_todos(user_content: str) -> str:
    log.info("Creating OpenAI todos", user_content=user_content)
    return f"OpenAI todos for {user_content}"
