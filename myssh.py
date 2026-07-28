import sys
import getpass
import paramiko
import time


def ssh_connect(username, ip):

    password = getpass.getpass("Passwort: ")

    print(f"Verbinde mit {username}@{ip} ...")


    client = paramiko.SSHClient()

    # unbekannte SSH-Server akzeptieren
    client.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )


    try:

        # eigene SSH-Verbindung über Paramiko
        client.connect(
            hostname=ip,
            port=22,
            username=username,
            password=password
        )


        print("SSH Verbindung erfolgreich!")
        print("")


        # interaktive Shell öffnen
        channel = client.invoke_shell()


        time.sleep(1)


        # Begrüßung / Prompt anzeigen
        while channel.recv_ready():
            output = channel.recv(4096).decode()
            print(output, end="")


        # eigene Kommando-Schleife
        while True:

            command = input()


            if command == "exit":
                print("Verbindung wird geschlossen...")
                break


            channel.send(command + "\n")


            time.sleep(0.5)


            while channel.recv_ready():

                output = channel.recv(4096).decode()
                print(output, end="")


    except paramiko.AuthenticationException:
        print("Fehler: Benutzername oder Passwort falsch.")


    except paramiko.SSHException as e:
        print("SSH Fehler:")
        print(e)


    except Exception as e:
        print("Fehler:")
        print(e)


    finally:
        client.close()



def main():

    # Argumente prüfen
    if len(sys.argv) != 4:

        print("Benutzung:")
        print("myssh ssh-connect <username> <ip>")
        print()

        print("Beispiel IPv4:")
        print("myssh ssh-connect maher ipv4")

        print()

        print("Beispiel IPv6:")
        print(
            "myssh ssh-connect maher ipv6"
        )

        sys.exit(1)



    command = sys.argv[1]
    username = sys.argv[2]
    ip = sys.argv[3]


    if command != "ssh-connect":

        print("Unbekannter Befehl:", command)
        sys.exit(1)



    ssh_connect(username, ip)



if __name__ == "__main__":
    main()