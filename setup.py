import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='aio-throttle-to-next-second',
    version='0.0.1',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    maintainer='Department for International Trade',
    maintainer_email='webops@digital.trade.gov.uk',
    description='Throttler for asyncio Python that throttles to the next whole second',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/uktrade/aio-throttle-to-next-second',
    py_modules=[
        'aio_throttle_to_next_second',
    ],
    python_requires='~=3.5',
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
