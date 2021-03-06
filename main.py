import requests
import json
import config
import logging
import smtplib
import base64
import os
import argparse
import setup

_args = None

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))
_logger.addHandler(ch)


def check_ip():
    try:
        if not os.path.isfile(config.ip_info_file):
            fh = open(config.ip_info_file, 'w+')
            fh.seek(0)
            fh.write(json.dumps({"ip": "0.0.0.0"}))
            fh.close()
        with open(config.ip_info_file, 'r+') as f:
            file_data = f.read()
            json_data = json.loads(file_data)
            old_ip = json_data['ip']
            _logger.info('Current IP address is `%s`' % old_ip)
            response = requests.get('https://api.ipify.org/')
            new_ip = response.text.strip()
            json_data['ip'] = new_ip
            f.seek(0)
            f.write(json.dumps(json_data))
    except Exception as e:
        _logger.debug(e)
        exit()
    if old_ip == new_ip:
        _logger.info('IP address has not changed')

    # region Update noip service
    auth_string_raw = '%s:%s' % (config.noip_username, config.noip_password)
    config.noip_base64 = base64.b64encode(auth_string_raw.encode('utf-8'))
    noip_headers = {'User-Agent': config.noip_user_agent,
                    'Authorization': 'Basic %s' % config.noip_base64.decode('utf-8'),
                    'Host': 'dynupdate.no-ip.com'}
    response = requests.get(config.noip_url % (config.noip_hostname, new_ip), headers=noip_headers)
    result = response.text.strip().split(' ')
    if result[0] == 'good':
        # region Email content
        _subject = 'IP address has changed for domain "%s"' % config.domains[0]
        email_msg = 'The IP address for the domain "%(domain)s" has changed, and has been' \
                    ' successfully updated for "%(noip_hostname)s"\n' \
                    'New IP address: %(new_ip)s\n' \
                    'Old IP address: %(old_ip)s\n' \
                    % {'domain': config.domains[0], 'new_ip': new_ip,
                       'old_ip': old_ip, 'noip_hostname': config.noip_hostname}
        # endregion
        # region Email server config
        _to = config.recipients
        _from = config.email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(config.email, config.password)

        _body = '\r\n'.join(['To: %s' % (','.join(_to) if len(_to) > 1 else _to[0]),
                             'From: %s' % config.from_name,
                             'Subject: %s' % _subject,
                             '', email_msg])
        # endregion
        try:
            server.sendmail(_from, _to, _body)
            _logger.info('Email sent')
        except:
            _logger.error('There was an error when sending the email')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('setup', help='Run the initial setup of the utility')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging', dest='v')
    subparsers = parser.add_subparsers(help='sub-command help')
    verify_parser = subparsers.add_parser('verify', help='Verify the initial setup')
    verify_parser.add_argument('--test', help='Do not make any changes when verifying setup',
                               dest='test', action='store_true')
    _args = parser.parse_args()

    if _args.v:
        _logger.setLevel(logging.DEBUG)
        _logger.debug('Verbose logging enabled')

    if _args.setup:
        setup.init()
    else:
        check_ip()


if __name__ == '__main__':
    main()
