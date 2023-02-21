import json
import time
import urllib
from json.decoder import JSONDecodeError
from typing import Optional

from graphqlclient import GraphQLClient
from locust import User, events


class MeasuredGraphQLClient(GraphQLClient):
    def execute(self, label, query, variables=None, type="graphql") -> Optional[dict]:
        start_time = time.time()
        result = None
        try:
            data = super().execute(query, variables)
            result = json.loads(data)
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, JSONDecodeError) as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=type, name=label, response_time=total_time, exception=e, response_length=0
            )

        else:
            total_time = int((time.time() - start_time) * 1000)
            if "errors" in result:
                events.request_failure.fire(
                    request_type=type,
                    name=label,
                    response_time=total_time,
                    exception=result["errors"],
                    response_length=len(result),
                )
            else:
                events.request_success.fire(
                    request_type=type, name=label, response_time=total_time, response_length=0
                )
        return result


class GraphQLLocust(User):
    abstract = True
    endpoint = ""

    def __init__(self, *args, **kwargs):
        super(GraphQLLocust, self).__init__(*args, **kwargs)
        destination_endpoint = f"{self.host}{self.endpoint}"
        self.client = MeasuredGraphQLClient(endpoint=destination_endpoint)
