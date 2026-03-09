#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only process Python files
if [[ "$FILE_PATH" != *.py ]]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR/document_processor" || exit 0
poetry run ruff format "$FILE_PATH" 2>&1
exit 0
