import graphene as g
import MySQLdb as mysql
from flask import Flask
from flask_graphql import GraphQLView
from graph_schema import Query
app = Flask(__name__)

schema = g.Schema(query=Query)

app.add_url_rule('/graphql',view_func=GraphQLView.as_view('graphql',schema=schema, graphiql=True))


if __name__ == "__main__":
    app.run()
