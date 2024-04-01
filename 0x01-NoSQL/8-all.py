#!/usr/bin/env python3
"""Function that lists all documents in a collection"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    result = mongo_collection.find()
    if result is None:
        return []
    else:
        return result
