import threading
from kivymd.app import MDApp
from kivymd.uix import Screen
from kivymd.uix.picker import MDThemePicker
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
import datetime
from datetime import timedelta, date
from kivy.properties import StringProperty
from kivymd.uix.datatables import MDDataTable
import pickle



class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class MainScreen(Screen):
    #card 1 Date Selection

    def on_save(self, instance, value,date_range):
        if len(date_range)==0:
            date_range.append(value)
        global initial_date,final_date
        initial_date=str(date_range[0])
        final_date=str(value)
        initial_date=datetime.datetime.strptime(initial_date,"%Y-%m-%d").strftime("%d/%m/%Y")
        final_date=datetime.datetime.strptime(final_date,"%Y-%m-%d").strftime("%d/%m/%Y")
        self.ids.Date_Label.text="{} - {}".format(str(initial_date),str(final_date))


    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    #card 2 Source card

    def Source_dropdown_items(self):
        source_menu_items = [
            {
                "viewclass": "IconListItem",
                "text": "Delhi",
                "icon":"airplane-takeoff",
                "on_release":lambda: self.source_menu_callback("Delhi")
            } ,
            {
                "viewclass": "IconListItem",
                "text": "Kolkata",
                "icon":"airplane-takeoff",
                "on_release":lambda: self.source_menu_callback("Kolkata")
            } ,
            {
                "viewclass": "IconListItem",
                "text": "Mumbai",
                "icon":"airplane-takeoff",
                "on_release":lambda: self.source_menu_callback("Mumbai")
            } ,
            {   
                "viewclass": "IconListItem",
                "text": "Chennai",
                "icon":"airplane-takeoff",
                "on_release":lambda: self.source_menu_callback("Chennai")
            }
        ]

        self.source_menu = MDDropdownMenu(
            caller=self.ids.source_button,
            items=source_menu_items,
            width_mult=3,
            max_height=200,
        )
        self.source_menu.open()
    
    def source_menu_callback(self, text_item):
        global source_text
        self.source_text=text_item
        self.ids.source_button.text=text_item
        self.source_menu.dismiss()

    #card 3 Destination card

    def Destination_dropdown_items(self):
        Destination_menu_items = [
            {
                "viewclass": "IconListItem",
                "text": "Cochin",
                "icon":"airplane-landing",
                "on_release":lambda: self.destination_menu_callback("Cochin")
            } ,
            {
                "viewclass": "IconListItem",
                "text": "Delhi",
                "icon":"airplane-landing",
                "on_release":lambda: self.destination_menu_callback("Delhi")
            } ,
            {
                "viewclass": "IconListItem",
                "text": "New Delhi",
                "icon":"airplane-landing",
                "on_release":lambda: self.destination_menu_callback("New Delhi")
            } ,
            {   
                "viewclass": "IconListItem",
                "text": "Hyderabad",
                "icon":"airplane-landing",
                "on_release":lambda: self.destination_menu_callback("Hyderabad")
            },
            {   
                "viewclass": "IconListItem",
                "text": "Kolkata",
                "icon":"airplane-landing",
                "on_release":lambda: self.destination_menu_callback("Kolkata")
            }
        ]
        

        self.destination_menu = MDDropdownMenu(
            caller=self.ids.destination_button,
            items=Destination_menu_items,
            width_mult=3,
            max_height=250,
        )
        self.destination_menu.open()
    
    def destination_menu_callback(self, text_item):
        global destination_text
        self.destination_text=text_item
        self.ids.destination_button.text=text_item
        self.destination_menu.dismiss()

    # Card 4 Stopage card
    def stopage_dropdown_items(self):
        stopage_menu_items = [
            {
                "viewclass": "IconListItem",
                "text": "Non-Stop",
                "icon":"map-marker-radius",
                "on_release":lambda: self.stopage_menu_callback("Non-Stop")
            } ,
            {
                "viewclass": "IconListItem",
                "text": "1",
                "icon":"map-marker-radius",
                "on_release":lambda: self.stopage_menu_callback("1")
            } ,
            {
                "viewclass": "IconListItem",
                "text": "2",
                "icon":"map-marker-radius",
                "on_release":lambda: self.stopage_menu_callback("2")
            } ,
            {   
                "viewclass": "IconListItem",
                "text": "3",
                "icon":"map-marker-radius",
                "on_release":lambda: self.stopage_menu_callback("3")
            },
            {   
                "viewclass": "IconListItem",
                "text": "4",
                "icon":"map-marker-radius",
                "on_release":lambda: self.stopage_menu_callback("4")
            }
        ]
        

        self.stopage_menu = MDDropdownMenu(
            caller=self.ids.stopage_button,
            items=stopage_menu_items,
            width_mult=3,
            max_height=250,
        )
        self.stopage_menu.open()
    
    def stopage_menu_callback(self, text_item):
        global stopage_text
        self.stopage_text=text_item
        self.ids.stopage_button.text=text_item
        self.stopage_menu.dismiss()


