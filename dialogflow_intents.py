import os
import dialogflow_v2 as dialogflow
import json
import argparse


def detect_intent_texts(project_id, session_id, text, language_code='ru-RU'):
    """Returns the result of detect intent with text as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response


def create_intent(project_id, intent):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    response = client.create_intent(parent, intent)
    return response


def create_intents_from_file(project_id, file_name):
    with open(file_name, 'r') as my_file:
        messages = json.load(my_file)

    for key, value in messages.items():
        training_phrases = []
        for question in value['questions']:
            training_phrases.append({
                'parts': [
                    {
                        'text': question,
                    }
                ]
            })
        intent = {
            "display_name": key,
            "messages": [{
                "text": {"text": [value['answer']]}
            }],
            "training_phrases": training_phrases,
        }
        create_intent(project_id=project_id, intent=intent)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.file_name

    project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    create_intents_from_file(
        project_id=project_id,
        file_name=filename,
    )


if __name__ == "__main__":
    main()
