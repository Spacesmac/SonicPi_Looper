from pythonosc import udp_client

ip = "127.0.0.1"
port = 4560
client = udp_client.SimpleUDPClient(ip, port)

def send_osc_message(name, sample, effects):
    print(sample)
    if effects == None or all(effect == "" for effect in effects):
        client.send_message(name, sample)
    else:
        generate_code = ""
        for i in range(len(sample)):
            effect = effects[i]
            
            if effect:  # Only generate code for non-empty effects
                generate_code += f"  {effect} do\n"
                generate_code += f"    sample :{sample[i]}\n"
                generate_code += "  end\n"
            else:
                generate_code += f"    sample :{sample[i]}\n"
        client.send_message("/run_code", generate_code)
