import urllib2

some_url = "http://192.168.8.101:49768/register_client.cshtml"

content = urllib2.urlopen(some_url).read()
print content

