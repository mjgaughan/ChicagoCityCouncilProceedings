{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "proceedings_collection_env";
  packages = with pkgs; [
   pkgs.python312
   pkgs.python312Packages.virtualenv
   pkgs.python312Packages.beautifulsoup4
   pkgs.python312Packages.requests
   git
  ];
  shellHook = ''
  echo "Nix shell for collecting Chicago City Council Proceedings."
  '';
}
