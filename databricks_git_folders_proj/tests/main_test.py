from databricks_git_folders_proj import main


def test_find_all_taxis():
    taxis = main.find_all_taxis()
    assert taxis.count() > 5
