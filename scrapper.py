import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def get_data(crypto, num_days):
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=path")
    options.add_argument(r'--profile-directory=profile') 
    driver = webdriver.Chrome(service=Service(executable_path=r"chromedriver.exe"), options=options)

    driver.get(f"https://finance.yahoo.com/quote/{crypto}/history?p={crypto}")
      
    final_rows = []
    
    for i in range(1, num_days+1):
        row = []
        rows = driver.find_element(By.XPATH, value=f'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr[{i}]').text
        data = rows.split()
        row.append(' '.join(data[:3]) )
        for i in data[-6:]: row.append(i)  
        final_rows.append( row ) 

        
    keys = ( 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume')
    output = [dict(zip(keys, l)) for l in final_rows]

    output = json.loads(json.dumps(output, indent=4))
            
    driver.close()
    driver.quit()
    
    return output

    

    