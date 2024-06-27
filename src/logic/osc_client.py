from pythonosc import udp_client

ip = "127.0.0.1"
port = 4560
client = udp_client.SimpleUDPClient(ip, port)

def send_osc_message(name, sample):
    client.send_message(name, sample)