class ResultScreen(Screen):
    def show_datatable(self,output):
        self.table=MDDataTable(pos_hint={"center_x":0.5,"center_y":0.5},
                        size_hint=(0.9,0.7),
                        elevation=20,
                        use_pagination=True,
                        rows_num=12,
                        column_data=[
                            ("Date",dp(20)),
                            ("Airline",dp(25)),
                            ("Price("+str(u"\u20B9")+")",dp(25))
                                    ],
                        row_data=output
                        )
        
        self.add_widget(self.table)
        prediction_list=[]
        output=[]
        predicted_list=[]

    #help button - Dialog
    def back(self):
        self.manager.current="Main"

    def help(self):
        close_btn=MDFlatButton(text="Close",on_release=self.close_dialog)
        self.dialog=MDDialog(title="Disclaimer",
                            text="This prediction results are predicted using Machine Learning model.\nThe accuracy of our model is 82%.\n\nPrivacy Policy:\nWe don't store or transfer your any kind of data.Your data is secured.",
                            buttons=[close_btn])
        self.dialog.open()
    def close_dialog(self,instance):
        self.dialog.dismiss()

    def on_enter(self, *args):
        global prediction_list,output,initial_date,final_date,Total_stops,predicted_list
        predicted_list=[]
        output=[]
        airline_array=["AIR ASIA",
                        "Jet Airways",
                        "IndiGo",
                        "Air India",
                        "Multiple_carriers",
                        "SpiceJet",
                        "Vistara",
                        "GoAir",
                        "Multiple carriers Premium economy",
                        "Jet Airways Business",
                        "Vistara Premium economy",
                        "Trujet"]
        Dep_hour=0
        Dep_min=0

        #Stops
        if stopage_text=="Non-Stop":
            dur_hour=1.95
            dur_min=32.6969
            Total_stops=0
        elif stopage_text=="1":
            dur_hour=12.60
            dur_min=25.8124
            Total_stops=1
        elif stopage_text=="2":
            dur_hour=20.0953
            dur_min=27.8157
            Total_stops=2
        elif stopage_text=="3":
            dur_hour=25.4444
            dur_min=20.7777
            Total_stops=3
        else:
            dur_hour=29
            dur_min=30
            total_stopage=4

        Arrival_hour = dur_hour
        Arrival_min = dur_min

        # Source
        # Banglore = 0 (not in column)
        if (source_text == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (source_text == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (source_text == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (source_text == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # Destination
        if (destination_text == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        
        elif (destination_text == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (destination_text == 'New_Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (destination_text == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (destination_text == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        try:
            initial_date=datetime.datetime.strptime(initial_date,"%d/%m/%Y").strftime("%Y-%m-%d")
            final_date=datetime.datetime.strptime(final_date,"%d/%m/%Y").strftime("%Y-%m-%d")

            dates_array=[]
            start_dt = initial_date[:10]
            start_dt=date(int(start_dt[:4]),int(start_dt[5:7]),int(start_dt[8:10]))
            end_dt = final_date[:10]
            end_dt=date(int(end_dt[:4]),int(end_dt[5:7]),int(end_dt[8:10]))

            def daterange(date1, date2):
                for n in range(int ((date2 - date1).days)+1):
                    yield date1 + timedelta(n)

            for dt in daterange(start_dt, end_dt):
                dates_array.append(dt.strftime("%Y-%m-%d"))

            for i in range(len(dates_array)):
                Journey_day = int(str(dates_array[i][-2:-1]+dates_array[i][-1]))
                Journey_month = int(str(dates_array[i])[-5:-3])

                prediction_list=[
                        Total_stops,
                        Journey_day,
                        Journey_month,
                        Dep_hour,
                        Dep_min,
                        Arrival_hour,
                        Arrival_min,
                        dur_hour,
                        dur_min,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        s_Chennai,
                        s_Delhi,
                        s_Kolkata,
                        s_Mumbai,
                        d_Cochin,
                        d_Delhi,
                        d_Hyderabad,
                        d_Kolkata,
                        d_New_Delhi
                    ]
                for air in range(9,21):
                    prediction=model.predict([prediction_list])
                    predicted_list.append(round(prediction[0],2))
                    prediction_list[air]=1
                    prediction_list[9:air]=[0]*(air-9)
            count=0
            date_count=0
            show_date_array=[]
            for j in range(len(dates_array)):
                show_date_array.append(datetime.datetime.strptime(dates_array[j],"%Y-%m-%d").strftime("%d/%m/%Y"))
            
            for i in range(len(dates_array)*len(airline_array)):
                if count==len(airline_array):
                    count=0
                    date_count+=1
                output.append(tuple([show_date_array[date_count],airline_array[count],predicted_list[i]]))
                count+=1
            self.show_datatable(output)
        except:
            self.back()
            self.error_close_btn=MDFlatButton(text="Close",on_release=self.error_close_dialog)
            self.error_dialog=MDDialog(title="Error",text="All fields are mendatory",buttons=[self.error_close_btn])
            self.error_dialog.open()


    def error_close_dialog(self,instance):
        self.error_dialog.dismiss()

sm=ScreenManager()
sm.add_widget(MainScreen(name="Main"))
sm.add_widget(ResultScreen(name="Result"))


class Flight(MDApp):
    def build(self):
        self.icon="Resources\icon.png"
        self.theme_cls.theme_style="Light"
        screen=Screen()
        
        screen.add_widget(Builder.load_file("Resources\main.kv"))
        return screen


    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()
        
if __name__=="__main__":
    global prediction_list,initial_date,final_date,source_text,destination_text,stopage_text,output,Total_stops,predicted_list
    prediction_list=[]
    output=[]
    predicted_list=[]
    initial_date=""
    final_date=""
    source_text=""
    destination_text=""
    stopage_text=""
    Total_stops=0
    model = pickle.load(open("Resources\\flight_rf.pkl", "rb"))
    Flight().run()