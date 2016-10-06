import smtplib

addr = "mepla.photography@gmail.com"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(addr, "XT2forthewin")

msg = "Salam"
server.sendmail(addr, 'soheil.nasirian@gmail.com', msg)
server.quit()