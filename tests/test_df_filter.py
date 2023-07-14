import pytest
import pandas as pd
from myrtle.pipelines import filter_author, filter_quotes
from pandas.testing import assert_frame_equal
from faker import Faker


@pytest.fixture
def sample_chunk_1():
    data = {
        "author": [
            "John Doe",
            "Mary Smith-surname",
            "David Johnson",
            "Emily Davis",
            "Name smithson",
            "Fake Name",
            "Sarah Dessen",
        ],
        "quote": ["Quote 1", "Quote 2", "Quote 3", "Quote 4", "Quote", "Quote", "Quote"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_chunk_2():
    data = {
        "quote": [
            "dummy_quote_1",
            "dummy_quote_2",
            "dummy_quote_3",
            "dummy_quote_4",
            "dummy_quote_5",
            "dummy_quote_6",
            "dummy_quote_7",
            "dummy_quote_8",
            "dummy_quote_9",
            "dummy_quote_10",
        ],
        "author": [
            "Jamie McGuire, Beautiful Disaster",
            "J.R.R. Tolkien, The Fellowship of the Ring",
            "Oscar Wilde, The Importance of Being Earnest",
            "Chuck Palahniuk, Choke",
            "Friedrich Nietzsche",
            "Nicholas Sparks, The Notebook",
            "Emily Brontë, Wuthering Heights",
            "Candace Bushnell, Sex and the City",
            "Paul McCartney, The Beatles Illustrated Lyrics",
            "Suzanne Collins, Mockingjay",
        ],
        "category": [
            "beatrice, divergent, humor, love, inspirational",
            "beatrice, inspirational, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, divergent, humor, love, tobias",
            "beatrice, inspirational, humor, love, tobias",
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def expected():
    expected_df = pd.DataFrame(
        {
            "quote": ["dummy_quote_1", "dummy_quote_10"],
            "author": ["Jamie McGuire, Beautiful Disaster", "Suzanne Collins, Mockingjay"],
            "category": [
                "beatrice, divergent, humor, love, inspirational",
                "beatrice, inspirational, humor, love, tobias",
            ],
        }
    )
    return expected_df


@pytest.fixture
def names():
    with open("./data/notable.csv", "r") as file:
        set_contents = file.read()
    names = set(set_contents.split("\n"))
    return names


def test_filter_author_simple(sample_chunk_1):
    names_set = {"John Do", "Mary Smith surname", "Name Fakename", "Emily", "Name smithon", "féke namó", "Sarah Dessen"}
    filtered_rows = sample_chunk_1.apply(filter_author, args=(names_set,), axis=1)
    expected_filtered_rows = [False, True, False, False, True, False, True]
    assert list(filtered_rows) == expected_filtered_rows


def test_filter_author_real(sample_chunk_2, names):
    filtered_rows = sample_chunk_2.apply(filter_author, args=(names,), axis=1)
    expected_filtered_rows = [True, False, False, False, False, False, True, True, False, True]
    assert list(filtered_rows) == expected_filtered_rows


def test_filter_quotes(sample_chunk_2, names, expected):
    filtered = filter_quotes(sample_chunk_2, names)
    print("\n", filtered, "\n \n")
    assert_frame_equal(filtered.reset_index(drop=True), expected.reset_index(drop=True))


fake = Faker()


@pytest.fixture
def sample_chunk_2_large():
    num_rows = 40  # Specify the desired number of rows

    data = {
        "quote": [fake.sentence() for _ in range(num_rows)],
        "author": [fake.name() for _ in range(num_rows)],
        "category": [fake.word() for _ in range(num_rows)],
    }

    return pd.DataFrame(data)


# Test function using the larger fixture
def test_filter_quotes_larger(sample_chunk_2_large, names):
    filtered = filter_quotes(sample_chunk_2_large, names)
    print(filtered)
