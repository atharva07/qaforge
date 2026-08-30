from datetime import timezone
from django.db import transaction
from .models import TestRun, TestResult
from django.core.exceptions import ValidationError


@transaction.atomic
def execute_test_run(test_run):
    transition_test_run(
       test_run,
       TestRun.Status.RUNNING,
       started_at = timezone.now()
    )

    test_cases = test_run.suite.test_cases.all()

    for test_case in test_cases:
        TestResult.objects.create(
            test_run=test_run,
            test_case=test_case,
            status=TestResult.Status.PASSED,
        )

    transition_test_run(
        test_run,
        TestRun.Status.COMPLETED,
        completed_at = timezone.now()
    )

    return test_run



ALLOWED_TRANSITIONS = {
    TestRun.Status.PENDING: {
        TestRun.Status.RUNNING,
        TestRun.Status.CANCELLED,
    },

    TestRun.Status.RUNNING: {
        TestRun.Status.COMPLETED,
        TestRun.Status.FAILED,
        TestRun.Status.CANCELLED,
    },

    TestRun.Status.COMPLETED: set(),
    TestRun.Status.FAILED: set(),
    TestRun.Status.CANCELLED: set(),
}

def transition_test_run(test_run, new_status, *, started_at=None, completed_at=None):
    current_status = test_run.status

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValidationError(
            f"Invalid TestRun transition: "
            f"{current_status} -> {new_status}"
        )

    if started_at is not None:
        test_run.started_at = started_at

    if completed_at is not None:
        test_run.completed_at = completed_at

    test_run.status = new_status

    test_run.save(
        update_fields=[
            "status",
            "started_at",
            "completed_at",
        ]
    )

    return test_run