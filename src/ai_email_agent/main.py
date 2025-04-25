from agents import Agent, Runner
from ai_email_agent.connection import config, model
from ai_email_agent.tools import get_email_by_id

def run_llm():
    agent = Agent(
        name = "Assistant",
        instructions = "Answer the users query in the most appropriate way",
        model = model,
        tools = [get_email_by_id]
    )

    result = Runner.run_sync(agent, "I want to reterive the email whoses id is 1965e0b50f61640f", run_config=config)
    print(result.final_output)


if __name__ == "__main__":
    run_llm()