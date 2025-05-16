import json

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main() -> None:
    env = Env()
    env.read_env()
    application_credentials = env.str("GOOGLE_APPLICATION_CREDENTIALS")

    with open(application_credentials, "r", encoding="UTF-8") as file:
        data = json.loads(file.read())
    project_id = data.get("project_id")

    with open("text_questions.json", "r", encoding="UTF-8") as file:
        questions = json.loads(file)
        for title, contents in questions.items():
            create_intent(project_id, title, contents["questions"], [contents["answer"]])


if __name__ == "__main__":
    main()