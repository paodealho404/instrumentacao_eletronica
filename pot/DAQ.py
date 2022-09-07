
import serial
import time
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import sys

def angle_gauge(angle,previous_angle,gauge_placeholder):
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = angle,
        mode = "gauge+number+delta",
        title = {'text': "Angle (°)"},
        delta = {'reference': previous_angle},
        gauge = {'axis': {'range': [0, 180]}}))

    gauge_placeholder.write(fig)

def angle_chart(df,chart_placeholder):
    fig = px.line(df, x="Time", y="Angle", title='Angle vs Time', color_discrete_sequence=['red'] )
    
    chart_placeholder.write(fig)

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def main():
    try:

        arduino = serial.Serial(port='COM3', baudrate=9600, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS) #Change the COM port to whichever port your arduino is in
        gauge_placeholder = st.empty()
        chart_placeholder = st.empty()
        
        if arduino.isOpen() == False:
            arduino.open()

        i = 0
        previous_angle = 0
        angle_record = pd.DataFrame(data=[],columns=['Time','Angle'])
        while True: #Change number of iterations to as many as you need
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            try:
                angle = round(float(arduino.readline().decode().strip('\r\n')),2)
            except:
                angle = 0
                pass

            angle_record.loc[i,'Time'] = current_time
            angle_record.loc[i,'Angle'] = angle
            angle_gauge(angle,previous_angle,gauge_placeholder)
            angle_chart(angle_record,chart_placeholder)
            time.sleep(0.01)
            i += 1
            if i==500:
                i=0
            previous_angle = angle

        angle_record.to_csv('angle_record.csv',index=False)

        if arduino.isOpen() == True:
            arduino.close()

    except Exception as e:
        print(e)
    # except:
    #     print('Wrong COM.\n Displaying all available COMs')
    #     print(serial_ports())


    
if __name__ == '__main__':
    main()
    




