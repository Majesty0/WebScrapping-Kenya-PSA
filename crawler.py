import requests,pandas as pd
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate,Table


URLS=["https://www.gov.ke/","https://www.eacc.go.ke/","https://www.iebc.or.ke/"]
KEYWORDS=["verify","register","report","public","notice","deadline","warning","citizen"]
def run():
    rows=[]
    for u in URLS:
        try:
            r=requests.get(u,timeout=20,headers={"User-Agent":"Mozilla/5.0"})
            s=BeautifulSoup(r.text,"lxml")
            text=" ".join(p.get_text(" ",strip=True) for p in s.find_all("p"))
            if sum(k in text.lower() for k in KEYWORDS)>=2:
                rows.append({"URL":u,"Title":s.title.text if s.title else "","Text":text[:2000]})
        except Exception as e:
            print(e)
    df=pd.DataFrame(rows)
    df.to_excel("Governance_PSA.xlsx",index=False)
    pdf=SimpleDocTemplate("Governance_PSA_Report.pdf")
    data=[list(df.columns)]+df.values.tolist() if not df.empty else [["No data"]]
    pdf.build([Table(data)])
    print(df)
