from jubarte.core.scheduler import SimpleSpacedScheduler
from jubarte.models import new_item


def test_generate_initial():
    sched = SimpleSpacedScheduler()
    item = new_item("Teste")
    entry = sched.generate_initial(item)
    assert entry.interval_days == 1


def test_update_good():
    sched = SimpleSpacedScheduler()
    item = new_item("Teste")
    entry = sched.generate_initial(item)
    entry = sched.update(entry, "good")
    assert entry.interval_days >= 1
