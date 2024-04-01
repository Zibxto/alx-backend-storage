#!/usr/bin/env python3
"""Function that changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name"""
    return mongo_collection.update_one({"name": name},
                                       {"$set": {"topics": topics}})
