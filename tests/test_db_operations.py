import os
import sys
import pytest
from unittest.mock import MagicMock, patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',)))
from handler_DB.operations import create_in_db, upsert

sample_data = {
    "date": "2025-06-01",
    "campaign_id": "CAMP-123",
    "spend": 100,
    "conversions": 10,
    "CPA": 10.0
}

@patch('handler_DB.operations.SessionLocal')
def test_create_in_db_success(mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    create_in_db(sample_data)

    mock_db.merge.assert_called_once()
    mock_db.commit.assert_called_once()

@patch('handler_DB.operations.SessionLocal')
def test_upsert_success(mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    upsert(sample_data)

    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()

@patch('handler_DB.operations.SessionLocal')
def test_create_in_db_exception(mock_session):
    mock_db = MagicMock()
    mock_db.merge.side_effect = Exception("DB error")
    mock_session.return_value = mock_db

    create_in_db(sample_data)

@patch('handler_DB.operations.SessionLocal')
def test_upsert_exception(mock_session):
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("DB error")
    mock_session.return_value = mock_db

    upsert(sample_data) 
