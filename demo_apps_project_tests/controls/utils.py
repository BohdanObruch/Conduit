def resource(relative_path):
    import demo_apps_project_tests
    from pathlib import Path
    return (
        Path(demo_apps_project_tests.__file__)
        .parent
        .parent
        .joinpath('resources/')
        .joinpath(relative_path)
        .absolute()
        .__str__()
    )
