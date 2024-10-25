from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
 
# Configurazione del logger
logging.basicConfig(level=logging.INFO)
 
# Percorso del driver di Chrome specifico
chrome_driver_path = r"C:\Users\pigro\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"
 
# Inizializzo il servizio con il percorso specifico del driver di Chrome
service = Service(chrome_driver_path)
 
# Inizializzo le opzioni del browser Chrome
options = Options()
options.add_experimental_option("detach", True)  #fix del crashh
 
# Avvio del driver di Chrome
driver = Chrome(service=service, options=options)
 
# Vai alla pagina di Amazon
driver.get("https://www.amazon.it/?tag=wwwbingcom07-21&ref=pd_sl_8nrp9peygk_e&adgrpid=1227055293731746&hvadid=76691120301091&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=1821&hvtargid=kwd-76691194887418:loc-93&hydadcr=10840_1834685&msclkid=bb314bc0081b135719c42cc4d7ac79d1")
 
time.sleep(2)

def accetta_cookie(driver):
    try:
        logging.info("SONO NEL accetta_cookie")
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".a-button-input.celwidget"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", cookie_button)
        cookie_button.click()
        logging.info("Cookie accettati con successo.")
    except TimeoutException:
        logging.error("Il bottone per accettare i cookie non è stato trovato o non è cliccabile.")
    except ElementClickInterceptedException:
        logging.error("Il click sul bottone dei cookie è stato bloccato.")
    except NoSuchElementException:
        logging.error("L'elemento non esiste.")
    except Exception as e:
        logging.error(f"Errore imprevisto: {str(e)}")

time.sleep(5)  


def rileva_testo(driver):
    global last_text
    try:


        logging.info("SONO NEL rileva_testo")

        input_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.nav-input.nav-progressive-attribute"))
        )

        while True:
            testo_inserito = input_element.get_attribute("value").strip()
            
            if testo_inserito != last_text:
                logging.info(f"Testo inserito nella casella di ricerca: {testo_inserito}")
                last_text = testo_inserito
                cerca_e_stampa_risultati(driver, last_text)

            time.sleep(0.5)

    except TimeoutException:
        logging.error("La casella di ricerca non è stata trovata o non è visibile.")
    except NoSuchElementException:
        logging.error("La casella di ricerca non è stata trovata.")
    except Exception as e:
        logging.error(f"Errore imprevisto: {str(e)}")


        ############################################################################

def cerca_e_stampa_risultati(driver):
    try:
        logging.info("SONO NEL cerca_e_stampa_risultati")
        termine_ricerca = input("Inserisci il termine di ricerca: ")
        input_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.nav-input.nav-progressive-attribute"))
        )
        input_element.clear()
        input_element.send_keys(termine_ricerca)
        input_element.send_keys(Keys.RETURN)

        time.sleep(5)
        titoli = driver.find_elements(By.CSS_SELECTOR, "span.a-size-base-plus.a-color-base.a-text-normal")
        valutazioni = driver.find_elements(By.CSS_SELECTOR, "i[data-cy='reviews-ratings-slot']")
        prezzi = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
        date = driver.find_elements(By.CSS_SELECTOR, "span.a-color-base.a-text-bold")

        if not titoli:
            logging.info("Nessun risultato trovato.")
            return

        for i in range(len(titoli)):
            titolo = titoli[i].text
            valutazione = valutazioni[i].text
            prezzo = prezzi[i].text
            data = date[i].text
            logging.info(f"Risultato {i + 1}: Titolo: {titolo}, Valutazione: {valutazione}, Prezzo: {prezzo}, Data: {data}")

    except TimeoutException:
        logging.error("I risultati della ricerca non sono stati trovati.")
    except Exception as e:
        logging.error(f"Errore imprevisto: {str(e)}")


###############################################################


accetta_cookie(driver)
time.sleep(5)  
rileva_testo(driver)

while True:
    cerca_e_stampa_risultati(driver)
    time.sleep(5)  
    break

time.sleep(2)
#cerca_e_stampa_risultati(driver)


driver.quit()      # Crash totale del browser  



# <input type="text" id="twotabsearchtextbox" 
# value="" name="field-keywords" autocomplete="off" 
# placeholder="Ricerca Amazon.it" 
# class="nav-input nav-progressive-attribute" dir="auto"
#  tabindex="0" aria-label="Ricerca Amazon.it" spellcheck="false">


# <span class="a-size-base-plus a-color-base a-text-normal">by Amazon Pasta di Grano Duro, Fusilli, 500g</span>

# <i data-cy="reviews-ratings-slot" aria-hidden="true" class="a-icon a-icon-star-small a-star-small-4-5"><span class="a-icon-alt">4,3 su 5 stelle</span></i>

# <span class="a-price-whole">0<span class="a-price-decimal">,</span></span>

# <span class="a-color-base a-text-bold">lun, 28 ott </span>