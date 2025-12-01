import os
import sys
import pytest
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',)))

from run import run_func

@patch('run.read_json_file')
def test_run_func_basic(mock_read_json):

    old_json = [
        {"date": "2025-06-01", "campaign_id": "CAMP-1", "spend": 100},
        {"date": "2025-06-02", "campaign_id": "CAMP-2", "spend": 200},
    ]
    incoming_json = [
        {"date": "2025-06-01", "campaign_id": "CAMP-1", "conversions": 10},
        {"date": "2025-06-02", "campaign_id": "CAMP-2", "conversions": 0},
    ]
    mock_read_json.side_effect = [old_json, incoming_json]

    result = run_func('2025-06-01', '2025-06-02', 'path1.json', 'path2.json')

    assert len(result) == 2

    assert result[0]['CPA'] == 10.0 
    assert result[1]['CPA'] is None  

    for record in result:
        assert set(record.keys()) == {'date', 'campaign_id', 'spend', 'conversions', 'CPA'}

@patch('run.read_json_file', return_value=[])
def test_run_func_empty(mock_read_json):
    result = run_func('2025-06-01', '2025-06-02', 'a.json', 'b.json')
    assert result == []
