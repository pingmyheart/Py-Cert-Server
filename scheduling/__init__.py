from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from scheduling.update_certificates_scheduler import UpdateCertificateScheduler
from service import certificate_service_bean, ca_service_bean

update_certificates_scheduler_bean = UpdateCertificateScheduler(certificate_service=certificate_service_bean,
                                                                certification_authority_service=ca_service_bean)
scheduler = BackgroundScheduler(timezone=ZoneInfo("UTC"))
cron_expr_every_minute = CronTrigger.from_crontab("* * * * *")

scheduler.add_job(update_certificates_scheduler_bean.schedule, cron_expr_every_minute)
scheduler.start()
