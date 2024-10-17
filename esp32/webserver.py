import network
import utime
import socket

from dht import DHT11
from bmp180 import Bmp180
from machine import Pin
from esp32 import raw_temperature

try:
    import config
except ImportError:
    print("I can't find configuration. Remane the file 'config.py.example' as 'config.py', edit accordingly and flash it.")
    raise

SENSOR_DHT_PIN = 16
SENSOR_BMP_SCL = 23
SENSOR_BMP_SDA = 22

def startWifiClient(ssid, passwd, ipconfig=None):
    '''
    Starts the wifi module as client
    @param ssid: Name of the network
    @param passwd: Password of the network
    @param ipconfig: (optional) IP configuration.
                   For example: ["192.168.1.210", "255.255.255.0", "192.168.1.1", "192.168.1.1"]
                   If not provided the configuration will be done by DHCP.
    '''

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, passwd)
    while not wifi.isconnected():
        utime.sleep(1)
    
    if ipconfig:
        wifi.ifconfig(ipconfig)
        utime.sleep(1)
        
        
def startWifiAp():

    wifi = network.WLAN(network.AP_IF)
    wifi.active(True)
    wifi.config(essid='ESP32-TEST-AP', authmode=network.AUTH_OPEN)

    
def startServer(dispatchFunc, dispatchObj, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(5)
    
    print("Listening on port {0}...".format(port))
    
    while True:
        conn, addr = s.accept()
        try:
            print("Got a connection from {0}".format(addr))
            request = conn.recv(1024)
            print(str(request))
        
            response = dispatchFunc(dispatchObj)
            
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
            
        except Exception as ex:
            print(ex)


def dispatch(obj):

    dht11 = obj["dht11"]
    dht11.measure()
    temp1 = dht11.temperature()
    humi = dht11.humidity()
    
    bmp180 = obj["bmp180"]
    temp2 = bmp180.readTemperature()
    press = bmp180.readPressure() / 100.0
    
    espTemperature = (raw_temperature()-32)*5/9
    
    time = utime.time_ns()

    html = """
            <html>
                <head>
                    <title>ESP32 Example</title>
                </head>
                <body>
                    <table>
                        <tr><th colspan=2>Esp32</th></tr>
                        <tr><td><b>Temperature</b></td><td>{0:.2f} &deg;C</td></tr>
                        <tr><td><b>Timestamp</b></td><td>{5}</td></tr>
                        <tr><th colspan=2>DHT11</th></tr>
                        <tr><td><b>Temperature</b></td><td>{1:.2f} &deg;C</td></tr>
                        <tr><td><b>Humidity</b></td><td>{2:.2f} %</td></tr>
                        <tr><th colspan=2>BMP180</th></tr>
                        <tr><td><b>Temperature</b></td><td>{3:.2f} &deg;C</td></tr>
                        <tr><td><b>Pressure</b></td><td>{4:.2f} mbar</td></tr>
                    </table>
                </body>
            </html>
        """.format(espTemperature, temp1, humi, temp2, press, time)

    return html


def main():

    if config.CONFIG_AP:
        wifi = startWifiAp()
    else:
        wifi = startWifiClient(config.SSID, config.PASSWD, config.IP_CONFIG)
        
    dht11 = DHT11(Pin(SENSOR_DHT_PIN))
    bmp180 = Bmp180(0, SENSOR_BMP_SCL, SENSOR_BMP_SDA)
    startServer(dispatch, { "dht11": dht11, "bmp180": bmp180 }, config.SERVER_PORT)
    
    
if __name__ == '__main__':
    main()
