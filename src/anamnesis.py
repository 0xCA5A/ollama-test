import sys
import logging

import ollama

logger = logging.getLogger(__name__)

MEDICAL_MODELS = ["medllama2:7b", "meditron:7b"]

MEDICAL_SYSTEM_PROMPT = """\
Du bist ein erfahrener Arzt. Analysiere die folgende Anamnese eines Patienten.
Antworte auf Deutsch mit folgender Struktur:

1. Klinische Beurteilung
2. Differentialdiagnosen
3. Empfohlene nächste Schritte
"""

TRANSLATION_PROMPT = """\
Übersetze den folgenden medizinischen Text ins Deutsche. \
Behalte die Struktur und Formatierung bei. \
Gib nur die Übersetzung aus, ohne Kommentar.
"""


def check_connection():
    try:
        ollama.list()
    except Exception as err:
        print(f"Fehler: Verbindung zu Ollama fehlgeschlagen: {err}", file=sys.stderr)
        print("Hinweis: OLLAMA_HOST setzen falls Ollama nicht lokal läuft.", file=sys.stderr)
        sys.exit(1)


def select_model():
    print("\nVerfügbare medizinische Modelle:")
    for i, model in enumerate(MEDICAL_MODELS, 1):
        print(f"  {i}) {model}")

    while True:
        choice = input("\nModell wählen (Nummer): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(MEDICAL_MODELS):
                return MEDICAL_MODELS[index]
        except ValueError:
            pass
        print("Ungültige Auswahl, bitte erneut versuchen.")


def get_available_models():
    response = ollama.list()
    return {m.model for m in response.models}


def validate_models(available, *models):
    missing = [m for m in models if m not in available]
    if missing:
        print("Fehler: Folgende Modelle sind nicht verfügbar:", file=sys.stderr)
        for m in missing:
            print(f"  - {m} (ollama pull {m})", file=sys.stderr)
        sys.exit(1)


def ask_translate(available):
    choice = input("\nAntwort ins Deutsche übersetzen? (j/n): ").strip().lower()
    if choice not in ("j", "ja", "y", "yes"):
        return None
    return select_translation_model(available)


def select_translation_model(available):
    models = sorted(available)
    print("\nVerfügbare Modelle für Übersetzung:")
    for i, model in enumerate(models, 1):
        print(f"  {i}) {model}")

    while True:
        choice = input("\nÜbersetzungsmodell wählen (Nummer): ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(models):
                return models[index]
        except ValueError:
            pass
        print("Ungültige Auswahl, bitte erneut versuchen.")


def read_anamnesis():
    print("\nAnamnese eingeben (Ctrl+D zum Beenden):")
    try:
        text = sys.stdin.read()
    except KeyboardInterrupt:
        print()
        sys.exit(130)

    if not text.strip():
        print("Fehler: Keine Anamnese eingegeben.", file=sys.stderr)
        sys.exit(1)
    return text


def query_medical_model(model, anamnesis):
    print(f"\nAnalyse mit {model} läuft...")
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": MEDICAL_SYSTEM_PROMPT},
            {"role": "user", "content": anamnesis},
        ],
    )
    return response.message.content


def translate_to_german(text, model):
    print(f"\nÜbersetzung mit {model} läuft...")
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": TRANSLATION_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        return response.message.content
    except Exception as err:
        logger.warning("Übersetzung fehlgeschlagen: %s", err)
        print("Hinweis: Übersetzung fehlgeschlagen, zeige englische Antwort.", file=sys.stderr)
        return text


def main():
    print("=== Medizinische Anamnese-Analyse ===")

    check_connection()
    available = get_available_models()

    medical_model = select_model()
    validate_models(available, medical_model)

    translation_model = ask_translate(available)

    anamnesis = read_anamnesis()

    print(f"\n{'=' * 50}")
    print("Prompt:")
    print(f"{'=' * 50}")
    print(MEDICAL_SYSTEM_PROMPT)
    print(anamnesis)

    result = query_medical_model(medical_model, anamnesis)

    if translation_model:
        result = translate_to_german(result, translation_model)

    print(f"\n{'=' * 50}")
    print("Ergebnis:")
    print(f"{'=' * 50}")
    print(result)


if __name__ == "__main__":
    main()
