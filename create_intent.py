import json
import argparse

from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
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

    return intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def load_json_file(filepath):
    with open(filepath, "r", encoding="UTF-8") as file:
        return json.load(file)


def main() -> None:
    parser = argparse.ArgumentParser(description="Создание намерений потока диалога")
    parser.add_argument("-c", "--credentials", required=True, help="Путь к вашим данным google.json")
    parser.add_argument("-q", "--questions", default="text_questions.json", help="Путь к вопросам в формате json")
    parsed_args = parser.parse_args()

    row_data = load_json_file(parsed_args.credentials)
    project_id = row_data.get("project_id")

    questions = load_json_file(parsed_args.questions)
    for title, contents in questions.items():
        response = create_intent(project_id, title, contents["questions"], [contents["answer"]])
        print(f"Намерения созданы: {response.name}")


if __name__ == "__main__":
    main()
