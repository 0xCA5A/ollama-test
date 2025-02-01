# Nix Shell

This folder contains the definition of the *Nix Development Shell* used in this project.

## Usage

To jump into the *Nix Development Shell*, run

```bash
$ nix develop
```

in the project root or let `direnv` do the work for you.

Further information about reproducible development environment can be found on
this [Confluence page](https://confluence.zurrose.ch/x/snQ5B).

## Update

To update the *Nix Development Shell* dependencies (also known as *Flake Inputs*), run

```bash
$ nix flake update
```

in the project root.

### Further Reading

For more documentation on *Nix Flakes* see the [NixOS Wiki](https://nixos.wiki/wiki/Flakes).
