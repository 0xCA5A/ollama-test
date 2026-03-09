{ pkgs }:

pkgs.mkShell {

  buildInputs = with pkgs; [
    python313
    poetry

    poppler_utils
    tesseract4

    ruff
  ];
}
