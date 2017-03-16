import datetime
import time
import bs4
import requests
import smtplib
import sqlite3
with requests.session() as c:

   
    emailAddress = ""
    password = ""
    sendTo = "@vtext.com"
    sleeptime = 20
    zip = 85295
    
    sqliteFile = 'SwitchData.sqlite'
    
    conn = sqlite3.connect(sqliteFile)
    conn.execute('''
	CREATE TABLE IF NOT EXISTS switchStock(
		Grey TEXT,
		Neon TEXT,
		Timestamp TEXT
    	);
    ''')
    
    conn.close()
	
    print("Searching in zip code: "+ str(zip) + '\n')
    neon = "Neon - No Stock"
    gray = "Gray - No Stock"
    url = "https://primenow.amazon.com/"
    c.get(url)
    login_data = dict(newPostalCode = zip);
    c.post(url, data=login_data, headers = {'User-agent': 'Mozilla/5.0'})
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(emailAddress, password)
    msg = "Battle Star ONLINE"
    server.sendmail(emailAddress, sendTo, msg)
    server.quit()
    
    counter = 0
    
    while(True):
        
        if counter == 180:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(emailAddress, password)
            msg = "Health Check- System Online"
            server.sendmail(emailAddress, sendTo, msg)
            server.quit()
            counter = 0
        else:
            counter = counter + 1
            
            
        page = c.get("https://primenow.amazon.com/search?k=nintendo+switch&p_95=&merchantId=&ref_=pn_gw_nav_ALL", headers = {'User-agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(page.text, "html5lib")
        filtered = soup.findAll("p", {"class": "asin__details__title"})
        for item in filtered:
            print(item.text.strip())
            if(item.text.strip() == "Nintendo Switch with Neon Blue and Neon Red Joy-Con"):
                neon = "Neon - IN STOCK!"
                break
            neon = "Neon - No Stock"
        for item in filtered:
            if (item.text.strip() == "Nintendo Switch with Gray Joy-Con"):
                gray = "Gray - IN STOCK!"
                break
            gray = "Gray - No Stock"

        if (neon == "Neon - IN STOCK!" or gray == "Gray - IN STOCK!"):
            #logic for stuff
            print("THERE IS ONE ")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(emailAddress, password)
            msg = "THERE IS ONE go to \nhttps://primenow.amazon.com/search?k=nintendo+switch&p_95=&merchantId=&ref_=pn_gw_nav_ALL/"
            server.sendmail(emailAddress, sendTo, msg)
            server.quit()
            
        
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        print(st + "\n" + neon + "\n" + gray + "\n")
        
        conn = sqlite3.connect(sqliteFile)
        data = [(gray, neon, st)]
        conn.executemany("INSERT INTO switchStock VALUES(?,?, ?)", data)
        conn.commit()
        conn.close()
        
        time.sleep(int(sleeptime))
        
