import csv
import os

TOTAL_FIELDS = 24
TITLE_FIRST_FIELD = 'NOMBRE DE MARCA'
OK = 'OK'
# Categories
FOOTWEAR_EU = 'FOOTWEAR - EU'
FOOTWEAR_US = 'FOOTWEAR - US'
APPAREL = 'APPAREL'
ACCESSORIES = 'ACCESSORIES'
ALL_CATEGORIES = [FOOTWEAR_EU, FOOTWEAR_US, APPAREL, ACCESSORIES]

def getSizesFromCategory(category):
    map_categories_and_sizes = {}
    map_categories_and_sizes[FOOTWEAR_EU] = [
        "19","20","21","22","23","24","25","26","27","28","29",
        "30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47"
    ]
    map_categories_and_sizes[FOOTWEAR_US] = [
        "1","1.5","2","2.5","3","3.5","4","4.5","5","5.5","6","6.5","7","7.5",
        "8","8.5","9","9.5","10","10.5","11","11.5","12","12.5","13","13.5"
    ]
    map_categories_and_sizes[APPAREL] = [
        "OS","XSS","XXS","XS","S","S/M","M","M/L","L","L/XL","XL","XXL","3XL","4XL","RH","LH",
        "1X","2X","3X","4X","5X","00","000","14","16","18","38B","38C","38D","68","74","80",
        "86","92","98","2832","3030","3032","3232","3432","3632","3832","4032","SHT","OSSHT",
        "XXSSHT","XSSHT","SSHT","MSHT","LSHT","XLSHT","XXLSHT","SHTRH","SHTLH","1XSHT","2XSHT",
        "3XSHT","00XSHT","000SHT","2SHT","4SHT","6SHT","8SHT","10SHT","12SHT","14SHT","16SHT",
        "18SHT","20SHT","28SHT","29SHT","30SHT","31SHT","32SHT","33SHT","34SHT","35SHT","36SHT",
        "38SHT","40SHT","REG","OSREG","XXSREG","XSREG","SREG","MREG","LREG","XLREG","XXLREG","REGRH",
        "REGLH","1XREG","2XREG","3XREG","00XREG","000REG","2REG","4REG","6REG","8REG",
        "10REG","12REG","1"
    ]
    map_categories_and_sizes[ACCESSORIES] = ["N/A"]
    return map_categories_and_sizes.get(category.upper()) #lista de sizes

def areFieldsOk(line, line_number, brand, offer):
    isOk = True
    error_message = 'linea: ' + str(line_number) + ' ERROR: '
    if line[2] == '': # 'Codigo de Color'
        error_message += 'falta Codigo de Color, '
        isOk = False
    if line[3] == '': # 'Nombre'
        error_message += 'falta Nombre, '
        isOk = False
    if line[4] == '': # 'Descripcion de Color'
        error_message += 'falta Descripcion de Color, '
        isOk = False
    if line[6].upper() not in ALL_CATEGORIES: # 'Size Category'
        error_message += 'Size Category no existe'
        isOk = False
    if line[14] == '': # 'Estilo'
        error_message += 'falta Estilo, '
        isOk = False
    if line_number > 2:
        if line[0] != brand:
            error_message += 'La marca no coincide con la primer fila, '
            isOk = False
        if line[1] != offer:
            error_message += 'La oferta no coincide con la primer fila'
            isOk = False
    if isOk:
        return OK
    return error_message

def writeLineWithSize(csv_writer, line):
    curva = line[7]
    size = line[5]
    category = line[6]
    isNeedToAddSize = curva == '' and size == '' and category.upper() in ALL_CATEGORIES
    if isNeedToAddSize:
        sizeList = getSizesFromCategory(category)
        for sizeName in sizeList:
            line[5] = sizeName
            csv_writer.writerow(line)
    else:
        csv_writer.writerow(line)


def procesarCSV(fileName):
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    def is_binary_string(bytes): return bool(bytes.translate(None, textchars))
    if is_binary_string(open(fileName, 'rb').read(1024)):
        return ['ERROR: El archivo no es del tipo esperado']
    with open(fileName, 'r') as fileToClean:
        readerObj = list(csv.reader(fileToClean))
    newName = fileName + "_CLEAN.csv"
    errors = []
    if len(readerObj) < 2:
        return ['ERROR: El archivo no tiene líneas para procesar']
    with open(newName, 'w') as fileToWrite:
        csv_writer = csv.writer(fileToWrite, delimiter=',')
        line_number = 1
        brand_name = ''
        offer_name = ''
        for line in readerObj:
            if line_number == 1:
                if len(line) != 24 and line[0] != TITLE_FIRST_FIELD:
                    return ['ERROR: El formato del archivo no es el esperado']
                msg_error = OK
            elif line_number == 2:
                brand_name = line[0] # 'Nombre de Marca'
                offer_name = line[1] # 'Oferta'
                msg_error = areFieldsOk(line, line_number, brand_name, offer_name)
            else:
                msg_error = areFieldsOk(line, line_number, brand_name, offer_name)
            if msg_error == OK:
                writeLineWithSize(csv_writer, line)
            else:
                line.insert(0, msg_error)
                errors.append(line)
            line_number += 1
    os.remove(fileName)
    os.rename(newName, fileName)
    errors.insert(0,'OK')
    return errors
                



