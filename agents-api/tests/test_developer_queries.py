# Tests for agent queries
from uuid import uuid4

from ward import raises, test

from agents_api.common.protocol.developers import Developer
from agents_api.models.developer.get_developer import get_developer, verify_developer
from tests.fixtures import cozo_client, test_developer_id


@test("model: get developer")
async def _(client=cozo_client, developer_id=test_developer_id):
    developer = await get_developer(
        developer_id=developer_id,
        client=client,
    )

    assert isinstance(developer, Developer)
    assert developer.id


@test("model: verify developer exists")
async def _(client=cozo_client, developer_id=test_developer_id):
    await verify_developer(
        developer_id=developer_id,
        client=client,
    )


@test("model: verify developer not exists")
async def _(client=cozo_client):
    with raises(Exception):
        await verify_developer(
            developer_id=uuid4(),
            client=client,
        )
