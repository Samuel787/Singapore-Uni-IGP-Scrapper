from bs4 import BeautifulSoup
import requests

def nus_scrap_data():
    source = requests.get("http://www.nus.edu.sg/oam/undergraduate-programmes/indicative-grade-profile-(igp)").text
    soup = BeautifulSoup(source, 'lxml')

    soup = soup.find('table')

    print("------------ start NUS report ------------------")

    result = []
    count = 0
    for row in soup.find_all('tr'):
        #get rid of the table header
        if count < 2:
            count += 1
            continue    

        erase = False
        for x in row.find_all('td'):
            if "colspan" in x.attrs:
                erase = True
    
        if erase == True:
            continue
    
        iterator = 0
        for data in row.find_all('td'):
            if iterator == 0:
                course = data.text
                iterator = 1
            elif iterator == 1:
                tenth = data.text
                iterator = 2
            else:
                hundredth = data.text
                iterator = 0
        result.append([course.strip('\n'), tenth.strip('\n'), hundredth.strip('\n')])

    print(result)
    print("------------ end report ------------------")

nus_scrap_data()