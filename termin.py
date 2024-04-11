import requests
import logging
import bs4
import enum

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    

def number_to_month(number):
    month_dict = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    
    return month_dict.get(number, "Invalid Month")

def aachen_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_0 = 'https://termine.staedteregion-aachen.de/auslaenderamt/'
    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    url_2 = 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=86&select_cnc=1&cnc-270=0&cnc-271=0&cnc-264=1&cnc-267=0&cnc-268=0&cnc-272=0&cnc-255=0&cnc-269=0&cnc-262=0&cnc-256=0&cnc-253=0&cnc-254=0&cnc-274=0&cnc-252=0&cnc-258=0&cnc-257=0&cnc-260=0&cnc-263=0&cnc-259=0&cnc-249=0&cnc-250=0&cnc-261=0&cnc-266=0&cnc-265=0'    
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_0 = session.get(url_0)
    res_1 = session.get(url_1)
    res_2 = session.get(url_2)
    payload = {'loc':'38', 'gps_lat': '50.768703', 'gps_long': '6.091849', 'select_location': 'Ausländeramt Aachen, 2. Etage auswählen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            logging.info(f'{"Appointment available now at Ausländeramt!"}')
            h3 = div.find_all("h3")
            res = 'New appointments are available now!\n'
            for h in h3:
                res += h.text + '\n'             
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'{"Appointment available now at Ausländeramt!"}')
            logging.info(f'{summary_text}')
            return True, 'New appointments are available now!\n' + summary_text
        else:
            logging.info(f'{"Cannot find sugg_accordion! Possible new appointments are available now at Ausländeramt!"}')                
            return True, "Cannot find sugg_accordion! Possible new appointments are available now!"
    else:
        logging.info(f'{"No appointment is available at Ausländeramt."}')                
        return False, "No appointment is available at Ausländeramt"    

aachen_termin()
