import requests
from typing import Final
import logging
import bs4

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

"""
User agent string for looking for Termine.    
"""
USER_AGENT_STRING: Final = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)


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


def get_hbf_url(res_1, team_name):    
    soup = bs4.BeautifulSoup(res_1.content, 'html.parser')         
    header_element = soup.find('h3', string=lambda s: 'Aufenthalt' in s if s else False)
    url_2 = ''
    li_index = int(team_name.split(' ')[-1]) - 1
    if header_element:        
        next_sibling = header_element.find_next_sibling()
        if next_sibling:
            li_elements = next_sibling.find_all('li')
            cnc_id = li_elements[li_index].get('id').split('-')[-1] if li_elements else None
            url_2 = f'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=89&select_cnc=1&cnc-{cnc_id}=1'
            logging.info(f"Aufenthalt {team_name} cnc id: {cnc_id}")
    else:
        logging.info("Element containing 'Aufenthalt' not found.")        

    return url_2

def aachen_hbf_termin():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"    
    headers = {"User-Agent": user_agent}
    session = requests.Session()
    session.headers.update(headers)

    url_1 = 'https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1'
    url_2 = 'https://termine.staedteregion-aachen.de/auslaenderamt/location?mdt=95&select_cnc=1&cnc-341=1&cnc-361=0&cnc-372=0&cnc-373=0&cnc-359=0&cnc-353=0&cnc-367=0&cnc-342=0&cnc-368=0&cnc-345=0&cnc-344=0&cnc-347=0&cnc-350=0&cnc-346=0&cnc-338=0&cnc-339=0&cnc-354=0&cnc-355=0&cnc-362=0&cnc-358=0'    
    url_3 = 'https://termine.staedteregion-aachen.de/auslaenderamt/suggest'
    res_1 = session.get(url_1)

    #url_2 = get_hbf_url(res_1, team_name)

    res_2 = session.get(url_2)
    soup = bs4.BeautifulSoup(res_2.content, 'html.parser')  #type: ignore
    loc = soup.find('input', {'name': 'loc'}).get('value')  #type: ignore
    logging.info(f"Aufenthalt loc: {loc}")

    payload = {'loc':str(loc), 'gps_lat': '50.770786', 'gps_long': '6.118778', 'select_location': 'Ausländeramt Aachen - Aachen Arkaden, Trierer Straße 1, Aachen'}
    res_3 = session.post(url_2, data=payload)
    res_4 = session.get(url_3)
    
    if "Kein freier Termin verfügbar" not in res_4.text:        
        
        # get exact termin date
        soup = bs4.BeautifulSoup(res_4.text, 'html.parser')
        div = soup.find("div", {"id": "sugg_accordion"})
        summary_tag = soup.find('summary', id='suggest_details_summary')
        
        if div:
            h3 = div.find_all("h3")
            res = ''
            for h in h3:
                res += h.text + '\n'             
            logging.info(res[:-1])
            return True, res[:-1]
        elif summary_tag:
            summary_text = summary_tag.get_text(strip=True)
            logging.info(f'Appointment available now at HBF')
            logging.info(f'{summary_text}')
            return True, summary_text
        else:
            logging.info(f'Cannot find sugg_accordion! Possible new appointments are available now at HBF')                
            return False, f"Cannot find sugg_accordion! Possible new appointments are available now at HBF"
    else:
        logging.info(f'No appointment is available at HBF.')                
        return False, f'No appointment is available at HBF.'   


# superc_termin(1)
# aachen_hbf_termin('Team 1')
# aachen_hbf_termin('Team 2')
# aachen_hbf_termin('Team 3')
# for key, value in hbf_url.items():
#     aachen_hbf_termin(key, value)
