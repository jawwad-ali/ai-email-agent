from agents import Agent, handoff
from ai_email_agent.connection import model
from ai_email_agent.tools import get_email_by_id
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from .globalFunction import on_email_summarize_handoff

email_finder_agent = Agent(
    name = "Email Finder",
    handoff_description="A helpful agent that can read the email by id provided by the user.",
    instructions = """
        You are an assistant capable of fetching emails based on a provided email ID. Your job is only to make fetch the email
        do not summarise it.
    """,
    model = model,
    tools = [get_email_by_id]
)

email_summarizer: Agent = Agent(
    name = 'Email Summarizer',
    handoff_description="A helpful agent that can summarize the email for the user",
    instructions = """ 
        You are an agent capable of summarizing emails. You should summarize the email's content in simple and easy-to-understand English.
        The summary should include key details like:
        Keep your language simple, and always give clear, helpful advice on whether or not to reply based on the email's context.
    """,
    model = model,
)

triage_agent = Agent(
    name = "Triage agent",
    handoff_description="A triage agent that can delegate a user request to the appropriate agent.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a helpful triaging agent. You can use your tools to delegate questions to other appropriate agents. Do not answer by yourself." \
        "Delegate the task to the proper agent"
    ),
    handoffs=[email_finder_agent, handoff(agent=email_summarizer, on_handoff = on_email_summarize_handoff) ],
    model = model,
)