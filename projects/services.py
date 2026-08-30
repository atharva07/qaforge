from django.db.models import Avg, Count, Q
from testing.models import TestResult

def get_project_test_report(project):
    results = TestResult.objects.filter(
        test_run__suite__project=project
    )

    report = results.aggregate(
        total_results = Count("id"),

        passed = Count(
            "id",
            filter = Q(
                status=TestResult.Status.PASSED
            ),
        ),

        failed = Count(
            "id",
            filter = Q(
                status=TestResult.Status.FAILED
            ),
        ),

        skipped = Count(
            "id",
            filter = Q(
                status=TestResult.Status.SKIPPED
            ),
        ),

        blocked = Count(
            "id",
            filter = Q(
                status=TestResult.Status.BLOCKED
            ),
        ),

        average_duration = Avg("duration"),
    )

    if report["total_results"]:
        report["pass_rate"] = (
            report["passed"]
            / report["total_results"]
        ) * 100
    else:
        report["pass_rate"] = 0

    report["project"] = project.key

    return report
    

