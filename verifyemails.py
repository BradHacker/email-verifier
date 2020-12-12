import socket
import time
import dns.resolver


SMTP_WAIT = 0
DEBUG = False


def getSmtpDomain(email: str) -> str:
    domain = email.split("@")[1]
    try:
        answers = dns.resolver.resolve(domain, "MX")
    except dns.resolver.NXDOMAIN:
        return ""
    best_answer = None
    for rdata in answers:
        if best_answer == None or rdata.preference < best_answer.preference:
            best_answer = rdata
        if DEBUG:
            print("Host", rdata.exchange, "has preference", rdata.preference)
    best_domain = ".".join(p.decode("utf-8") for p in best_answer.exchange[:-1])
    return best_domain


def send_msg(socket: socket.socket, msg: str) -> str:
    socket.sendall((msg + "\r\n").encode("utf-8"))
    data = socket.recv(1024)
    return data.decode("utf-8")


def main():
    with open("output.csv", "w") as out:
        with open("input.txt", "r") as file:
            curr_line = 0
            for email in file:
                curr_line += 1
                print(" | Checking email #" + str(curr_line), end="\r")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    best_domain = getSmtpDomain(email[:-1])
                    if best_domain == "":
                        out.write(email[:-1] + ",doesn't exist\n")
                        continue
                    s.connect((best_domain, 25))
                    s.recv(1024)
                    time.sleep(SMTP_WAIT)
                    helo = send_msg(s, "HELO gmail.com")
                    if DEBUG:
                        print(helo)
                    time.sleep(SMTP_WAIT)
                    main_from = send_msg(s, "MAIL FROM:<example@gmail.com>")
                    if DEBUG:
                        print(main_from)
                    time.sleep(SMTP_WAIT)
                    status = send_msg(s, "RCPT TO:<" + email[:-1] + ">")
                    if DEBUG:
                        print(status)
                    if status[:9] == "550-5.1.1":
                        out.write(email[:-1] + ",doesn't exist\n")
                    elif status[:9] == "250 2.1.5":
                        out.write(email[:-1] + ",exists\n")
                    else:
                        out.write(email[:-1] + ",can't verify\n")
                    send_msg(s, "quit\n")
                    s.close()
            print("\n all done!")


if __name__ == "__main__":
    main()
