#!/bin/python

from argparse import ArgumentParser
import json
import os.path
import requests

class App(object):

  def __init__(self):
    self.options = self.get_options()

  def run(self):
    credentials = self.read_credentials()

    currentPublicIp = self.get_public_ip()
    lastSyncedIp = self.get_last_synced_ip(credentials)

    if None == lastSyncedIp or lastSyncedIp != currentPublicIp:
      print "Syncing public ip %s with Google DDNS for url %s" % (currentPublicIp, credentials["url"])
      
      if self.sync_ip(credentials, currentPublicIp):
        credentials["last_synced_ip"] = currentPublicIp
        self.write_credentials(credentials)

    else:
      print "No change in IP found for %s - no need to sync (current public IP %s)" % (credentials["url"], lastSyncedIp)

  def get_options(self):
    parser = ArgumentParser(description = "Google DDNS Sync - Sync your public IP with Google DDNS")
    parser.add_argument("--credentials", help="Google DDNS Credentials (JSON File, { 'url':'the url', 'username':'your_user_name', 'password':'the password' })", required=True)
    return parser.parse_args()

  def get_public_ip(self):
    return json.loads(requests.get("http://jsonip.com").text)["ip"]

  def get_last_synced_ip(self, credentials):
    if "last_synced_ip" in credentials:
      return credentials["last_synced_ip"]

    return None

  def sync_ip(self, credentials, ip):
    url = "https://%s:%s@domains.google.com/nic/update?hostname=%s" % (credentials["username"], credentials["password"], credentials["url"])
    response = requests.post(url, allow_redirects=True)
    
    if "good %s" % ip != response.text and "nochg %s" % ip != response.text:
      print "Failed to sync ip with %i:%s" % (response.status_code, response.text)
      return False

    return True

  def read_credentials(self):
    with open(self.options.credentials) as f:    
      return json.load(f)

  def write_credentials(self, credentials):
    with open(self.options.credentials, 'w') as f:    
      f.write(json.dumps(credentials, indent=2))

if "__main__" == __name__:
  App().run()
