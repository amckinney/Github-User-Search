import json
import time
import urllib
import urllib2
import base64
import sys

def main(argv):
  print "Starting Engineer Search:"
  uniquify(argv[0])
  find_engineers()

def uniquify(filename):
  """ Creates an input file with unique entries. """
  document = open("input.txt", 'w')
  input_file = open(filename, 'r')
  contents = input_file.read()
  input_file.close()
  new_list = contents.split()
  unique_list = set(new_list)
  for item in unique_list:
    new_line = item + "\n"
    document.write(new_line)
  document.close()

def find_engineers():
  """Goes through potential engineers one by one"""

  output = open("github_emails.txt", "w")
  valid_emails = []
  count = 0

  for line in open("input.txt", 'r'):
    count += 1

    print "Search Count: " + str(count)
    url = call_github(line)

    if url:
      entry = line + "-- " + url
      print entry
      valid_emails.append(entry)

    if count % 30 == 0:
      valid_emails = list(set(valid_emails))

      for email in valid_emails:
        print "Adding Valid Github Emails:"
        print email
        g_email = email + "\n"
        output.write(g_email)
        output.write("\n")

      print "Request Max (30) Reached. Sleeping for a 90 seconds."
      valid_emails = []
      time.sleep(90)

  valid_emails = list(set(valid_emails))
  for email in valid_emails:
    print "Adding Final Entries:"
    print email
    g_email = email + "\n"
    output.write(g_email)
    output.write("\n")

  output.close()


def call_github(email):
  """Returns an email's Github URL"""

  url = 'https://api.github.com/search/users'
  values = {'q' : '{0} in:email type:user repos:>0'.format(email) }

  # TODO Insert Github credentials here. You will be limited to 30 requests per minute.
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
