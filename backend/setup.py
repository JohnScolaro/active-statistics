from setuptools import find_packages, setup

requires = [
    "Flask==3.0.2",
    "boto3==1.34.64",
    "stravalib~=1.3.3",
    "sentry-sdk==1.42.0",
    "rq==1.16.1",
    "plotly==5.20.0",
    "pandas==2.2.1",
    "plotly_calplot==0.1.20",
    "redis==5.0.3",
    "gunicorn==21.2.0",
    "polyline==2.0.2",
    "pillow==10.2.0",
]

dev_requires = [
    "mypy==1.9.0",
    "pytest==8.1.1",
    "freezegun==1.4.0",
    "pytest-redis==3.0.2",
    "pre-commit==3.6.2",
    "black==24.3.0",
    "isort==5.13.2",
    "factory-boy==3.3.0",
    "moto==5.0.3",
]

types_requires = [
    "boto3-stubs[essential]==1.34.64",
    "types-Flask==1.1.6",
    "types-redis==4.6.0.20240311",
    "types-requests==2.31.0.20240311",
    "pandas-stubs==2.2.1.240316",
    "types-setuptools==69.2.0.20240316",
    "types-Pillow==10.2.0.20240311",
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
