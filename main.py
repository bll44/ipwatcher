import requests
import json
import config
import logging
import smtplib


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))
_logger.addHandler(ch)


def main():
    try:
        with open(config.ip_info_file, 'r+') as f:
            file_data = json.loads(f.read())
            f.seek(0)
            old_ip = file_data['ip']
            _logger.info('Current IP address is `%s`' % old_ip)
            response = requests.get('https://api.ipify.org/')
            new_ip = response.text.strip()
            file_data['ip'] = new_ip
            f.write(json.dumps(file_data))
    except Exception as e:
        _logger.debug(e)
        exit()

    if old_ip == file_data['ip']:
        _logger.info('IP address has not changed')
        exit()

    # region Send the email alert
    _to = config.recipients
    _from = config.email
    _subject = 'IP address has changed for domain "%s"' % config.domains[0]

    email_msg = "The IP address for the domain `%(domain)s` has changed.\n" \
                "New IP address: %(new_ip)s\n" \
                "Old IP address: %(old_ip)s\n" % {'domain': config.domains[0],
                                                  'new_ip': new_ip,
                                                  'old_ip': old_ip}

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(config.email, config.password)

    _body = '\r\n'.join(['To: %s' % (','.join(_to) if len(_to) > 1 else _to[0]),
                         'From: %s' % 'TeamSpeak Alerts',
                         'Subject: %s' % _subject,
                         '', email_msg])

    try:
        server.sendmail(_from, _to, _body)
        _logger.info('Email sent')
    except:
        _logger.error('There was an error when sending the email')
    # endregion


if __name__ == '__main__':
    main()