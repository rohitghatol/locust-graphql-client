import time
import urllib
from locust import Locust, events
from graphqlclient import GraphQLClient


class MeasuredGraphQLClient(GraphQLClient):

    def execute(self, label, query, variables=None):
        start_time = time.time()
        try:
            result = super().execute(query, variables)
        except urllib.error.HTTPError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="graphql", name=label, response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="graphql", name=label, response_time=total_time, response_length=0)
        return result


class GraphQLLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(GraphQLLocust, self).__init__(*args, **kwargs)
        print('000000')
        print(self.host)
        self.client = MeasuredGraphQLClient(endpoint=self.host)
