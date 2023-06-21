import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django_apscheduler import util

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime
from django.utils import timezone
from postsapp.models import Post
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def notify_new_post_weekly():
    template = 'weekly_mail.html'

    week = timezone.now() - datetime.timedelta(days=7)

    users = User.objects.all() # Получаем всех зарегистрированных пользователей

    for user in users:

        posts = Post.objects.filter(dataCreation__gte=week) # Получаем все посты за прошедшую неделю

        if posts.exists():
            email_subject = 'News of the Week'
            html = render_to_string(
                template_name=template,
                context={
                    'posts': posts,
                },
            )
            msg = EmailMultiAlternatives(
                subject=email_subject,
                body='',
                from_email='newspaperss@yandex.ru',
                to=[user.email],
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()


# функция, которая будет удалять неактуальные задачи
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            notify_new_post_weekly,
            trigger=CronTrigger(second="*/10"),   # каждые 10 сек для проверки, ниже по понедельникам 10-00
            # trigger=CronTrigger(
            #     day_of_week="mon", hour="10", minute="00"
            # ),
            id="notify_new_post_weekly",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'notify_new_post_weekly'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
