{
  description = "Starting to try good Ops procedures w/ Nix";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-22.05";

  outputs = { self, nixpkgs }:
  let 
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in
    { 
      devShells.x86_64-linux = {
        default = pkgs.mkShell {
          buildInputs = [
            pkgs.python311
            pkgs.streamlit
            pkgs.cowsay
          ];
        };
      };
    };
}

