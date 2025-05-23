import pytest
from tests.test_fixtures import any_to_any_instance
from unittest.mock import patch

def test_empty_directory(any_to_any_instance, tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    with pytest.raises(SystemExit):
        any_to_any_instance.run([str(empty_dir)], format="mp3", output=str(tmp_path), framerate=None, quality=None, merge=False, concat=False, delete=False, across=False, recursive=False, dropzone=False)

def test_permission_error_on_output(any_to_any_instance, tmp_path):
    file_path = tmp_path / "test.mp4"
    file_path.write_bytes(b"\x00" * 128)
    with patch("os.remove", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            any_to_any_instance._post_process((str(tmp_path) + "/", 'test', 'mp4'), str(tmp_path / "out.mp3"), delete=True)

def test_get_file_paths_invalid_directory(any_to_any_instance):
    with pytest.raises(FileNotFoundError):
        any_to_any_instance._get_file_paths(input="nonexistent_directory")

def test_fuzz_random_file_names(any_to_any_instance, tmp_path):
    import random
    import string
    for _ in range(10):
        name = ''.join(random.choices(string.ascii_letters, k=8))
        ext = random.choice(['mp4', 'mp3', 'jpg', 'wav', 'pdf'])
        file = tmp_path / f"{name}.{ext}"
        file.write_bytes(b"\x00" * 128)
    try:
        any_to_any_instance._get_file_paths(str(tmp_path))
    except Exception as e:
        pytest.fail(f"_get_file_paths failed: {e}")
