import smtplib

def send_sms_via_smtp(phone_number, message, carrier):
    # Define the SMS gateway address based on the carrier
    sms_gateways = {
        "verizon": "{}@vtext.com",
        "att": "{}@txt.att.net",
        "tmobile": "{}@tmomail.net",
        "sprint": "{}@messaging.sprintpcs.com",
        # Add more carriers as needed
    }

    if carrier not in sms_gateways:
        raise ValueError("Unsupported carrier")

    # Replace these with your email server details
    smtp_server = "smtp.gmail.com"  # e.g., Gmail SMTP server
    smtp_port = 587
    email = "piyushkhannavb@gmail.com"  # Your email address
    password = "ymoercskkitgiyoc"  # Your email password

    # Construct the SMS gateway email address
    to_address = sms_gateways[carrier].format(phone_number)

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)

    # Send the SMS message
    server.sendmail(email, to_address, message)
    server.quit()

# Usage example
phone_number = "+918755122371"  # Recipient's phone number
message = "server#120.76.241.191#8005"
carrier = "verizon"  # Recipient's mobile carrier

send_sms_via_smtp(phone_number, message, carrier)
