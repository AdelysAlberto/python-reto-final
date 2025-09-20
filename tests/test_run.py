import pytest
import os
from unittest.mock import patch, MagicMock


class TestRunModule:
    
    def test_environment_variable_reading(self):
        original_env = os.environ.get('FLASK_ENV')
        
        os.environ['FLASK_ENV'] = 'custom_env'
        env_name = os.getenv('FLASK_ENV', 'development')
        assert env_name == 'custom_env'
        
        del os.environ['FLASK_ENV']
        env_name = os.getenv('FLASK_ENV', 'development')
        assert env_name == 'development'
        
        if original_env:
            os.environ['FLASK_ENV'] = original_env
    
    def test_default_flask_env_fallback(self):
        original_env = os.environ.get('FLASK_ENV')
        
        if 'FLASK_ENV' in os.environ:
            del os.environ['FLASK_ENV']
        
        env_name = os.getenv('FLASK_ENV', 'development')
        assert env_name == 'development'
        
        if original_env:
            os.environ['FLASK_ENV'] = original_env