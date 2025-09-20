from app import db
from app.models import Data


class TestData:

    def test_data_creation(self, app):
        with app.app_context():
            data = Data(name="test_data")
            assert data.name == "test_data"
            assert data.id is None

    def test_data_repr(self, app):
        with app.app_context():
            data = Data(id=1, name="test_data")
            assert repr(data) == "<Data id=1 name=test_data>"

    def test_data_repr_none_id(self, app):
        with app.app_context():
            data = Data(name="test_data")
            assert repr(data) == "<Data id=None name=test_data>"

    def test_data_save_to_database(self, app):
        with app.app_context():
            data = Data(name="test_data")
            db.session.add(data)
            db.session.commit()

            assert data.id is not None
            saved_data = Data.query.get(data.id)
            assert saved_data is not None
            assert saved_data.name == "test_data"

    def test_data_query_by_name(self, app):
        with app.app_context():
            data1 = Data(name="data1")
            data2 = Data(name="data2")
            db.session.add_all([data1, data2])
            db.session.commit()

            found_data = Data.query.filter_by(name="data1").first()
            assert found_data is not None
            assert found_data.name == "data1"

    def test_data_query_all(self, app):
        with app.app_context():
            data1 = Data(name="data1")
            data2 = Data(name="data2")
            data3 = Data(name="data3")
            db.session.add_all([data1, data2, data3])
            db.session.commit()

            all_data = Data.query.all()
            assert len(all_data) == 3
            names = [d.name for d in all_data]
            assert "data1" in names
            assert "data2" in names
            assert "data3" in names

    def test_data_delete(self, app):
        with app.app_context():
            data = Data(name="to_delete")
            db.session.add(data)
            db.session.commit()
            data_id = data.id

            db.session.delete(data)
            db.session.commit()

            deleted_data = Data.query.get(data_id)
            assert deleted_data is None

    def test_data_with_empty_name(self, app):
        with app.app_context():
            data = Data(name="")
            db.session.add(data)
            db.session.commit()

            assert data.id is not None
            assert data.name == ""

    def test_data_with_none_name(self, app):
        with app.app_context():
            data = Data(name=None)
            db.session.add(data)
            db.session.commit()

            assert data.id is not None
            assert data.name is None

    def test_data_with_long_name(self, app):
        with app.app_context():
            long_name = "a" * 100
            data = Data(name=long_name)
            db.session.add(data)
            db.session.commit()

            assert data.id is not None
            assert data.name == long_name

    def test_data_update_name(self, app):
        with app.app_context():
            data = Data(name="original_name")
            db.session.add(data)
            db.session.commit()

            data.name = "updated_name"
            db.session.commit()

            updated_data = Data.query.get(data.id)
            assert updated_data.name == "updated_name"
