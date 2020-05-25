from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="dsi-utils",
    install_requires=[
        "click",
        "pygments",
        "pytest",
        "simplejson",
    ],
    extras_require={
        "dotenv": ["python-dotenv"],
    },
)
