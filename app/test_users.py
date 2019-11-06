from app.models import User
import pytest
 
@pytest.fixture(scope='module')
def new_user():
    user = User(email='TESTING123@gmail.com', username='TESTING123')
    user.set_password('TESTING')
    return user
def test_new_user(new_user):
    assert new_user.username == 'TESTING123'
    assert new_user.email == 'TESTING123@gmail.com'
    assert new_user.password_hash != 'TESTING'

def test_user_id(new_user):
    new_user.id=17
    assert isinstance(new_user.get_id(),str)
    assert not isinstance(new_user.get_id(),int)
    assert new_user.get_id() == "17"