from app.models import Event
import pytest

@pytest.fixture(scope='module')

def new_event():
    event = Event(title='Testing',description='Testing123',
                date='11/06/2019',startTime ='11:11 AM',
                endTime = '12:00 PM')
    return event

def test_new_event(new_event):
    assert new_event.title == 'Testing'
    assert new_event.description == 'Testing123'
    assert new_event.date == '11/06/2019'
    assert new_event.startTime == '11:11 AM'
    assert new_event.endTime == '12:00 PM'