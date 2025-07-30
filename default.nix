{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "flask-env";

  buildInputs = with pkgs; [
    python3
    git
    docker
  ];

  shellHook = ''
    export FLASK_APP=app  # Adjust to your entrypoint if needed
    export FLASK_ENV=development

    if [ ! -d .venv ]; then
      echo "Creating virtual environment..."
      python3 -m venv .venv
    fi

    source .venv/bin/activate

    if [ -f requirements.txt ]; then
      echo "Installing dependencies from requirements.txt..."
      pip install --upgrade pip
      pip install -r requirements.txt
    else
      echo "requirements.txt not found!"
    fi

    echo "Virtual environment activated. Run 'flask run' to start the server."
  '';
}
