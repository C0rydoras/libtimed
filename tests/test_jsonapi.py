import pytest

from libtimed.jsonapi import deserialize


@pytest.mark.parametrize(
    ("data", "result"),
    [
        (
            {
                "data": {
                    "type": "reports",
                    "id": "1",
                    "attributes": {
                        "comment": "foo",
                    },
                    "relationships": {
                        "task": {
                            "data": {"type": "tasks", "id": "2"},
                        },
                    },
                },
                "included": [
                    {
                        "type": "tasks",
                        "id": "2",
                        "attributes": {
                            "name": "task",
                        },
                        "relationships": {"customer": {"data": {"id": "4", "type": "customers"}}},
                    },
                    {
                        "type": "customers",
                        "id": "4",
                        "attributes": {"name": "customer"},
                    },
                ],
            },
            {
                "type": "reports",
                "id": "1",
                "comment": "foo",
                "task": {
                    "type": "tasks",
                    "id": "2",
                    "name": "task",
                    "customer": {"type": "customers", "id": "4", "name": "customer"},
                },
            },
        ),
        (
            {
                "data": [
                    {
                        "type": "reports",
                        "id": "1",
                        "attributes": {
                            "comment": "foo",
                        },
                        "relationships": {
                            "task": {
                                "data": {"type": "tasks", "id": "2"},
                            },
                        },
                    },
                    {
                        "type": "reports",
                        "id": "2",
                        "attributes": {
                            "comment": "bar",
                        },
                        "relationships": {
                            "task": {
                                "data": {"type": "tasks", "id": "3"},
                            },
                        },
                    },
                ],
                "included": [
                    {
                        "type": "tasks",
                        "id": "2",
                        "attributes": {
                            "name": "task",
                        },
                        "relationships": {"customer": {"data": {"id": "4", "type": "customers"}}},
                    },
                    {
                        "type": "tasks",
                        "id": "3",
                        "attributes": {
                            "name": "docs",
                        },
                        "relationships": {"customer": {"data": {"id": "5", "type": "customers"}}},
                    },
                    {
                        "type": "customers",
                        "id": "4",
                        "attributes": {"name": "customer"},
                    },
                    {
                        "type": "customers",
                        "id": "5",
                        "attributes": {"name": "other-customer"},
                    },
                ],
            },
            [
                {
                    "type": "reports",
                    "id": "1",
                    "comment": "foo",
                    "task": {
                        "type": "tasks",
                        "id": "2",
                        "name": "task",
                        "customer": {"type": "customers", "id": "4", "name": "customer"},
                    },
                },
                {
                    "type": "reports",
                    "id": "2",
                    "comment": "bar",
                    "task": {
                        "type": "tasks",
                        "id": "3",
                        "name": "docs",
                        "customer": {"type": "customers", "id": "5", "name": "other-customer"},
                    },
                },
            ],
        ),
    ],
)
def test_jsonapi_deserialize(data, result):
    assert deserialize(data) == result
