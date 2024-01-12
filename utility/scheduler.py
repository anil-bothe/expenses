from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from datetime import datetime
from django.conf import settings
from abc import abstractclassmethod, ABC
from django.core.mail import send_mail


class EmailSchedulerBase(ABC):
    @abstractclassmethod
    def send_message(self):
        pass 

    @abstractclassmethod
    def start(self):
        pass 


"""
Email schedular
"""
class EmailScheduler(EmailSchedulerBase):
    def __init__(self, expense, subject="Expense Notification") -> None:
        self.scheduler = BackgroundScheduler()
        self.job_id = None 

        self.subject = subject
        self.expense = expense
        self.message = {
            "Equal": "Hi {participant_name},\n\n You've been added to an expense in Expense Sharing App! {expense_name} was added by {creator_name}, and everyone owes Rs. {your_share} equally.\n\n Regards,\n Expense Sharing App!",
            "Exact": "Hi {participant_name},\n\n You've been added to an expense in Expense Sharing App! {expense_name} was added by {creator_name}, and your specific share is Rs. {your_share} equally.\n\n Regards,\n Expense Sharing App!",
            "Percent": "Hi {participant_name},\n\n You've been added to an expense in Expense Sharing App! {expense_name} was added by {creator_name}, and your share is {percentage}% which amounts to Rs {your_share} .\n\n Regards,\n Expense Sharing App!",
        }

    def send_message(self):
        print("Sending Message Started: {datetime}".format(datetime=datetime.now()))
        participants = self.expense.participants

        _message = ""

        if self.expense.split_type == "Equal":
            _message = self.message["Equal"] 
        elif self.expense.split_type == "Exact":
            _message = self.message["Exact"] 

        # elif self.expense.split_type == "Percent":
        #     _message = self.message["Percent"] 

        try:
             for user in participants.all():
                send_mail(
                    self.subject,
                    _message.format(
                        participant_name=user.name,
                        expense_name=str(self.expense.name),
                        creator_name=str(self.expense.payer.name),
                        your_share=self.expense.shares.get(user.id)
                    ),
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )
                print("MSG sent to: {name}, email: {email}".format(name=user.name, email=user.email))

        except Exception as e:
            print(e)


        # Stop JOB
        self.job_id.remove()

        # Shutdown scheduler
        self.scheduler.shutdown()
        print("Sending Message Ended: {datetime}".format(datetime=datetime.now())) 

    def start(self):
        try:
            self.job_id = self.scheduler.add_job(self.send_message)  
            self.scheduler.start()
        except Exception as e:
            print("ERROR: ", e)
