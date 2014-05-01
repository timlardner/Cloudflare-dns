import urllib
import urllib2
import json
import CF_config

email_address = CF_config.email_address
zone = CF_config.zone
API_key = CF_config.API_key
CF_on = CF_config.CF_on
TTL = CF_config.TTL
target_record = CF_config.target_record

# Get current IP
new_ip = urllib.urlopen("http://my-ip.heroku.com/").read().strip()
target_record = target_record+"."+zone
if CF_on:
    service_mode = '1'
else:
    service_mode = '0'

# Get all current records and find ID of the target record
url = 'https://www.cloudflare.com/api_json.html'
values1 = {'a' : 'rec_load_all',
          'tkn' : API_key,
          'email' : email_address,
          'z':zone
          }

data = urllib.urlencode(values1)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
output = json.loads(the_page)
response = output.get('response')
objs = response.get('recs').get('objs')
found_rec = False
for iter in objs:
    if iter.get('name') == target_record:
        new_id = iter.get('rec_id')
        found_rec = True

# If the record we wish to set exists, then just update it
if found_rec:
    values = {'a' : 'rec_edit',
          'tkn' : API_key,
          'email' : email_address,
          'z':zone,
          'type':'A',
          'name':target_record,
          'id':new_id,
          'content':new_ip,
          'service_mode':service_mode,
          'ttl':TTL
          }
    update = 'update'
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response2 = urllib2.urlopen(req)
    the_page2 = response2.read()
    output2 = json.loads(the_page2)
    success = str(output2.get('result')).capitalize()
# create a new one. When we make a new one, we still need to use the update function
# otherwise, traffic will be forwarded through Cloudflare
else:
    values = {'a' : 'rec_new',
          'tkn' : API_key,
          'email' : email_address,
          'z':zone,
          'type':'A',
          'name':target_record,
          'content':new_ip,
          'ttl':TTL
          } 
    update = 'create'    
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response2 = urllib2.urlopen(req)
    the_page2 = response2.read()
    output2 = json.loads(the_page2)
    success = str(output2.get('result')).capitalize()
    if success == 'Success' and CF_on == False:
        data = urllib.urlencode(values1)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        output = json.loads(the_page)
        response = output.get('response')
        objs = response.get('recs').get('objs')
        for iter in objs:
            if iter.get('name') == target_record:
                new_id = iter.get('rec_id')
        values = {'a' : 'rec_edit',
              'tkn' : API_key,
              'email' : email_address,
              'z':zone,
              'type':'A',
              'name':target_record,
              'id':new_id,
              'content':new_ip,
              'service_mode':'0',
              'ttl':TTL
              }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response2 = urllib2.urlopen(req)
        the_page2 = response2.read()
        output2 = json.loads(the_page2)
        success = str(output2.get('result')).capitalize()
    
print "Attempted to %s %s with IP %s: %s" % (update,target_record,new_ip,success) 
