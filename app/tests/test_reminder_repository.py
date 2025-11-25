# -*- coding: utf-8 -*-
import pytest
from datetime import datetime, timedelta
from app.repositories.fake_reminder_repository import FakeReminderRepository


@pytest.fixture
async def repo():
    return FakeReminderRepository()


class TestReminderRepository:
    
    # ============ GET TESTS (7) ============
    
    @pytest.mark.asyncio
    async def test_get_all(self, repo):
        reminders = await repo.get_all(None)
        assert len(reminders) == 9
    
    @pytest.mark.asyncio
    async def test_get_by_id(self, repo):
        reminder = await repo.get_by_id(None, 1)
        assert reminder.text == "Buy milk"
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo):
        reminder = await repo.get_by_id(None, 999)
        assert reminder is None
    
    
    
    # ============ CREATE TESTS (3) ============
    
    @pytest.mark.asyncio
    async def test_create_reminder(self, repo):
        new = await repo.create(None, {
            "telegram_id": 999,
            "text": "Test",
            "remind_at": datetime.now() + timedelta(hours=1),
            "priority": "high",
            "status": "active",
        })
        assert new.id == 10
    
    @pytest.mark.asyncio
    async def test_create_auto_increments(self, repo):
        r1 = await repo.create(None, {"telegram_id": 1, "text": "1", "remind_at": datetime.now(), "priority": "high", "status": "active"})
        r2 = await repo.create(None, {"telegram_id": 2, "text": "2", "remind_at": datetime.now(), "priority": "high", "status": "active"})
        
        assert r1.id == 10
        assert r2.id == 11
    
    # ============ UPDATE TESTS (5) ============
    
    @pytest.mark.asyncio
    async def test_update_status(self, repo):
        updated = await repo.update(None, 1, status="completed")
        assert updated.status == "completed"
    
    @pytest.mark.asyncio
    async def test_update_text(self, repo):
        updated = await repo.update(None, 1, text="New text")
        assert updated.text == "New text"
    
    @pytest.mark.asyncio
    async def test_update_multiple_fields(self, repo):
        updated = await repo.update(None, 1, status="done", priority="low")
        assert updated.status == "done"
        assert updated.priority == "low"
    
    @pytest.mark.asyncio
    async def test_update_not_found(self, repo):
        updated = await repo.update(None, 999, status="done")
        assert updated is None
    
    # ============ DELETE TESTS (3) ============
    
    @pytest.mark.asyncio
    async def test_delete_reminder(self, repo):
        deleted = await repo.delete(None, 1)
        assert deleted is True
    
    @pytest.mark.asyncio
    async def test_delete_not_found(self, repo):
        deleted = await repo.delete(None, 999)
        assert deleted is False
    
    @pytest.mark.asyncio
    async def test_delete_removes_from_storage(self, repo):
        await repo.delete(None, 1)
        reminder = await repo.get_by_id(None, 1)
        assert reminder is None
    
    # ============ ISOLATION TESTS (2) ============
    
    @pytest.mark.asyncio
    async def test_isolation_separate_repos(self):
        repo1 = FakeReminderRepository()
        repo2 = FakeReminderRepository()
        
        await repo1.delete(None, 1)
        
        reminder = await repo2.get_by_id(None, 1)
        assert reminder is not None
    
    @pytest.mark.asyncio
    async def test_isolation_create_independent(self):
        repo1 = FakeReminderRepository()
        repo2 = FakeReminderRepository()
        
        all_before = len(await repo2.get_all(None))
        await repo1.create(None, {"telegram_id": 999, "text": "x", "remind_at": datetime.now(), "priority": "high", "status": "active"})
        all_after = len(await repo2.get_all(None))
        
        assert all_before == all_after
