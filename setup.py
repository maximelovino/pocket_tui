import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pocket-tui",
    version="1.0",
    author="Maxime Lovino",
    author_email="maximelovino@gmail.com",
    description="A terminal UI for managing Pocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maximelovino/pocket_tui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['pocket_tui=pocket_tui.__main__:main_loop']
    },
    install_requires=[
        'astroid==2.3.3',
        'autopep8==1.4.4',
        'cachetools==4.1.0',
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'diskcache==4.1.0',
        'google-api-core==1.17.0',
        'google-api-python-client==1.8.1',
        'google-auth==1.14.0',
        'google-auth-httplib2==0.0.3',
        'googleapis-common-protos==1.51.0',
        'httplib2==0.18.0',
        'idna==2.8',
        'isort==4.3.21',
        'lazy-object-proxy==1.4.3',
        'mccabe==0.6.1',
        'prompt-toolkit==1.0.14',
        'protobuf==3.18.3',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'pycodestyle==2.5.0',
        'Pygments==2.6.1',
        'PyInquirer==1.0.3',
        'pylint==2.4.4',
        'python-dotenv==0.10.3',
        'pytz==2019.3',
        'regex==2020.4.4',
        'requests==2.22.0',
        'requests-file==1.4.3',
        'rsa==4.0',
        'six==1.13.0',
        'tldextract==2.2.2',
        'uritemplate==3.0.1',
        'urllib3==1.25.7',
        'wcwidth==0.1.9',
        'wrapt==1.11.2'
    ]
)
