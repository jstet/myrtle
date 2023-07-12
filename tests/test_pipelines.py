from myrtle.pipelines import get_process_notable_ppl


def test_get_process_notable_ppl():
    lst = get_process_notable_ppl()
    assert isinstance(lst, list)
    print(lst)
