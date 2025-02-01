{ pkgs }:

pkgs.mkShell {

  buildInputs = with pkgs; [
    python310Packages.pip
    pipenv

    ruff
  ];
}
