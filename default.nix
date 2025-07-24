{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "flask-env";

  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.flask
    pkgs.nodejs_20  # Needed only if you want to build Tailwind locally
    pkgs.git        # Useful for managing versions or fetching packages
  ];

  shellHook = ''
    export FLASK_APP=app.py
    export FLASK_ENV=development
    echo "✅ Flask development environment is ready."
    echo "▶ Run: flask run"
  '';
}
