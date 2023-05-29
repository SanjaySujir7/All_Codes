
class DateTimeProcess:
    def __init__(self,Date_Time):
        self.Date_Time = Date_Time
        
    def Get(self):
        Date_Time = self.Date_Time
        
        Split = Date_Time.split()
        
        Date = Split[0]
        TIme = Split[1]
        
        Date_Split = Date.split('-')
        
        return f"{Date_Split[2]}-{Date_Split[1]}-{Date_Split[0]} {TIme}"
    
    def Get_Csv_Date(self):
        Date_Time = self.Date_Time
        
        Split = Date_Time.split()
        
        Date = Split[0]
        
        Date_Split = Date.split('-')
        
        return f"{Date_Split[2]}-{Date_Split[1]}-{Date_Split[0]}"
