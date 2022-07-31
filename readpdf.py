import re
import pdfplumber
import string
from collections import defaultdict
r = re.compile("\n([\w-]+ \d+).*?\n.*?(\(\d\d:\d\d\)[\w\W\n]+?\(\d\d:\d\d\)).*?\n")


def alphafilter(s):
    r = []
    for i in s:
        if i.isalpha() or i == ' ':
            r.append(i)
    return ''.join(r)


results = []
pleaseadd = True
with pdfplumber.open('/Users/onion/Downloads/db.pdf') as pdf:
    for x in pdf.pages:
        foundroutes = r.findall(x.extract_text())
        for route in foundroutes:
            trainname = route[0]
            stops = [alphafilter(s).strip() for s in route[1].split('-')]
            for stop in stops:
                if len(stop) > 50:
                    pleaseadd = False
            if pleaseadd:
                results.append((trainname, stops))
            pleaseadd = True

allstops = defaultdict(list)
for train in results:
    name = train[0]
    for stop in train[1]:
        allstops[stop].append(name)
# [('EC 86', '(13:50)- Verona Porta Nuova - Bolzano / Bozen - (Brennero/Brenner (17:48/18:00)) -\nInnsbruck (18:36/18:40) - (Kufstein (19:24/19:26)) - München (20:25)')]





"""
672 Druckzeitraum : 01.04.2019 - 10.06.2019
ICE-T 1630
ICE-T 1630 (Ber
(Berlin-Rummelsburg (Triebzuganlage)) - Berlin-Gesundbrunnen (12:54)- Berlin - Berlin Südkreuz - Halle
(Saale) - Erfurt - Frankfurt (Main) (16:56)
Bln-Rummels Tanl - Frankfurt(M), Mi+Fr+So 24.V.-07.VI., auch 05., 07., 30.IV., 10.VI., nicht 31.V., 05.VI.
Bln-Rummels Tanl - Frankfurt(M), Fr+So 12.IV.-19.V., auch 18., 22.IV., nicht 19., 21.IV.
Tfz1:411 Hg230 0t BrH193 318m EB a (WC); )p(
+ Tfz1:411 Hg230 0t BrH193 185m EB a (WC); )p(
Œ; ­
7
Apmzf 28 F7 310 1690 BRGBT FF 1635
ABpmz 27 78430 78679
WRmz 26
06 Bpmdz 24
Bpmz 23
Bpmbz 22
Bpmzf 21
70
06) Fahrradstellplätze buchbar ab 1. April
ICE-T 1631
ICE-T 1631 <b>
Frankfurt (Main) (15:02)- Erfurt - Halle (Saale) - Berlin Südkreuz - Berlin - Berlin-Gesundbrunnen (19:10)-
(Berlin-Rummelsburg (Triebzuganlage))
Frankfurt(M) - Bln-Rummels Tanl, tgl. 01.-07.IV., 20.V.-10.VI.
Frankfurt(M) - Bln-Rummels Tanl, tgl. 08.IV.-19.V.
FF Tfz1:411 Hg230 0t BrH193 318m EB a (WC); )p(
Reisendensicherung gemäß Richtlinie 419.3312 (siehe Anhang Xb)
Œ; ­
7
Bpmzf 31 F5 311 a) 78674 FF BRGBT 78434
Bpmbz 32 1627 1695
Bpmz 33 1697
Bpmkz 37
Apmzf 38
Bpmzf 21 F7 310 1636 FF BRGBT 1701
Bpmbz 22 1634 1197
Bpmz 23 78471
06 Bpmdz 24 1691
WRmz 26 78444
ABpmz 27 92736
Apmzf 28
71
06) Fahrradstellplätze buchbar ab 1. April a) Fr auch 18., 30.IV., 29.V., nicht 19.IV.
2019_ZpAR Wi_B2






Output for each page:
[('ICE-T 1630', '(12:54)- Berlin - Berlin Südkreuz - Halle\n(Saale) - Erfurt - Frankfurt (Main) (16:56)'), ('ICE-T 1631', '(15:02)- Erfurt - Halle (Saale) - Berlin Südkreuz - Berlin - Berlin-Gesundbrunnen (19:10)')]
RRRR[0]
('ICE-T 1630', '(12:54)- Berlin - Berlin Südkreuz - Halle\n(Saale) - Erfurt - Frankfurt (Main) (16:56)')
RRRR[1]
('ICE-T 1631', '(15:02)- Erfurt - Halle (Saale) - Berlin Südkreuz - Berlin - Berlin-Gesundbrunnen (19:10)')
"""