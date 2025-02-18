{ pkgs }:

pkgs.mkShell {

  buildInputs = with pkgs; [
    python310Packages.pip

    poppler_utils
    tesseract4

    ruff
  ];
}
