import pytest
from app.repositories.fake_user_repository import FakeUserRepository


@pytest.fixture
async def repo():
    return FakeUserRepository()


@pytest.fixture
async def user_data():
    return {
        "telegram_id": 999999999,
        "username": "test_user"
    }


@pytest.fixture
async def original_user(repo):
    return await repo.get_by_id(None, 0)


class TestUserRepository:
    
    @pytest.mark.asyncio
    async def test_get_user(self, repo):
        user = await repo.get_by_id(None, 0)
        
        assert user is not None
        assert user["username"] == "john_doe"
    
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, repo):
        user = await repo.get_by_id(None, 999)
        
        assert user is None
    
    
    @pytest.mark.asyncio
    async def test_get_all_users(self, repo):
        all_users = await repo.get_all(None)
        
        assert len(all_users) == 5
        assert all(isinstance(u, dict) for u in all_users)
    
    
    @pytest.mark.asyncio
    async def test_create_user(self, repo):
        all_before = await repo.get_all(None)
        assert len(all_before) == 5
        
        new = await repo.create(None, {"telegram_id": 999, "username": "new"})
        
        all_after = await repo.get_all(None)
        assert len(all_after) == 6
        assert new["id"] == 5
    
    
    @pytest.mark.asyncio
    async def test_create_with_fixture(self, repo, user_data):
        new = await repo.create(None, user_data)
        
        assert new["telegram_id"] == user_data["telegram_id"]
        assert new["username"] == user_data["username"]
    
    
    @pytest.mark.asyncio
    async def test_create_auto_increments(self, repo):
        user1 = await repo.create(None, {"telegram_id": 111, "username": "u1"})
        user2 = await repo.create(None, {"telegram_id": 222, "username": "u2"})
        user3 = await repo.create(None, {"telegram_id": 333, "username": "u3"})
        
        assert user1["id"] == 5
        assert user2["id"] == 6
        assert user3["id"] == 7
    
    
    @pytest.mark.asyncio
    async def test_update_user_username(self, repo):
        updated = await repo.update(None, 0, username="john_updated")
        
        assert updated is not None
        assert updated["username"] == "john_updated"
        assert updated["id"] == 0
    
    
    @pytest.mark.asyncio
    async def test_update_user_telegram_id(self, repo):
        updated = await repo.update(None, 1, telegram_id=999888777)
        
        assert updated is not None
        assert updated["telegram_id"] == 999888777
        assert updated["username"] == "jane_smith"
    
    
    @pytest.mark.asyncio
    async def test_update_multiple_fields(self, repo):
        updated = await repo.update(
            None,
            2,
            username="bob_updated",
            telegram_id=111222333
        )
        
        assert updated["username"] == "bob_updated"
        assert updated["telegram_id"] == 111222333
        assert updated["id"] == 2
    
    
    @pytest.mark.asyncio
    async def test_update_not_found(self, repo):
        updated = await repo.update(None, 999, username="nonexistent")
        
        assert updated is None
    
    
    @pytest.mark.asyncio
    async def test_update_preserves_fields(self, repo, original_user):
        await repo.update(None, 0, username="new_name")
        updated = await repo.get_by_id(None, 0)
        
        assert updated["username"] == "new_name"
        assert updated["telegram_id"] == original_user["telegram_id"]
    
    
    @pytest.mark.asyncio
    async def test_update_retrieval(self, repo):
        updated = await repo.update(None, 0, username="modified")
        fetched = await repo.get_by_id(None, 0)
        
        assert fetched["username"] == "modified"
        assert fetched["username"] == updated["username"]
    
    
    @pytest.mark.asyncio
    async def test_delete_user(self, repo):
        count_before = len(await repo.get_all(None))
        
        deleted = await repo.delete(None, 0)
        
        assert deleted is True
        count_after = len(await repo.get_all(None))
        assert count_after == count_before - 1
    
    
    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo):
        deleted = await repo.delete(None, 999)
        
        assert deleted is False
    
    
    @pytest.mark.asyncio
    async def test_delete_retrieval_fails(self, repo):
        await repo.delete(None, 0)
        
        user = await repo.get_by_id(None, 0)
        assert user is None
    
    
    @pytest.mark.asyncio
    async def test_isolation(self, repo):
        all_users = await repo.get_all(None)
        assert len(all_users) == 5
    
    
    @pytest.mark.asyncio
    async def test_isolation_separate_repos(self):
        repo1 = FakeUserRepository()
        repo2 = FakeUserRepository()
        
        await repo1.delete(None, 0)
        
        user = await repo2.get_by_id(None, 0)
        assert user is not None
    
    
    @pytest.mark.asyncio
    async def test_crud_full_cycle(self, repo):
        new = await repo.create(None, {"telegram_id": 7777, "username": "test"})
        assert new["id"] == 5
        
        fetched = await repo.get_by_id(None, 5)
        assert fetched["username"] == "test"
        
        updated = await repo.update(None, 5, username="updated")
        assert updated["username"] == "updated"
        
        deleted = await repo.delete(None, 5)
        assert deleted is True
        assert await repo.get_by_id(None, 5) is None
    
    
    @pytest.mark.asyncio
    async def test_get_all_includes_created(self, repo):
        all_before = await repo.get_all(None)
        
        new = await repo.create(None, {"telegram_id": 8888, "username": "new"})
        
        all_after = await repo.get_all(None)
        
        assert new in all_after
        assert len(all_after) == len(all_before) + 1
