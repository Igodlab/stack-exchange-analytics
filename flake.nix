{
  description = "Starting to try good Ops procedures w/ Nix";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      pythonPackages = pkgs.python311Packages;
      pyPkgs = pythonPackages: with pythonPackages; [
        pandas
        matplotlib
        numpy
        plotly
        seaborn
      ];
    in
    {
      devShells.x86_64-linux = {
        default = pkgs.mkShell {
          buildInputs = [ 
            (pkgs.python3.withPackages pyPkgs)
            pkgs.streamlit 
            pkgs.cowsay 
          ];
        };
      };
    };
}

