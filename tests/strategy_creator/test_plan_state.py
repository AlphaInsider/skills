from scripts.strategy_plan import main, read_plan_status


def write_plan(tmp_path, status, body="## Universe\n\nSPY only\n"):
    plan = tmp_path / "plan.md"
    plan.write_text(f"---\nstatus: {status}\n---\n\n# Strategy Plan\n\n{body}")
    return plan


def test_missing_plan_starts_the_interview(tmp_path):
    assert read_plan_status(tmp_path / "plan.md") == "interviewing"


def test_draft_plan_resumes_the_interview(tmp_path):
    plan = write_plan(tmp_path, "interviewing")
    assert read_plan_status(plan) == "interviewing"


def test_confirmed_plan_hands_off_to_implementation(tmp_path):
    plan = write_plan(tmp_path, "confirmed")
    assert read_plan_status(plan) == "confirmed"


def test_implemented_plan_returns_to_normal_handling(tmp_path):
    plan = write_plan(tmp_path, "implemented")
    assert read_plan_status(plan) == "implemented"


def test_unknown_status_falls_back_to_interviewing(tmp_path):
    plan = write_plan(tmp_path, "done-ish")
    assert read_plan_status(plan) == "interviewing"


def test_plan_without_frontmatter_is_a_draft(tmp_path):
    plan = tmp_path / "plan.md"
    plan.write_text("# Strategy Plan\n\nsome notes\n")
    assert read_plan_status(plan) == "interviewing"


def test_cli_reports_state_and_next_action(tmp_path, capsys):
    plan = write_plan(tmp_path, "confirmed")
    assert main(["--path", str(plan)]) == 0
    output = capsys.readouterr().out
    assert "plan state: confirmed" in output
    assert "Implement the confirmed plan" in output


def test_cli_missing_plan_points_to_interview(tmp_path, capsys):
    assert main(["--path", str(tmp_path / "plan.md")]) == 0
    output = capsys.readouterr().out
    assert "plan state: interviewing" in output
    assert "interview" in output
