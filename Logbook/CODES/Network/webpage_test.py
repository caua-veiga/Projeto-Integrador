import machine
import network, socket, urequests

def do_connect():
    '''
    Connects to local Wi-Fi
    '''
    essid = "NOS-D610" # "Galaxy A32 5G1A70"
    password = "fbe228d0bc19"  # "yfee4537"

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def parseQuerystring(url, qs):
    '''
    Parse a dictionary containing the query parameters
    and write them to the url
    '''
    query = f"?key={qs['key']}&src={qs['src']}&hl={qs['hl']}&r={qs['r']}&c={qs['c']}&f={qs['f']}"
    return url + query


def main():
    do_connect()

    url = "http://api.voicerss.org/"
    querystring = {
                   "key":"855df224b9e54663af317722f0a96eaf",
                   "src":"Testing",
                   "hl":"en-us",
                   "r":"0",
                   "c":"mp3",
                   "f":"8khz_8bit_mono"
                   }
    parsed = parseQuerystring(url, querystring)
    api_response = urequests.request("GET", parsed)
    print(api_response.status_code)
    with open("test.mp3", mode="wb") as file:
        print("Writing .mp3 ...")
        file.write(api_response.content)
        print("Finished writing")

    html =  """
            <!DOCTYPE html>
            <html>
              <head> <title>Color sensor</title> </head>
              <body>
                <h1>Current reading</h1>
                <p>This box updates with the current color measured by the sensor.</p>
                <style>
                .square {
                  height: 50px;
                  width: 50px;
                  background-color: rgb(255, 099, 071);
                }
                </style>
                </head>
              <body>
                <h2>Color</h2>
                <div class="square"></div>
              </body>

              <body>
                <h1>Text-to-speech</h1>
                <p>We use the VoiceRRS API to read outloud the color name.</p>
                <audio controls autoplay>
                  <source src="test.mp3" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              </body>
            </html>
            """

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        # Send audio file
#         cl.send('HTTP/1.0 200 OK\r\nContent-type: audio/mpeg\r\n\r\n')
#         with open("test.mp3", "r") as file:
#             audio = file.read()
#             cl.send(audio)
        # Send page HTML 
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        
        


if __name__=='__main__':
    main()
