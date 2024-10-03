from dateutil import parser
import time


# Função para formatar uma data  do formato ISO (yyyy-MM-ddTHH:mm:ssZ) para dd/MM/yyyy HH:mm:ss
def format_date(iso_date, date_format="%d/%m/%Y %H:%M:%S"):
    date = parser.isoparse(iso_date)
    
    return date.strftime(date_format)

# Função para calcular a diferença de tempo em horas
def calculate_time_difference_in_hours(start_time, end_time):
    start_time = time.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    end_time = time.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
    difference_in_seconds = time.mktime(end_time) - time.mktime(start_time)
    return difference_in_seconds / 3600