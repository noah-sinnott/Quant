import requests
import os

hasura_endpoint=os.environ.get("GRAPHQL_ENDPOINT")
admin_secret=os.environ.get("GRAPHQL_SECRET")

headers = {
    "content-type": "application/json",
    "x-hasura-admin-secret": admin_secret
}

def query_database (graphql_query):
  response = requests.post(hasura_endpoint, json={"query": graphql_query}, headers=headers)
  if response.status_code == 200:
      data = response.json()
      return data
  else:
      print(f"Error: {response.status_code} - {response.text}", graphql_query)
      return False
