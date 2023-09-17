""" Setup file to make the content installable """
import setuptools

repo_url = "https://github.com/Jtachan/genetic_rubiks_solver.git"

if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setuptools.setup(
        url=repo_url,
        name="rubiks_solver",
        author="Jaime Gonzalez Gomez",
        author_email="jim.gomez.dnn@gmail.com",
        version="0.0.0",
        python_requires=">=3.8",
        description="",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        install_requires=[],
    )
