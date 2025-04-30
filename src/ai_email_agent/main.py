from ai_email_agent.connection import config
from ai_email_agent.supermen import triage_agent
import asyncio
from agents import Agent, trace, Runner, MessageOutputItem, ItemHelpers, HandoffOutputItem, ToolCallItem
from ai_email_agent.model import EmailAgentContext
import uuid
import json
import rich

email_with_id = 'Fetch the email with the ID 1966ef6cd8d96c72.'
email_id = ''
email_content = ''

# summary = 'Fetch the email with the ID 1966ef6cd8d96c72 and summarize it'
async def run_llm():
    input_items = []
    email_context = EmailAgentContext()
    current_agent: Agent[EmailAgentContext] = triage_agent
    conversation_id = uuid.uuid4().hex[:16]
    global email_content

    while True:
        user_input = input('Enter your message?')
        with trace('Customer Service' , group_id = conversation_id):
            
            input_items.append({
                'role': 'user',
                'content': f"{user_input} {email_content if email_content else ''}"
            })
            rich.print('input items', input_items)

            result = await Runner.run(current_agent , input_items , context = email_context, run_config=config)
            print('\n\n\n\n\n\n Last Agent Name',result.last_agent.name, "\n")
            print(' Final Output',result.final_output, "\n\n\n\n")

            for new_item in result.new_items:
                agent_name = new_item.agent.name

                if isinstance(new_item , MessageOutputItem):
                    print(f'Agent Name {agent_name}: {ItemHelpers.text_message_output(new_item)}')

                elif isinstance(new_item, HandoffOutputItem):
                    print(f'Handed off output item from {new_item.source_agent.name} to {new_item.target_agent.name}')

                elif isinstance(new_item, ToolCallItem):
                    print(f'{agent_name} calling a tool.')

                else:
                    print(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")

            # Getting the email id and output (actual email) from the LLM response. 
            input_list = result.to_input_list()
            email_content = input_list[4].get('output')

            for item in input_list:
                if 'arguments' in item:
                    try:
                        # Parse the arguments field if it's a JSON string
                        arguments = json.loads(item['arguments'])

                        if 'email_id' in arguments:
                            email_id = arguments['email_id']
                            print(f"Extracted email_id: {email_id}")
                            # break  # Stop once we find the first email_id
                        

                    except json.JSONDecodeError:
                        continue
                
                if 'output' in item:
                    try:
                        arguments = json.loads(item['output'])
                        rich.print('THE ARGUMENTS ARE HERE ==>', arguments)

                    except json.JSONDecodeError:
                        continue

                

if __name__ == "__main__":
    asyncio.run(run_llm())