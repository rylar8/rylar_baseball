import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rylar_baseball',
    version='0.0.1',
    author='Ryley Larson',
    author_email='rlarson.ump@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rylar8/rylar_baseball',
    project_urls = {
    },
    license='MIT',
    packages=['rylar_baseball'],
    install_requires=['requests'],
)
