import glob
from nox import session, Session, options
import shutil


options.sessions = ["lint", "tests", "examples"]
main_version = ["3.11"]
supported_versions = main_version + ["3.9", "3.10"]
locations = "pysketcher", "tests", "examples", "docs", "noxfile.py"


def _lint(session: Session, install: bool = True) -> None:
    if install:
        session.install(".[lint]")
    session.run("flake8")


@session(python=False)
def local_lint(session: Session) -> None:
    _lint(session, install=False)


@session(python=main_version)
def lint(session: Session) -> None:
    _lint(session, install=True)


def _tests(
    session: Session, cov_report: str = "xml:coverage.xml", install: bool = True
) -> None:
    if install:
        session.install(".[tests]")
    session.run(
        "pytest", "--cov", "--cov-report", cov_report, "--junitxml=test-results.xml"
    )


@session(python=False)
def local_tests(session: Session):
    _tests(session, "html", False)


@session(python=supported_versions)
def tests(session: Session):
    _tests(session)


@session(python=False)
def install(session: Session):
    session.run("pip", "install", "-e", ".[lint,tests,documentation,build]")


@session(python=supported_versions)
def build(session: Session):
    session.run("pip", "install", ".[build]")
    session.run("python", "-m", "build")


def _examples(session: Session, install: bool = False) -> None:
    if install:
        session.install(".[tests]")

    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-o",
        "testpaths=examples",
        "-o",
        "python_files=*.py",
        "-o",
        "python_functions=main",
    )


@session(python=False)
def local_examples(session: Session):
    _examples(session)


@session(python=supported_versions)
def examples(session: Session):
    _examples(session, install=True)


def _documentation(session: Session, install: bool = False) -> None:
    """Build the documentation."""
    if install:
        session.install(".[documentation,tests]")
    session.run("pytest", "pysketcher")  # generate the images by running the docstrings
    for file in glob.glob("./pysketcher/images/*.png"):
        print(f"{file}")
        shutil.copy(file, "./docs/images")
    session.run("sphinx-build", "docs", "docs/_build")


@session(python=main_version)
def documentation(session: Session):
    _documentation(session, install=True)


@session(python=False)
def local_documentation(session: Session):
    _documentation(session)
