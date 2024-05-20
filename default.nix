# ollama-spell-check is a nix derivation.
# A python script that uses the Ollama LLM to spell check a text file

{ stdenv, fetchFromGitHub, python3, ollama, python3Packages }: 

stdenv.mkDerivation rec {
  name = "ollama-spell-check-${version}";
  version = "0.1";

  src = fetchFromGitHub {
    owner = "argent0";
    repo = "ollama-spell-check";
    rev = "master";
    sha256 = "<sha256>";
  };

  buildInputs = [
    python3
    python3Packages.requests
    ollama.override { acceleration = "cuda"; }
  ];

  installPhase = ''
    mkdir -p $out/bin
    cp $src/ollama-spell-check.py $out/bin/ollama-spell-check
    chmod +x $out/bin/ollama-spell-check
  '';

  meta = with stdenv.lib; {
    description = "A python script that uses the Ollama LLM to spell check a text file";
    license = licenses.mit;
    maintainers = with maintainers; [ argent0 ];
  };
}
