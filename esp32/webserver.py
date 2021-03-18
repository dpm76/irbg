import network
import utime
import socket

from dht import DHT11
from machine import Pin


CONFIG_AP = True
SERVER_PORT = 8080
SENSOR_DHT_PIN = 23

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
            
        except ex:
            print(ex)


def dispatch(obj):

    sensor = obj["sensor"]
    sensor.measure()
    temp = sensor.temperature()
    humi = sensor.humidity()
    time = utime.time_ns()
    #TODO: Add data from the BMP180 sensor

    html = """
            <html>
                <head>
                    <title>ESP32 Example</title>
                </head>
                <body>
                    <table>
                        <tr><td><b>Temperature</b></td><td>{0} C</td></tr>
                        <tr><td><b>Humidity</b></td><td>{1} %</td></tr>
                        <tr><td><b>Time</b></td><td>{2}</td></tr>
                    </table>
                </body>
            </html>
        """.format(temp,humi, time)

    return html


def main():

    if CONFIG_AP:
        startWifiAp()
    else:
        startWifiClient()
        
    sensor = DHT11(Pin(SENSOR_DHT_PIN))
    startServer(dispatch, { "sensor": sensor }, SERVER_PORT)
    
    
if __name__ == '__main__':
    main()
