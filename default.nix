# ollama-spell-check is a nix derivation.
# A python script that uses the Ollama LLM to spell check a text file

{ lib, stdenv, fetchFromGitHub, python3, python3Packages }:

stdenv.mkDerivation rec {
  name = "ollama-spell-check-${version}";
  version = "0.1";

  src = fetchFromGitHub {
    owner = "argent0";
    repo = "ollama-spell-check";
    rev = "main";
    sha256 = "sha256-/4ZGNKhgSslDQ5SMV0ISpUNn9LiK7OOdQom0rXYvYYk=";
  };

  propagatedBuildInputs = [
    python3Packages.requests
  ];

  installPhase = ''
    mkdir -p $out/bin
    install -m 755 ${src}/src/ollama-spell-check.py $out/bin/ollama-spell-check
  '';

  meta = with lib; {
    description = "A python script that uses the Ollama LLM to spell check a text file";
    license = licenses.mit;
    maintainers = with maintainers; [ argent0 ];
  };
}
