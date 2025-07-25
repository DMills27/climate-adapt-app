{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "flask-env";

  buildInputs = with pkgs; [
    python3
    python3Packages.flask
    # Optional: common Flask-related packages
    python3Packages.requests
    python3Packages.pip
    python3Packages.setuptools
    python3Packages.wheel
  ];

  shellHook = ''
    export FLASK_APP=app        # Change to your Flask entrypoint if different
    export FLASK_ENV=development
    echo "Flask environment ready. Run 'flask run' to start the server."
  '';
}
 