#!/usr/bin/env python

"""Absraction over pyyaml.
Use yaml file as a python object."""

import functools
import yaml


class Storage:
    """Abstraction over pyyaml."""

    def __init__(self, file: str):
        """Interface for using pyyaml as a python object."""
        self._file = file

    @property
    def _node(self):
        """Return node."""
        return Node(self)

    @property
    def _dict(self):
        """Return node."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}
        return content

    def __getattribute__(self, key: str):
        """Get an attribute from the yaml object."""
        if key.startswith("_"):
            return super().__getattribute__(key)
        return self._get([key])
        # return getattr(self._node, [key])

    def __setattr__(self, key: str, value):
        """Set a key/value pair."""
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._set([key], value)

    def _get(self, key_path: list, raw=False):
        """Get a value given a key path."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}
        value = functools.reduce(lambda a, b: a[b], [content] + key_path)
        if not raw and isinstance(value, dict):
            return Node(self, key_path)
        return value

    def _set(self, key_path: list, value):
        """Set a value given a key path."""
        with open(self._file, "r") as stream:
            content = yaml.safe_load(stream) or {}

        dict_ = functools.reduce(
            lambda dict_, key: dict_[key], [content] + key_path[:-1]
        )
        dict_[key_path[-1]] = value
        with open(self._file, "w") as stream:
            yaml.safe_dump(content, stream)

    def __str__(self):
        """Return string representation of a node."""
        return f"Storage({self._dict})"


class Node:
    """Node in pyyaml storage."""

    def __init__(self, storage: Storage, key_path: list = []):
        """Create a given a storage and a key path."""
        self._storage = storage
        self._key_path = key_path

    def __getattribute__(self, key: str):
        """Return the attribute of the node."""
        if key.startswith("_"):
            return super().__getattribute__(key)
        value = self._storage._get(self._key_path + [key])
        if isinstance(value, dict):
            value = Node(self, self._key_path + [key])
        return value

    def __setattr__(self, key: str, value):
        """Set a key/value pair."""
        # print("Node.setattr:", key)
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            # self[key] = value
            self._storage._set(self._key_path + [key], value)

    def __str__(self):
        """Return string representation of a node."""
        content = self._storage._get(self._key_path, raw=True)
        return f"Node({content})"


if __name__ == "__main__":
    from rich import print

    storage = Storage("storage.yml")
    print(storage)
    # print(storage.a)
    storage.a = 1
    storage.b = dict(c=2, d=3)
    storage.c = [1, 2, 3]
    b = storage.b
    print("b:", b)
    print("b.c", b.c)
    print(storage.b.c)
