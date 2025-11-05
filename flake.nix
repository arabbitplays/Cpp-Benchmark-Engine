{
  description = "A Nix-flake-based development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs = { self , nixpkgs ,... }: let
    # system should match the system you are running on
    system = "x86_64-linux";
    venvDir = "venv";
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs {
        inherit system;
      };
    in pkgs.mkShell {
      packages = with pkgs; [
        python3
        (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
            # select Python packages here
            matplotlib
        ]))
      ];

      buildInputs = with pkgs; [
        virtualenv
      ];

      shellHook = ''
        echo "Entered dev env"
      '';
    };
  };
}                                                                                           