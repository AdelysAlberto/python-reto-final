import pytest
import os
from app.config import Config, DevelopmentConfig, ProductionConfig, config_dict
from app import create_app


class TestConfig:
    
    def test_config_default_values(self):
        config = Config()
        assert config.SECRET_KEY == "your_secret_key"
        assert config.SQLALCHEMY_DATABASE_URI is None
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    
    def test_config_with_environment_variables(self):
        original_secret = os.environ.get('SECRET_KEY')
        original_database = os.environ.get('DATABASE_URI')
        
        os.environ['SECRET_KEY'] = 'test_secret'
        os.environ['DATABASE_URI'] = 'sqlite:///test.db'
        
        config = Config()
        assert config.SECRET_KEY == 'test_secret'
        assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///test.db'
        
        del os.environ['SECRET_KEY']
        del os.environ['DATABASE_URI']
        
        if original_secret:
            os.environ['SECRET_KEY'] = original_secret
        if original_database:
            os.environ['DATABASE_URI'] = original_database


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
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app = create_app('development')
        assert app.config['DEBUG'] is True
        assert 'data_routes' in [bp.name for bp in app.blueprints.values()]
        del os.environ['SQLALCHEMY_DATABASE_URI']
    
    def test_create_app_production(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app = create_app('production')
        assert app.config['DEBUG'] is False
        assert 'data_routes' in [bp.name for bp in app.blueprints.values()]
        del os.environ['SQLALCHEMY_DATABASE_URI']
    
    def test_create_app_with_custom_config(self):
        original_secret = os.environ.get('SECRET_KEY')
        os.environ['SECRET_KEY'] = 'custom_secret'
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app = create_app('development')
        assert app.config['SECRET_KEY'] == 'custom_secret'
        del os.environ['SQLALCHEMY_DATABASE_URI']
        if original_secret:
            os.environ['SECRET_KEY'] = original_secret
        else:
            del os.environ['SECRET_KEY']
    
    def test_app_has_blueprints_registered(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app = create_app('development')
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'data_routes' in blueprint_names
        del os.environ['SQLALCHEMY_DATABASE_URI']
    
    def test_app_database_initialization(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app = create_app('development')
        with app.app_context():
            from app import db
            assert db is not None
        del os.environ['SQLALCHEMY_DATABASE_URI']
    
    def test_app_routes_are_registered(self):
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app = create_app('development')
        with app.test_client() as client:
            response = client.get('/data')
            assert response.status_code == 200
        del os.environ['SQLALCHEMY_DATABASE_URI']
    
    def test_config_inheritance_chain(self):
        dev_config = DevelopmentConfig()
        prod_config = ProductionConfig()
        
        assert hasattr(dev_config, 'SQLALCHEMY_TRACK_MODIFICATIONS')
        assert hasattr(prod_config, 'SQLALCHEMY_TRACK_MODIFICATIONS')
        assert hasattr(dev_config, 'SECRET_KEY')
        assert hasattr(prod_config, 'SECRET_KEY')
    
    def test_environment_variable_override(self):
        original_secret = os.environ.get('SECRET_KEY')
        os.environ['SECRET_KEY'] = 'env_override_secret'
        
        config = Config()
        assert config.SECRET_KEY == 'env_override_secret'
        
        if original_secret:
            os.environ['SECRET_KEY'] = original_secret
        else:
            del os.environ['SECRET_KEY']