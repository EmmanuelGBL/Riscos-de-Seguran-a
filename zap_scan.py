# zap_scan.py
from zapv2 import ZAPv2
import time

target = "http://127.0.0.1:5000"  # ajuste se seu app rodar em outro lugar
zap = ZAPv2(
    apikey="",
    proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
)

print("Acessando alvo:", target)
zap.urlopen(target)
time.sleep(2)

print("Iniciando spider...")
scanid = zap.spider.scan(target)
time.sleep(2)
while int(zap.spider.status(scanid)) < 100:
    print("Spider {}%".format(zap.spider.status(scanid)))
    time.sleep(1)
print("Spider completo")

print("Iniciando active scan...")
ascan_id = zap.ascan.scan(target)
while int(zap.ascan.status(ascan_id)) < 100:
    print("Active scan {}%".format(zap.ascan.status(ascan_id)))
    time.sleep(5)
print("Active scan completo")

print("Gerando relatório HTML...")
report = zap.core.htmlreport()
with open("zap_report.html", "w", encoding="utf-8") as f:
    f.write(report)
print("Relatório salvo: zap_report.html")
