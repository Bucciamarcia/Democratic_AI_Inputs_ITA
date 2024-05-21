from openai import OpenAI, OpenAIError
import json
import os
from time import time, sleep
import textwrap
import yaml

client = OpenAI(
    api_key=os.environ.get("OPENAI_APIKEY"),
)


###     file operations


def save_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(content)


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as infile:
        return infile.read()


def save_yaml(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        yaml.dump(data, file, allow_unicode=True)


def open_yaml(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


###     API functions


def chatbot(conversation, model="gpt-4o", temperature=0):
    max_retry = 7
    retry = 0
    while True:
        try:
            response = client.chat.completions.create(
                model=model, messages=conversation, temperature=temperature
            )
            text = response.choices[0].message.content
            return text, response.usage.total_tokens
        except OpenAIError as oops:
            print(f"OpenAI Error: {oops}")
            raise oops
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if "maximum context length" in str(oops):
                a = conversation.pop(0)
                print("\n\n DEBUG: Trimming oldest message")
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f"\n\nRetrying in {2 ** (retry - 1) * 5} seconds...")
            sleep(2 ** (retry - 1) * 5)


###     CHAT FUNCTIONS


def get_user_input():
    # get user input
    text = input("\n\n\nUSER:\n")

    # check if scratchpad updated, continue
    if "DONE" in text:
        print(
            "\n\n\nGrazie per aver partecipato al nostro sondaggio! Il tuo risultato è stato salvato. Il programma si chiuderà fra 5 secondi."
        )
        sleep(5)
        exit(0)
    if text == "":
        # empty submission, probably on accident
        None
    else:
        return text


def compose_conversation(ALL_MESSAGES, text, system_message):
    # continue with composing conversation and response
    ALL_MESSAGES.append({"role": "user", "content": text})
    conversation = list()
    conversation += ALL_MESSAGES
    conversation.append({"role": "system", "content": system_message})
    return conversation


def generate_chat_response(ALL_MESSAGES, conversation):
    # generate a response
    response, tokens = chatbot(conversation)
    if tokens > 25000:
        print(
            "Sfortunatamente questa conversazione è diventata troppo lunga, quindi non può continuare. Il programma si chiuderà fra 5 secondi."
        )
        sleep(5)
        exit(0)
    ALL_MESSAGES.append({"role": "assistant", "content": response})
    print("\n\n\n\nCHATBOT:\n")
    formatted_lines = [textwrap.fill(line, width=120) for line in response.split("\n")]
    formatted_text = "\n".join(formatted_lines)
    print(formatted_text)


def evaluate_stop_condition(conversation):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "valuta_condizione_di_stop",
                "description": "Valuta se la conversazione è giunta al termine",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_done": {
                            "type": "boolean",
                            "description": "Indica se la conversazione è terminata",
                        }
                    },
                    "required": ["is_done"],
                },
            },
        }
    ]
    messages = [
        {
            "role": "system",
            "content": (
                "Sei un'intelligenza artificiale che deve valutare una conversazione. "
                "Il tuo unico compito è valutare se la conversazione è terminata. "
                "Il tuo output è true se l'agente ha ringraziato l'utente alla fine del sondaggio, "
                "altrimenti è false.\n\n"
                "NOTA: Se il tuo output è true, la finestra di chat dell'agente verrà automaticamente disconnessa: "
                "quindi rispondi true solo se l'agente ha propriamente salutato l'utente."
            ),
        },
        {"role": "user", "content": conversation},
    ]
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {
                "name": "valuta_condizione_di_stop",
            }
        }
    )

    args = json.loads(
        completion.choices[0].message.tool_calls[0].function.arguments
    )
    return args["is_done"]


if __name__ == "__main__":
    # instantiate chatbot, variables
    research_question = open_file("question.txt")
    system_message = open_file("system.txt").replace("<<QUESTION>>", research_question)
    ALL_MESSAGES = list()
    start_time = time()

    # get username, start conversation
    print(
        '\n\n****** IMPORTANTE: ******\n\nScrivi "DONE" (senza virgolette) per uscire dal programma\n\nDomanda di ricerca: %s'
        % research_question
    )
    username = input("\n\n\nPer iniziare, per favore inserisci il tuo nome: ").strip()
    filename = f"chat_{start_time}_{username}.yaml"
    text = f"Ciao, il mio nome è {username}."
    conversation = compose_conversation(ALL_MESSAGES, text, system_message)
    generate_chat_response(ALL_MESSAGES, conversation)

    while True:
        text = get_user_input()
        if not text:
            continue

        conversation = compose_conversation(ALL_MESSAGES, text, system_message)
        save_yaml(f"chat_logs/{filename}", ALL_MESSAGES)

        generate_chat_response(ALL_MESSAGES, conversation)
        save_yaml(f"chat_logs/{filename}", ALL_MESSAGES)
        if evaluate_stop_condition(text):
            print("Grazie per aver partecipato al nostro sondaggio!")
            sleep(5)
            exit(0)
