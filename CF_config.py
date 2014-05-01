target_record = 'subdomain'
email_address = 'timlardner@gmail.com'
API_key = '12345' # You can get this from your account details page on the Cloudflare website
zone = 'example.com'
CF_on = False # For things like SSH, set this to False. For web-servers only, True is OK. 
TTL = '300'   # Short TTLs are best for often changing IPs like dynamic ones. 300 is the minimum for a free account