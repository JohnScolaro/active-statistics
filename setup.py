from setuptools import find_packages, setup

requires = [
    "Flask==2.3.3",
    "boto3==1.28.40",
    "stravalib~=1.3.3",
    "sentry-sdk==1.30.0",
    "rq==1.15.1",
    "plotly==5.16.1",
    "pandas==1.5.3",
    "plotly-calplot==0.1.16",
    "redis==5.0.0",
    "gunicorn==21.2.0",
]

dev_requires = [
    "mypy==1.5.1",
    "pytest==7.4.0",
    "freezegun==1.2.2",
    "pytest-redis==3.0.2",
    "pre-commit==3.3.3",
    "black==23.7.0",
    "isort==5.12.0",
    "factory-boy==3.3.0",
]

types_requires = [
    "boto3-stubs[essential]==1.28.36",
    "types-Flask==1.1.6",
    "types-redis==4.6.0.5",
    "pandas-stubs==2.0.3.230814",
    "types-setuptools==68.1.0.1",
]

setup(
    name="active_statistics",
    version="1.0",
    author="John Scolaro",
    email="johnscolaro95@gmail.com",
    packages=find_packages(),
    install_requires=requires,
    extras_require={"dev": dev_requires + types_requires},
)
