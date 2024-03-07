{ sources ? import ./nix/sources.nix
, system ? builtins.currentSystem
, pkgs ? import sources.nixpkgs { inherit system; }
, python ? "python310"
, ...
}:

let
  ## Our base Python:
  thisPython = pkgs.${python}.override {
    packageOverrides = pself: psuper: {
      flake8-comprehensions = pself.buildPythonPackage rec {
        pname = "flake8_comprehensions";
        version = "3.12.0";
        format = "wheel";
        src = pself.fetchPypi {
          inherit pname version format;
          dist = "py3";
          python = "py3";
          sha256 = "sha256-ATI0Y37H38t80pAFePtTxRL4HbkJzv43HAGSMmlcNi0=";
        };
        propagatedBuildInputs = [
          pself.flake8
        ];
      };

      flake8-print = pself.buildPythonPackage rec {
        pname = "flake8_print";
        version = "5.0.0";
        format = "wheel";
        src = pself.fetchPypi {
          inherit pname version format;
          dist = "py3";
          python = "py3";
          sha256 = "sha256-hKGm6hDXBWuAQiGsXmKxzuGu/Il84W8uXELTBGBo9dg=";
        };
        propagatedBuildInputs = [
          pself.flake8
          pself.pycodestyle
        ];
      };

      flake8-pyproject = pself.buildPythonPackage rec {
        pname = "flake8_pyproject";
        version = "1.2.3";
        format = "wheel";
        src = pself.fetchPypi {
          inherit pname version format;
          python = "py3";
          sha256 = "sha256-Ykn+U1RSBa9edoN2RNyAtMEAN+c6Dl24f/Vi11+1vUo=";
        };
        propagatedBuildInputs = [
          pself.flake8
          pself.tomli
        ];
      };

      flake8-type-checking = pself.buildPythonPackage rec {
        pname = "flake8_type_checking";
        version = "2.4.0";
        format = "wheel";
        src = pself.fetchPypi {
          inherit pname version format;
          dist = "py3";
          python = "py3";
          sha256 = "sha256-Le4SfzALuVt/F7fD//T2M29eS6kggsFZKMbhm2Zs+6Q=";
        };
        propagatedBuildInputs = [
          pself.astor
          pself.classify-imports
          pself.flake8
        ];
      };
    };
  };

  ## Our project definition:
  thisProject = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project;

  ## Our package:
  thisPackage = thisPython.pkgs.buildPythonPackage {
    pname = thisProject.name;
    version = thisProject.version;
    format = "pyproject";

    src = ./.;

    propagatedBuildInputs = [
      thisPython.pkgs.python-dateutil
    ];
  };

  ## Our Python with production and development packages:
  thisPythonWithDeps = thisPython.withPackages (ps: with ps;
    thisPackage.propagatedBuildInputs ++ [
      ## Development tools:
      ps.black
      ps.build
      ps.flake8
      ps.flake8-bugbear
      ps.flake8-comprehensions
      ps.flake8-docstrings
      ps.flake8-print
      ps.flake8-pyproject
      ps.flake8-type-checking
      ps.ipython
      ps.isort
      ps.mypy
      ps.nox
      ps.pip
      ps.pylint
      ps.pytest
      ps.pytest-cov
      ps.sphinx
      ps.sphinx-rtd-theme
      ps.sphinxcontrib-apidoc
      ps.twine
      ps.wheel

      ## Types:
      ps.types-python-dateutil
    ]
  );

  ## Our Nix shell:
  thisShell = pkgs.mkShell {
    packages = [
      ## Python dependency with packages for development purposes:
      thisPythonWithDeps

      ## Further development dependencies:
      pkgs.nodePackages.pyright
    ];

    shellHook = ''
      ## Make sure that we emulate Python development (or editable) mode:
      pip install -e . --prefix $TMPDIR/
    '';
  };
in
if pkgs.lib.inNixShell then thisShell else thisPackage
