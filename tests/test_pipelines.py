from myrtle.pipelines import get_process_notable_ppl


def test_get_process_notable_ppl():
    st = get_process_notable_ppl()
    assert isinstance(st, set)
