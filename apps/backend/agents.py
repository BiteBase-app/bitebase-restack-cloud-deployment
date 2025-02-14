from restack_ai.agent import agent, import_functions, log, condition, child_start, child_execute, agent_info
from datetime import timedelta

with import_functions():
    from apps.backend.functions import my_custom_function, another_custom_function, lookup_sales, llm_chat
    from apps.backend.workflows import my_child_workflow

@agent.defn()
class Agent1:
    @agent.run
    async def run(self):
        log("Agent1 is running")
        await agent.step(my_custom_function, "param1", start_to_close_timeout=timedelta(seconds=10))

@agent.defn()
class Agent2:
    @agent.run
    async def run(self):
        log("Agent2 is running")
        await agent.step(another_custom_function, "param2", start_to_close_timeout=timedelta(seconds=10))

@agent.defn()
class AgentRag:
    @agent.run
    async def run(self):
        log("AgentRag is running")
        await agent.step(lookup_sales, "sales_data", start_to_close_timeout=timedelta(seconds=10))
        await agent.step(llm_chat, "chat_input", start_to_close_timeout=timedelta(seconds=10))

@agent.defn()
class ParentAgent:
    @agent.run
    async def run(self):
        handle = await agent.child_start(
            my_child_workflow,
            input={"key": "value"},
            options={
                "workflow_id": "my-workflow-id",
            }
        )
        return handle

@agent.defn()
class MyAgent:
    @agent.run
    async def run(self):
        info = agent_info()
        log("Agent info: " + str(info))
        await condition(True)
        await agent.step(my_custom_function, "param", start_to_close_timeout=timedelta(seconds=10))
        response = await agent.child_execute(
            my_child_workflow,
            workflow_id="my-workflow-id",
            input={"key": "value"},
        )
        return response
