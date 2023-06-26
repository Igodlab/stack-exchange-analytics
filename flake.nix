{
  description = "Starting to try good Ops procedures w/ Nix";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };

      myShellHook = ''
        function parse_git_dirty {
          [[ $(git status --porcelain 2> /dev/null) ]] && echo "*"
        }
        function parse_git_branch {
          git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/ (\1$(parse_git_dirty))/"
        }

        export PS1="\[\033[1;32m\]\W\[\033[33m\]\$(parse_git_branch)\[\033[00m\]$ "
      '';

      # pythonPackages = pkgs.python311Packages;
      # pyPkgs = pythonPackages: with pythonPackages; [
      pyPkgs = pkgs.python3.withPackages ( ps: [
        ps.pandas
        ps.matplotlib
        ps.numpy
        ps.plotly
        ps.seaborn
      ]);
    in
    {
      devShells.x86_64-linux = {
        default = pkgs.mkShell {
          buildInputs = [ 
            # (pkgs.python3.withPackages pyPkgs)
            pyPkgs
            pkgs.streamlit 
            pkgs.cowsay 
          ];

        shellHook = myShellHook;
        };
      };
    };
}

