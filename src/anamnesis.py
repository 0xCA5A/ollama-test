import sys
import logging

import ollama

logger = logging.getLogger(__name__)

MEDICAL_MODELS = ["medllama2:7b", "meditron:7b"]
TRANSLATION_MODEL = "mistral-small3.1:24b"

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

COMMON_GERMAN_WORDS = frozenset(
    [
        "der",
        "die",
        "das",
        "und",
        "ist",
        "in",
        "zu",
        "den",
        "von",
        "mit",
        "ein",
        "eine",
        "für",
        "auf",
        "nicht",
        "sich",
        "des",
        "dem",
        "es",
        "auch",
        "nach",
        "wird",
        "bei",
        "einer",
        "um",
        "am",
        "sind",
        "noch",
        "wie",
        "einem",
        "über",
        "so",
        "zum",
        "kann",
        "wurde",
        "haben",
        "nur",
        "oder",
        "aber",
        "vor",
        "zur",
        "bis",
        "mehr",
        "durch",
        "man",
        "dann",
        "soll",
        "sehr",
        "wenn",
        "keine",
        "schon",
        "werden",
        "patient",
        "patienten",
        "diagnose",
        "therapie",
        "behandlung",
        "symptome",
        "anamnese",
        "befund",
        "beurteilung",
    ]
)

GERMAN_WORD_RATIO_THRESHOLD = 0.08


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


def validate_models(medical_model):
    response = ollama.list()
    available = {m.model for m in response.models}

    missing = []
    for required in [medical_model, TRANSLATION_MODEL]:
        if required not in available:
            missing.append(required)

    if missing:
        print("Fehler: Folgende Modelle sind nicht verfügbar:", file=sys.stderr)
        for m in missing:
            print(f"  - {m} (ollama pull {m})", file=sys.stderr)
        sys.exit(1)


def read_anamnesis():
    print("\nAnamnese eingeben (leere Zeile zum Beenden):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    text = "\n".join(lines)
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


def is_german(text):
    words = text.lower().split()
    if not words:
        return True
    german_count = sum(1 for w in words if w.strip(".,;:!?()") in COMMON_GERMAN_WORDS)
    return (german_count / len(words)) >= GERMAN_WORD_RATIO_THRESHOLD


def translate_to_german(text):
    print("Antwort wird ins Deutsche übersetzt...")
    try:
        response = ollama.chat(
            model=TRANSLATION_MODEL,
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

    model = select_model()
    validate_models(model)

    anamnesis = read_anamnesis()
    result = query_medical_model(model, anamnesis)

    if not is_german(result):
        result = translate_to_german(result)

    print(f"\n{'=' * 50}")
    print("Ergebnis:")
    print(f"{'=' * 50}")
    print(result)


if __name__ == "__main__":
    main()
