from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL de la página a la que queremos acceder
url1 = 'https://co.computrabajo.com/trabajo-de-desarrollador'

# Iniciamos el navegador (Chrome en este caso)
driver = webdriver.Chrome()
driver.get(url1)

# Espera explícita de 10 segundos para que la página cargue completamente
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))

# Inicializamos listas para almacenar nombres de empresas y títulos de trabajos
companies = []
job_titles = []

# Bucle de paginación
for i in range(1, 17):  # Cambia 17 por el número total de páginas que deseas recorrer
    # print(f"Página {i}")

    # Obtener todos los artículos de ofertas de trabajo
    job_offers = driver.find_elements(By.CLASS_NAME, 'box_offer')
    # print(f"Se encontraron {len(job_offers)} ofertas de trabajo en la página.")

    for offer in job_offers:
        try:
            # Encontramos el nombre de la empresa dentro de cada oferta
            company = offer.find_element(By.CSS_SELECTOR, 'a.fc_base.t_ellipsis').text
            companies.append(company)

            # Encontramos el puesto de trabajo dentro de cada oferta
            job_title = offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').text
            job_titles.append(job_title)

            # print(f"Empresa: {company} - Puesto: {job_title}")  # Imprimir el nombre de la empresa y el puesto de trabajo
        except Exception as e:
            # print(f"Error al obtener datos de la oferta: {e}")
            pass

    # Intentamos buscar el botón "Siguiente"
    try:
        # print("Buscando el botón 'Siguiente'...")
        next_button = driver.find_element(By.XPATH, '//span[@title="Siguiente"]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # Espera a que cargue la nueva página
    except Exception as e:
        # print(f"No se encontró el botón 'Siguiente' o se produjo un error: {e}")
        break  # Salimos del bucle si no hay más páginas

# Convertir a DataFrame
companyfinal = pd.DataFrame(companies, columns=['Company'])
titlefinal = pd.DataFrame(job_titles, columns=['Title'])
final = companyfinal.join(titlefinal)

# Imprimir resultados finales
print(final)

# Cerrar el navegador al finalizar
driver.quit()
