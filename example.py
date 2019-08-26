import json
from locust import HttpLocust, TaskSet, task
from locustgraphqlclient import GraphQLLocust


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        query = '''
        mutation login($username: String!, $password: String!) {
          login(username: $username, password: $password) {
            access_token
          }
        }'''
        variables = {
            'username': 'gm',
            'password': 'centric8'
        }
        data = self.client.execute("login", query, variables)
        result = json.loads(data)

        # Inject the Access Token in the Client, so subsequent requests can be made
        self.client.inject_token(result['data']['login']['access_token'])

    def logout(self):
        # Reset the Access Token in the Client, so no subsequent requests can be made
        self.client.inject_token('')

    @task(2)
    def index(self):
        query = '''
                    query products {
                      products {
                        id
                        name
                        image
                      }
                    }'''
        result = self.client.execute("products", query)

    @task(1)
    def profile(self):
        query = '''
                    query me {
                      me {
                        id
                        username
                        firstName
                        lastName                    
                      }
                    }'''
        result = self.client.execute("me", query)


class WebsiteUser(GraphQLLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
