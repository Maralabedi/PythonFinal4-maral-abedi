import csv
import os
from datetime import datetime

def export_to_csv(students):
    os.makedirs("exports", exist_ok=True)
    filename = f"exports/نمرات_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["آیدی","نام","نام‌خانوادگی","سن","ریاضی","انگلیسی","برنامه‌نویسی","دینی","عربی","فیزیک","شیمی","زیست","معدل"])
        for s in students:
            g = [s['math'],s['english'],s['programming'],s['religion'],s['arabic'],s['physics'],s['chemistry'],s['biology']]
            avg = round(sum(x for x in g if x>0)/len([x for x in g if x>0]),2) if any(g) else 0
            w.writerow([s['id'],s['first_name'],s['last_name'],s['age'],*g,avg])
    os.startfile(filename)

def generate_report(student):
    g = [student['math'],student['english'],student['programming'],student['religion'],
         student['arabic'],student['physics'],student['chemistry'],student['biology']]
    avg = round(sum(x for x in g if x>0)/len([x for x in g if x>0]),2) if any(g) else 0

    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>کارنامه</title>
<style>body{{font-family:Tahoma;background:linear-gradient(135deg,#667eea,#764ba2);padding:50px;}}
.card{{max-width:900px;margin:auto;background:#fff;color:#000;border-radius:25px;padding:40px;box-shadow:0 20px 40px rgba(0,0,0,0.5);}}
table{{width:100%;border-collapse:collapse;margin:30px 0;}}
th,td{{padding:15px;text-align:center;border-bottom:1px solid #eee;}}
.avg{{font-size:48px;color:#4CAF50;font-weight:bold;text-align:center;margin:40px;}}</style></head>
<body><div class="card">
<h1 style="text-align:center;color:#4CAF50;">کارنامه تحصیلی</h1>
<h2 style="text-align:center;">{student['first_name']} {student['last_name']}</h2>
<table>
<tr><th>درس</th><th>نمره</th></tr>
<tr><td>ریاضی</td><td><b>{g[0]:.1f}</b></td></tr>
<tr><td>انگلیسی</td><td><b>{g[1]:.1f}</b></td></tr>
<tr><td>برنامه‌نویسی</td><td><b>{g[2]:.1f}</b></td></tr>
<tr><td>دینی</td><td><b>{g[3]:.1f}</b></td></tr>
<tr><td>عربی</td><td><b>{g[4]:.1f}</b></td></tr>
<tr><td>فیزیک</td><td><b>{g[5]:.1f}</b></td></tr>
<tr><td>شیمی</td><td><b>{g[6]:.1f}</b></td></tr>
<tr><td>زیست</td><td><b>{g[7]:.1f}</b></td></tr>
</table>
<div class="avg">معدل: {avg:.2f}</div>
<p style="text-align:center;color:#555;">{datetime.now().strftime('%Y/%m/%d')}</p>
</div></body></html>"""

    filename = f"exports/کارنامه_{student['first_name']}_{student['last_name']}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    os.startfile(filename)