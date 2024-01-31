import pytest
from images_crawler.pipelines import SQLAlchemyPipeline
from unittest.mock import MagicMock
from images_crawler.pipelines import SQLAlchemyPipeline

@pytest.fixture
def mock_db_manager():
    return MagicMock()

@pytest.fixture
def sqlalchemy_pipeline(mock_db_manager):
    return SQLAlchemyPipeline(mock_db_manager)

def test_process_item(sqlalchemy_pipeline, mock_db_manager):
    fake_item = {
        'images': [{'url': 'http://example.com/image.jpg', 'checksum': 'abc123', 'path': 'images/image.jpg'}]
    }
    result = sqlalchemy_pipeline.process_item(fake_item, None)

    mock_db_manager.add_image.assert_called_with({
        'url': 'http://example.com/image.jpg',
        'file_hash': 'abc123',
        'path': 'images/image.jpg'
    })
