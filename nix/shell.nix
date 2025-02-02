{ pkgs }:

pkgs.mkShell {

  buildInputs = with pkgs; [
    python310Packages.pip
    pipenv

    poppler_utils
    tesseract4

    ruff
  ];
}
