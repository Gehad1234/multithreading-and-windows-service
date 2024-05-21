import os
import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time


# Function to collect workload data and save it to a text file
def collect_and_save_data(file_path):
    with open(file_path, 'w') as f:
        # Collect data
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        # Save data to the file
        f.write(f"CPU consuming percentage: {cpu_percent}%\n")
        f.write(f"Memory consuming percentage: {memory_percent}%\n")
        f.write(f"Hard disk consuming percentage: {disk_usage}%\n")
        f.write(f"Network consuming percentage: {network_usage} bytes\n")


# Function to send email with attached file
def send_email(sender_email, sender_password, receiver_email, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "PC Workload Data"

    # Attach file
    with open(attachment_path, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
    msg.attach(attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


# Main function
def main():
    # Paths and email configuration
    file_path = "workload_data.txt"
    sender_email = "gehadabdellah86@gmail.com"
    sender_password = "Gerry@2020"
    receiver_email = "gehad.abdellah@ejust.edu.eg"

    # Run indefinitely
    while True:
        # Collect and save data
        collect_and_save_data(file_path)

        # Send email every 12 hours
        send_email(sender_email, sender_password, receiver_email, file_path)

        # Wait for 12 hours
        time.sleep(12 * 60 * 60)


if __name__ == "__main__":
    main()
