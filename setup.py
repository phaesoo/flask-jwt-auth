from setuptools import setup


setup(
    name='flask-jwt-auth-example',
    version='1.0.0',
    author='hspark',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
