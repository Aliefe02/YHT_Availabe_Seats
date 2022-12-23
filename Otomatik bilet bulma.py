from selenium import webdriver
import time
from scrapy import Selector
import re
import pyautogui
import pywhatkit

print("\n             ***IMPORTANT***\n**Login whatsapp web before starting program**\n\n")
departure_loc = input('Enter departure location > ')
arrival_loc = input('Enter arriving location > ')
departure_time = int(input('Enter departure time > '))
max_departure_time = int(input('Enter latest hour you want to depart > '))
departure_date = input('Enter departure date > ')
repeat_time = int(input('Enter repeat time in minutes > '))*60
phone_number = input("Enter phone number to send msg on whatsapp > ")

while True:
    try:
        web = webdriver.Chrome()
        web.get('https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf')

        time.sleep(2)

        departure_location = departure_loc
        destination_location = arrival_loc

        departure = web.find_element("xpath", '//*[@id="nereden"]')
        departure.send_keys(departure_location)

        destination = web.find_element("xpath", '//*[@id="nereye"]')
        destination.send_keys(destination_location)

        date = web.find_element("xpath", '//*[@id="trCalGid_input"]')
        date.clear()
        date.send_keys(departure_date)
        time.sleep(3)

        pyautogui.click(1348,1004)

        time.sleep(2)

        Search_button = web.find_element("xpath", '//*[@id="btnSeferSorgula"]/span')
        Search_button.click()

        time.sleep(5)

        html = web.page_source .encode('utf-8')  
        time.sleep(3)
        sel = Selector( text = html )
        
        web.close()

        flag = -1
        flag_2 = True

        time_info = sel.xpath('/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody//span/text()').extract()
        #print(time_info)
        arrival = []
        length = len(time_info)
        for i in range(1,length,5):
            if (int(time_info[i-1][:1])==0 and int(time_info[i][:1])==0) or int(time_info[i][:1])>0:
                arrival.append(int(time_info[i-1][:2]))
                if (int(time_info[i-1][:2]) >= departure_time) and flag_2:
                    flag = len(arrival)-1
                    flag_2 = False
        if len(arrival) == 0:
            continue

        # print(len(arrival))
        # print(arrival)

        info = sel.xpath('/html/body/div[3]/div[2]/div/div/div/div/form/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/table/tbody//label/text()').extract()
        #print(info)
        
        if 'gece' in info[0]:
            del info[0]

        seats = []
        n = len(arrival)*6+1
        for i in range(4,n,6):
            empty_seats = re.findall('\(\d+\)',info[i])
            #print(empty_seats)
            seats.append(int(empty_seats[0][1:-1]))
        #print(len(seats))
        #print(seats)

        print("\n**************************\n")
        count = 0
        available_seats = ''
        if flag > -1 :
            n = flag
            while n < len(seats):
                if seats[n]>2 and int(time_info[n*5][:2]) <= max_departure_time and int(time_info[n*5][:2]) >= departure_time:
                    #print(time_info[n*5]+"--"+time_info[(n+1)*5]+" Seats -> "+str(seats[n]))
                    available_seats = available_seats +'\n'+ (time_info[n*5]+"--"+time_info[(n*5)+1]+" Seats -> "+str(seats[n]))
                    n += 1
                    count += 1
                else:
                    n += 1
            print(available_seats)
            if count > 0:
                pywhatkit.sendwhatmsg_instantly(phone_number,available_seats,20,True,3)
        else:
            print("NO AVAILABLE TRAIN!")
        
        time.sleep(repeat_time)
    except:
        web.close()
        continue
            

