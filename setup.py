import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "1.0.0"

REPO_NAME = "red_wine_quality_prediction"
AUTHOR_USER_NAME = "yshanukajay"
SRC_REPO = "RedWine"
AUTHER_EMAIL = "yshanuka123@gmail.com"

setuptools.setup(
    name="RedWine",
    version=__version__,
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for red wine quality prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    }
)
