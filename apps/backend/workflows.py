from restack_ai.workflow import workflow, import_functions, child_start, child_execute, workflow_info, continue_as_new, log
from datetime import timedelta
from pydantic import BaseModel
from apps.backend.functions.hn.schema import HnSearchInput

with import_functions():
    from apps.backend.functions.openai.chat import openai_todos, FunctionInputParams
    from apps.backend.functions.hn.search import tool_hn_search
    from apps.backend.workflows.child_workflow import my_child_workflow

@dataclass
class WorkflowInputParams(BaseModel):
    pass

@workflow.defn()
class AutomatedWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        hn_results = await workflow.step(tool_hn_search, HnSearchInput(query="ai"), start_to_close_timeout=timedelta(seconds=10))

        user_content = f"You are a personal assistant. Here is the latest hacker news data: {str(hn_results)} Create a todo for me to contact the founder with a one sentence summary of their product"

        result = await workflow.step(openai_todos, FunctionInputParams(user_content=user_content), start_to_close_timeout=timedelta(seconds=10))

        return {"result": result}

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self):
        handle = await workflow.child_start(
            my_child_workflow,
            input={"key": "value"},
            options={
                "workflow_id": "my-workflow-id",
            }
        )
        return handle

@workflow.defn()
class MyWorkflow:
    @workflow.run
    async def run(self):
        info = workflow_info()
        log("Workflow info: " + str(info))
        await continue_as_new()
