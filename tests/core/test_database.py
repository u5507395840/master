"""Tests para Database Manager"""
import pytest
import os
import tempfile
from core.database import DatabaseManager

@pytest.fixture
def db():
    """Fixture de database temporal"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    db_manager = DatabaseManager(db_path)
    yield db_manager
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

def test_db_initialization(db):
    """Test inicialización de la DB"""
    assert db is not None
    assert os.path.exists(db.db_path)

def test_save_campaign(db):
    """Test guardar campaña"""
    campaign = {
        "id": "TEST001",
        "artist": "Test Artist",
        "track": "Test Track",
        "genre": "trap",
        "status": "active",
        "created_at": "2025-01-01T00:00:00"
    }
    
    result = db.save_campaign(campaign)
    assert result is True

def test_get_campaign(db):
    """Test obtener campaña"""
    campaign = {
        "id": "TEST002",
        "artist": "Test Artist 2",
        "track": "Test Track 2",
        "genre": "reggaeton",
        "status": "active",
        "created_at": "2025-01-01T00:00:00"
    }
    
    db.save_campaign(campaign)
    retrieved = db.get_campaign("TEST002")
    
    assert retrieved is not None
    assert retrieved['artist'] == "Test Artist 2"

def test_get_all_campaigns(db):
    """Test obtener todas las campañas"""
    campaigns = [
        {"id": f"TEST{i}", "artist": f"Artist {i}", "track": f"Track {i}",
         "genre": "trap", "status": "active", "created_at": "2025-01-01T00:00:00"}
        for i in range(5)
    ]
    
    for campaign in campaigns:
        db.save_campaign(campaign)
    
    all_campaigns = db.get_all_campaigns()
    assert len(all_campaigns) >= 5

def test_update_campaign_status(db):
    """Test actualizar estado de campaña"""
    campaign = {
        "id": "TEST003",
        "artist": "Artist",
        "track": "Track",
        "status": "active",
        "created_at": "2025-01-01T00:00:00"
    }
    
    db.save_campaign(campaign)
    result = db.update_campaign_status("TEST003", "paused")
    
    assert result is True
    
    updated = db.get_campaign("TEST003")
    assert updated['status'] == "paused"

def test_get_stats(db):
    """Test obtener estadísticas"""
    stats = db.get_stats()
    
    assert 'total_campaigns' in stats
    assert 'active_campaigns' in stats
    assert isinstance(stats['total_campaigns'], int)

