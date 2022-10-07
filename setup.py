from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="dsi-utils",
    install_requires=[
        "click",
        "pygments",
        "pytest",
        "pytest-asyncio",
        "simplejson",
    ],
    extras_require={
        "develop": [
            "black",
            "isort[pyproject]",
            "pre-commit",
            "pylint",
            "python-dotenv",
            "toml",
        ],
    },
)
