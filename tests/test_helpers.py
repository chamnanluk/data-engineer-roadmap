import pandas as pd

from src.utils import helpers


def test_helper_directories_are_defined_under_project_root():
    assert helpers.RAW_DIR == helpers.ROOT_DIR / "data" / "raw"
    assert helpers.CLEANED_DIR == helpers.ROOT_DIR / "data" / "cleaned"
    assert helpers.SAMPLE_OUTPUT_DIR == helpers.ROOT_DIR / "data" / "sample_output"
    assert helpers.SQL_DIR == helpers.ROOT_DIR / "sql"


def test_ensure_directories_creates_missing_paths(tmp_path):
    path_a = tmp_path / "a"
    path_b = tmp_path / "b" / "nested"

    helpers.ensure_directories([path_a, path_b])

    assert path_a.exists() and path_a.is_dir()
    assert path_b.exists() and path_b.is_dir()


def test_normalize_text_formats_strings_and_preserves_nulls():
    assert helpers.normalize_text("  hELLo   woRLD ") == "Hello World"
    assert helpers.normalize_text(42) == "42"
    assert pd.isna(helpers.normalize_text(pd.NA))


def test_write_csv_writes_file_and_returns_output_path(tmp_path):
    df = pd.DataFrame({"col": [1, 2]})
    output_path = tmp_path / "out" / "result.csv"

    returned = helpers.write_csv(df, output_path)

    assert returned == output_path
    assert output_path.exists()

    loaded = pd.read_csv(output_path)
    assert loaded.to_dict(orient="list") == {"col": [1, 2]}
