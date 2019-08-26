from setuptools import setup

setup(
    name='locust-graphql-client',
    version='0.1.0',
    packages=['locustgraphqlclient'],
    url='https://github.com/rohitghatol/locust-graphql-client',
    license='Apache License 2.0',
    author='rohitghatol',
    author_email='',
    description='Locust GraphQL client GraphQL. This is a GraphQLLocust equivalent of HttpLocust',
    install_requires=[
        'graphqlclient',
        'locust'
    ]
)
