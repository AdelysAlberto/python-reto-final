import pytest
import os
from unittest.mock import patch
from app.config import Config, DevelopmentConfig, ProductionConfig, config_dict
from app import create_app


class TestConfig:
    
    def test_config_has_required_attributes(self):
        config = Config()
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'SQLALCHEMY_DATABASE_URI')
        assert hasattr(config, 'SQLALCHEMY_TRACK_MODIFICATIONS')
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    
    def test_config_reads_environment_variables(self):
        config = Config()
        assert isinstance(config.SECRET_KEY, str)
        assert len(config.SECRET_KEY) > 0


class TestDevelopmentConfig:
    
    def test_development_config_inheritance(self):
        config = DevelopmentConfig()
        assert config.DEBUG is True
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    
    def test_development_config_secret_key(self):
        config = DevelopmentConfig()
        assert config.SECRET_KEY == "your_secret_key"


class TestProductionConfig:
    
    def test_production_config_inheritance(self):
        config = ProductionConfig()
        assert config.DEBUG is False
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    
    def test_production_config_secret_key(self):
        config = ProductionConfig()
        assert config.SECRET_KEY == "your_secret_key"


class TestConfigDict:
    
    def test_config_dict_contains_development(self):
        assert 'development' in config_dict
        assert config_dict['development'] == DevelopmentConfig
    
    def test_config_dict_contains_production(self):
        assert 'production' in config_dict
        assert config_dict['production'] == ProductionConfig
    
    def test_config_dict_keys(self):
        expected_keys = ['development', 'production']
        assert list(config_dict.keys()) == expected_keys


class TestAppCreation:
    
    def test_create_app_development(self):
        app = create_app('development')
        assert app.config['DEBUG'] is True
        assert 'data_routes' in [bp.name for bp in app.blueprints.values()]
    
    def test_create_app_production(self):
        app = create_app('production')
        assert app.config['DEBUG'] is False
        assert 'data_routes' in [bp.name for bp in app.blueprints.values()]
    
    def test_app_has_blueprints_registered(self):
        app = create_app('development')
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'data_routes' in blueprint_names
    
    def test_app_database_initialization(self):
        app = create_app('development')
        with app.app_context():
            from app import db
            assert db is not None
    
    def test_config_inheritance_chain(self):
        dev_config = DevelopmentConfig()
        prod_config = ProductionConfig()
        
        assert hasattr(dev_config, 'SQLALCHEMY_TRACK_MODIFICATIONS')
        assert hasattr(prod_config, 'SQLALCHEMY_TRACK_MODIFICATIONS')
        assert hasattr(dev_config, 'SECRET_KEY')
        assert hasattr(prod_config, 'SECRET_KEY')