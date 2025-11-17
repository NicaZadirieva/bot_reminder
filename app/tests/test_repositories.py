# Repository test
import pytest
from app.repositories.fake_user_repository import FakeUserRepository;

@pytest.mark.asyncio
async def test_get_user():
    repo = FakeUserRepository()
    user = await repo.get_by_id(None, 1)
    
    assert user is not None
    assert user["username"] == "jane_smith"

@pytest.mark.asyncio
async def test_create_user():
    repo = FakeUserRepository()
    
    all_before = await repo.get_all(None)
    assert len(all_before) == 5
    
    new = await repo.create(None, {"telegram_id": 999, "username": "new"})
    
    all_after = await repo.get_all(None)
    assert len(all_after) == 6
    assert new["id"] == 5

@pytest.mark.asyncio
async def test_isolation():
    repo = FakeUserRepository()
    all_users = await repo.get_all(None)
    assert len(all_users) == 5