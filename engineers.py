import json
import time
import urllib
import urllib2
import base64
import sys

def main(argv):
  print "Starting Engineer Search:"
  find_engineers(argv[0])


def find_engineers(filename):
  """Goes through potential engineers one by one"""

  output = open("github_emails.txt", "w")
  count = 0
  valid_emails = []

  for line in open(filename):

    count += 1

    url = call_github(line)

    if url:
      valid_emails.append(line)

    if count % 20 == 0:
      valid_emails = list(set(valid_emails))

      print "Added Valid Github Emails!"
      for email in valid_emails:
        print email
        g_email = email + "\n"
        output.write(g_email)

      print "Request Max (20) Reached. Sleeping for 5 minutes."
      valid_emails = []
      time.sleep(300)

  output.close()


def call_github(email):
  """Calls GitHub with an email
  Returns a user's GitHub URL, if one exists.
  Otherwise returns None """

  url = 'https://api.github.com/search/users'
  values = {'q' : '{0} in:email type:user repos:>0'.format(email) }

  # TODO insert your credentials here or read them from a config file or whatever
  # First param is username, 2nd param is passwd
  # Without credentials, you'll be limited to 5 requests per minute
  auth_info = '{0}:{1}'.format('','')

  basic = base64.b64encode(auth_info)
  headers = { 'Authorization' : 'Basic ' + basic }
  params = urllib.urlencode(values)
  req = urllib2.Request('{0}?{1}'.format(url,params), headers=headers)
  response = json.loads(urllib2.urlopen(req).read())

  if response and response['total_count'] == 1:
    return response['items'][0]['html_url']
  else:
    return None


if __name__ == "__main__":
  main(sys.argv[1:])
