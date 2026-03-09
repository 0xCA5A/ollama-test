{ pkgs }:

pkgs.mkShell {

  buildInputs = with pkgs; [
    python314
    poetry

    poppler_utils
    tesseract4

    ruff
  ];
}
