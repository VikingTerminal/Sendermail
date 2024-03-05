import smtplib
from email.mime.text import MIMEText
from getpass import getpass
import re
from colorama import Fore, Style, init
import time

init(autoreset=True)

def welcome_message():
    print(Fore.MAGENTA + "Benvenuto in questo tool. Visita https://github.com/VikingTerminal per provare altre utility" + Style.RESET_ALL)
    time.sleep(2)  

def colored_input(prompt, color=Fore.YELLOW):
    return input(color + prompt + Style.RESET_ALL)

def is_valid_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_regex, email))

def get_email_input(prompt):
    while True:
        email_input = colored_input(prompt)
        if is_valid_email(email_input):
            return email_input
        else:
            print(Fore.RED + "Errore: Inserisci un indirizzo email valido." + Style.RESET_ALL)

def get_smtp_server():
    while True:
        smtp_server = colored_input("Inserisci il server SMTP (es. smtp.gmail.com): ")
        if smtp_server:
            return smtp_server
        else:
            print(Fore.RED + "Errore: Il campo non può essere vuoto. Riprova." + Style.RESET_ALL)

def get_smtp_port():
    while True:
        try:
            smtp_port = int(colored_input("Inserisci la porta SMTP (solitamente 587 per TLS): "))
            if 1 <= smtp_port <= 65535:
                return smtp_port
            else:
                print(Fore.RED + "Errore: Inserisci una porta valida." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Errore: Inserisci un numero valido." + Style.RESET_ALL)

def send_email():
    smtp_server = get_smtp_server()
    smtp_port = get_smtp_port()
    sender_email = get_email_input("Inserisci il tuo indirizzo email: ")
    recipient_email = get_email_input("Inserisci l'indirizzo email del destinatario: ")
    subject = colored_input("Inserisci l'oggetto dell'email: ", Fore.CYAN)
    body = colored_input("Inserisci il corpo dell'email: ", Fore.CYAN)

    while True:
        use_app_password = colored_input("Vuoi utilizzare una password dell'app? (sì/no): ", Fore.CYAN).lower()
        if use_app_password in ["sì", "no"]:
            break
        else:
            print(Fore.RED + "Errore: Rispondi con 'sì' o 'no'." + Style.RESET_ALL)

    app_password = None
    if use_app_password == "sì":
        app_password = getpass(colored_input("Inserisci la tua password dell'app: ", Fore.CYAN))

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()

            if app_password:
                server.login(sender_email, app_password)

            server.sendmail(sender_email, recipient_email, message.as_string())

        print(Fore.GREEN + "Email inviata con successo!" + Style.RESET_ALL)

    except smtplib.SMTPAuthenticationError:
        print(Fore.RED + "Errore di autenticazione: Verifica l'indirizzo email e la password dell'app." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Errore durante l'invio dell'email: {e}" + Style.RESET_ALL)

welcome_message()
send_email()
