import asyncio
import os
from watchfiles import run_process
import webbrowser
from restack_ai import Restack
from apps.backend.functions import my_custom_function, another_custom_function, lookup_sales, llm_chat
from apps.backend.agents import Agent1, Agent2, AgentRag

client = Restack()

async def custom_service_1():
    await client.start_service(
        agents=[Agent1],
        functions=[my_custom_function],
        task_queue="queue_1"
    )

async def custom_service_2():
    await client.start_service(
        agents=[Agent2],
        functions=[another_custom_function],
        task_queue="queue_2"
    )

async def main():
    await client.start_service(agents=[AgentRag], functions=[lookup_sales, llm_chat])

async def run_services():
    await asyncio.gather(custom_service_1(), custom_service_2(), main())

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
    try:
        asyncio.run(run_services())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")
