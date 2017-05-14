import os

# region Gmail config
email = '<gmail_username>'
password = '<gmail_password>'
recipients = ['recipient_1@example.com', 'recipient_2@example.com']
from_name = '<My Example Company>'
# endregion

# region Other settings
domains = ['brady.ehumps.me']
ip_info_file = os.path.abspath(os.path.join(__file__, '..', 'ip_info'))
# endregion

# region No-IP service config
noip_username = '<no-ip_username>'
noip_password = '<no-ip_password>'
noip_base64 = ''  # leave this blank
noip_hostname = '<no-ip hostname to update>'
noip_url = 'http://dynupdate.no-ip.com/nic/update?hostname=%s&myip=%s'  # leave this as is
# endregion