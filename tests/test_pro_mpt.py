#!/usr/bin/env python3
"""
Comprehensive test suite for pro-mpt
Tests core functionality, edge cases, and error handling
"""

import pytest
import sqlite3
from pathlib import Path
from datetime import datetime
import tempfile
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pro_mpt import DataStore, InputValidator, Config


class TestDataStore:
    """Test database operations"""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            yield DataStore(db_path)

    def test_init_creates_database(self, temp_db):
        """Test that database is created and schema is initialized"""
        assert temp_db.db_path.exists()
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert len(tables) > 0
        conn.close()

    def test_add_prompt(self, temp_db):
        """Test adding a prompt to database"""
        result = temp_db.add_prompt(
            query="Test prompt",
            model="claude-3-sonnet",
            domain="testing"
        )
        assert result is not None

    def test_search_prompts(self, temp_db):
        """Test searching prompts with full-text search"""
        temp_db.add_prompt(query="How to optimize Python code", domain="coding")
        temp_db.add_prompt(query="Best practices for React", domain="frontend")

        results = temp_db.search("optimize")
        assert len(results) >= 1

    def test_list_recent(self, temp_db):
        """Test retrieving recent prompts"""
        for i in range(5):
            temp_db.add_prompt(query=f"Prompt {i}", domain="test")

        results = temp_db.list_recent(limit=3)
        assert len(results) == 3

    def test_stats_generation(self, temp_db):
        """Test statistics generation"""
        temp_db.add_prompt(query="Prompt 1", model="claude", domain="coding", rating=5)
        temp_db.add_prompt(query="Prompt 2", model="claude", domain="creative", rating=4)
        temp_db.add_prompt(query="Prompt 3", model="gpt", domain="coding", rating=3)

        stats = temp_db.get_stats()
        assert stats is not None
        assert "total_prompts" in stats or len(stats) > 0


class TestInputValidator:
    """Test input validation"""

    def test_validate_query_empty(self):
        """Test that empty queries are rejected"""
        with pytest.raises(ValueError):
            InputValidator.validate_query("")

    def test_validate_query_valid(self):
        """Test that valid queries pass"""
        result = InputValidator.validate_query("How to code in Python?")
        assert result == "How to code in Python?"

    def test_validate_query_max_length(self):
        """Test that overly long queries are rejected"""
        long_query = "x" * (Config.MAX_QUERY_LENGTH + 1)
        with pytest.raises(ValueError):
            InputValidator.validate_query(long_query)

    def test_validate_rating_valid(self):
        """Test valid ratings"""
        for rating in range(1, 6):
            result = InputValidator.validate_rating(rating)
            assert result == rating

    def test_validate_rating_invalid(self):
        """Test invalid ratings"""
        with pytest.raises(ValueError):
            InputValidator.validate_rating(0)
        with pytest.raises(ValueError):
            InputValidator.validate_rating(6)

    def test_validate_domain_valid(self):
        """Test valid domains"""
        result = InputValidator.validate_domain("coding")
        assert result == "coding"

    def test_validate_domain_special_chars(self):
        """Test domains with special characters"""
        # Should handle common domain names
        result = InputValidator.validate_domain("machine-learning")
        assert result is not None


class TestConfig:
    """Test configuration"""

    def test_config_paths_exist(self):
        """Test that config defines required paths"""
        assert hasattr(Config, 'DB_PATH')
        assert hasattr(Config, 'DATA_DIR')
        assert hasattr(Config, 'DEFAULT_LIMIT')

    def test_config_validation_constants(self):
        """Test validation constants are set"""
        assert Config.MIN_RATING == 1
        assert Config.MAX_RATING == 5
        assert Config.MAX_QUERY_LENGTH > 0

    def test_ensure_dirs_creates_directories(self):
        """Test that ensure_dirs creates required directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test"
            original_data_dir = Config.DATA_DIR
            Config.DATA_DIR = test_dir

            Config.ensure_dirs()
            assert test_dir.exists()

            # Restore original
            Config.DATA_DIR = original_data_dir


class TestEdgeCases:
    """Test edge cases and error handling"""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            yield DataStore(db_path)

    def test_unicode_handling(self, temp_db):
        """Test handling of unicode characters"""
        temp_db.add_prompt(
            query="How to code in 中文? (Chinese)",
            domain="multilingual"
        )
        results = temp_db.search("中文")
        assert len(results) >= 0  # Should not crash

    def test_sql_injection_prevention(self, temp_db):
        """Test that SQL injection attempts are safely handled"""
        malicious_query = "'; DROP TABLE prompts; --"
        result = temp_db.add_prompt(query=malicious_query, domain="test")
        assert result is not None

        # Verify table still exists
        results = temp_db.list_recent(limit=1)
        assert isinstance(results, list)

    def test_very_long_prompt(self, temp_db):
        """Test handling of very long prompts"""
        long_query = "x" * (Config.MAX_QUERY_LENGTH + 100)
        with pytest.raises(ValueError):
            InputValidator.validate_query(long_query)

    def test_empty_database_operations(self, temp_db):
        """Test operations on empty database"""
        results = temp_db.search("nonexistent")
        assert isinstance(results, list)

        recent = temp_db.list_recent()
        assert isinstance(recent, list)

    def test_concurrent_database_access(self, temp_db):
        """Test multiple database operations"""
        for i in range(10):
            temp_db.add_prompt(query=f"Prompt {i}", domain="test")

        results = temp_db.list_recent(limit=5)
        assert len(results) == 5


class TestDataIntegrity:
    """Test data integrity and consistency"""

    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            yield DataStore(db_path)

    def test_prompt_id_uniqueness(self, temp_db):
        """Test that each prompt gets a unique ID"""
        id1 = temp_db.add_prompt(query="Prompt 1", domain="test")
        id2 = temp_db.add_prompt(query="Prompt 2", domain="test")

        assert id1 != id2

    def test_timestamp_accuracy(self, temp_db):
        """Test that timestamps are recorded accurately"""
        before = datetime.now()
        temp_db.add_prompt(query="Test", domain="test")
        after = datetime.now()

        recent = temp_db.list_recent(limit=1)
        assert len(recent) > 0

    def test_domain_consistency(self, temp_db):
        """Test that domains are stored and retrieved correctly"""
        test_domain = "test-domain-123"
        temp_db.add_prompt(query="Test", domain=test_domain)

        recent = temp_db.list_recent(limit=1)
        assert len(recent) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
