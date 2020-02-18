from bs4 import BeautifulSoup
import requests
import xlsxwriter

year = "2020"

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
    return result

def write_nus(result):
    #create file (workbook) and worksheet   
    outWorkbook = xlsxwriter.Workbook("nus_igp"+year+".xlsx")
    outSheet = outWorkbook.add_worksheet()

    #write headers
    outSheet.write(0,0, "Course name")
    outSheet.write(0,1, "90th")
    outSheet.write(0,2, "10th")

    row = 1
    pos = 0
    for x in result:
        for y in x:
            pos = pos % 3
            outSheet.write(row, pos, y)
            pos += 1
        row += 1
    
    outWorkbook.close()

result = nus_scrap_data()
write_nus(result)