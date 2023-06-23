# models.py
# defines the models for different Nodes and Relationships

from neomodel import (
    DateTimeProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    cardinality,
)


### structured relationships
class UpvotedBy(StructuredRel):
    upvoted_at = DateTimeProperty(default_now=True)


class DownvotedBy(StructuredRel):
    downvoted_at = DateTimeProperty(default_now=True)


### nodes and properties
class User(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)


class UpvotableNode(StructuredNode):
    __abstract_node__ = True
    uuid = UniqueIdProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    upvoters = RelationshipTo(User, "UPVOTED_BY", model=UpvotedBy)
    downvoters = RelationshipTo(User, "DOWNVOTED_BY", model=DownvotedBy)

    # define methods to build a Cypher query to return upvote/downvote count:
    def _upvotes_query(self) -> str:
        return f"""\
         MATCH
            ({{uuid: '{self.uuid}'}})-[uv:UPVOTED_BY]->()
        RETURN
            COUNT(uv)
        """

    def _downvotes_query(self) -> str:
        return f"""\
         MATCH
            ({{uuid: '{self.uuid}'}})-[dv:DOWNVOTED_BY]->()
        RETURN
            COUNT(dv)
        """

    # this is more efficient (leverages the Neo4J count store) than returning
    # the results and counting them:
    def n_upvotes(self):
        count_upvotes_query = self._upvotes_query()
        results, columns = self.cypher(count_upvotes_query)
        return results[0][0]

    def n_downvotes(self):
        count_downvotes_query = self._downvotes_query()
        results, columns = self.cypher(count_downvotes_query)
        return results[0][0]


class Thread(UpvotableNode):
    title = StringProperty(required=True, unique_index=True)
    body = StringProperty(required=True)
    author = RelationshipTo(User, "AUTHORED_BY", cardinality=cardinality.One)
    children = RelationshipFrom("ReplyTopLevel", "IN_REPLY_TO")


class Reply(UpvotableNode):
    body = StringProperty(required=True)
    author = RelationshipTo(User, "AUTHORED_BY", cardinality=cardinality.One)
    children = RelationshipFrom("Reply", "IN_REPLY_TO")


class ReplyTopLevel(Reply):
    parent = RelationshipTo(Thread, "IN_REPLY_TO", cardinality=cardinality.One)


class ReplyLowerLevel(Reply):
    parent = RelationshipTo(Reply, "IN_REPLY_TO")
