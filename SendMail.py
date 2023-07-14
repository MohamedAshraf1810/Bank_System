from email.message import EmailMessage
import ssl
import smtplib
import random
import random
from datetime import datetime
from email.utils import formataddr


nowD_T = datetime.now()
dt_string = nowD_T.strftime("%d/%m/%Y %H:%M:%S")

def Num_rand():
    # Generate a random six-digit number
    random_number = random.randint(100000, 999999)
    return random_number


def send_Mail(receiver,name):
    
    OTPRAND = Num_rand()
    email_sender =   '#### #### #### ####' # E-mail address
    email_password = '#### #### #### ####' # E-mail Password
    email_receiver = receiver

    subject = 'Voice Authentication OTP'

    body = f""" 
    Dear [{name}],

    I hope this email finds you well. 
    In response to your request for an OTP to pass the 
    voice recognition process, I am pleased to provide 
    you with the required information. 
    OTP that you can use to gain access,

    OTP: {OTPRAND}

    To ensure the security of your account, please 
    remember to keep this OTP confidential and do 
    not share it with anyone. Once you receive 
    the OTP, please follow the voice recognition 
    prompts and enter the provided OTP when 
    prompted. 
    This will allow you to successfully 
    pass the voice recognition process and access 
    your account.

    If you encounter any difficulties or have any 
    further questions, please don't hesitate to reach 
    out to our support team. We are here to assist 
    you in any way we can.

    We appreciate your cooperation and understanding 
    in maintaining the security of your personal 
    information.

    ***************************************
    * Please Dont Reply to this Message *
    ***************************************
    
    Best regards,
    Administrator
    MAS BANK
    {dt_string}
    """
    em = EmailMessage()
    em['From'] = formataddr(('MAS BANK', email_sender))
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465 , context=context) as smtp:
        smtp.login(email_sender , email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

    print("Email Sent !")
    return (OTPRAND)