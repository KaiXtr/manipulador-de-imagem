setup(
    name="Manipulador de Imagem",
    version="1.0.0",
    description="Trabalho da matéria de Processamento de sinais e imagens do curso de Ciência da Computação da UDF.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KaiXtr/manipulador-de-imagem",
    author="Ewerton Bramos",
    author_email="ewertonmatheus2113@gmail.com",
    license="GNU",
    classifiers=[
        "Programming Language :: Python",
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=[
        "pillow", "pandas", "PyQt6", "Jinja2"
    ],
    entry_points={"console_scripts": ["imgmani=gui.__main__:main"]},
)
