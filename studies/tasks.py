import io
import time
from django.core.files import File

from celery import shared_task

from .services import MakeReportTable
from .models import (
    Report,
    ReportStatus,
)


@shared_task()
def run_report(report_id=None):
    """Запускает генерацию отчета
    Args:
        report_id: ID модели Report

    Returns: None

    """
    time.sleep(15)
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        return None
    sheet = MakeReportTable().make_report()
    file = File(io.BytesIO(sheet.xlsx), name=f"report_{report_id}.xlsx")
    report.file = file
    report.status = ReportStatus.ready
    report.save()
