#!/usr/bin/env python
import sys
import os
import platform
import ssl
import logging
import subprocess
import socket
import requests
from requests import get
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def output_subprocess(command):
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    output = output.decode("utf-8")
    return output

# Create logger for consumer (logs will be emitted when poll() is called)
logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("cas_siem_consumer_debug.log", mode="a")
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)

# Import confluent_kafka lib
current_confluent_kafka = os.path.join(os.path.dirname(__file__), "..", "lib", "confluent_kafka_python374")
sys.path.append(current_confluent_kafka)
from confluent_kafka import Consumer, KafkaException, version, libversion
# Import Splunk Lib - http://dev.splunk.com/python
current_splunklib = os.path.join(os.path.dirname(__file__), "..", "lib", "splunklib_python374")
sys.path.append(current_splunklib)
import splunklib

logger.debug("##############################################")
logger.debug("## Citrix Analytics Splunk APP Debugging ")
logger.debug("##############################################")
logger.debug("##############################################")
logger.debug("## OS/Splunk details ")
logger.debug("##############################################")
logger.debug("Linux Details: " + str(platform.uname()))
logger.debug("Kernel Version: " + str(platform.platform()))
logger.debug("Splunk SDK Version: " + str(splunklib.__version__))
#try:
#    output_packages = output_subprocess("yum list installed")
#    logger.debug("Installed yum packages: \n" + str(output_packages))
#except:
#    pass
#try:
#    output_packages = output_subprocess("apt list --installed")
#    logger.debug("Installed apt packages: \n" + str(output_packages))
#except:
#    pass
try:
    output_splunk_version = output_subprocess(os.environ['_'] +" --version")
    logger.debug("Splunk version: " + str(output_splunk_version))
except:
    logger.warning("Splunk version: not available")
logger.debug("Splunk OpenSSL version: " + str(ssl.OPENSSL_VERSION))
logger.debug("Python Splunk version: " + str(sys.version))
logger.debug("Python Splunk version info: " + str(sys.version_info))
logger.debug("Python Splunk Confluent Kafka version: " + str(version()))
logger.debug("Python Splunk Confluent Kafka lib version: " + str(libversion()))
logger.debug("##############################################")
logger.debug("## OPENSSL/TSL details ")
logger.debug("##############################################")
try:
    output_m5sum = output_subprocess("md5sum " + os.environ['SPLUNK_HOME'] + "/etc/apps/TA_CTXS_AS/bin/*/*/*.pem")
    logger.debug("MD5Sum certificates: \n" + str(output_m5sum))
except:
    logger.warning("List MD5Sum failed")

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger.debug("TLS version check: " + requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])
try:
    logger.debug("## OPENSSL/TLS details - US \n")
    certificates_folder_US = os.path.join(os.path.dirname(__file__), "certificates/US/CARoot.pem")
    output_kafka_tls_1_2_broker_0_us = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-0.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_US+" -status")
    logger.debug("Kafka TLS 1_2 check US broker 0: \n" + str(output_kafka_tls_1_2_broker_0_us))
    output_kafka_tls_1_2_broker_1_us = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-1.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_US+" -status")
    logger.debug("Kafka TLS 1_2 check US broker 1: \n" + str(output_kafka_tls_1_2_broker_1_us))
    output_kafka_tls_1_2_broker_2_us = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-2.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_US+" -status")
    logger.debug("Kafka TLS 1_2 check US broker 2: \n" + str(output_kafka_tls_1_2_broker_2_us))
except:
    logger.warning("Kafka check broker US failed")
try:
    logger.debug("## OPENSSL/TLS details - EU \n")
    certificates_folder_EU = os.path.join(os.path.dirname(__file__), "certificates/EU/CARoot.pem")
    output_kafka_tls_1_2_broker_0_eu = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-eu-0.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_EU+" -status")
    logger.debug("Kafka TLS 1_2 check EU broker 0: \n" + str(output_kafka_tls_1_2_broker_0_eu))
    output_kafka_tls_1_2_broker_1_eu = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-eu-1.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_EU+" -status")
    logger.debug("Kafka TLS 1_2 check EU broker 1: \n" + str(output_kafka_tls_1_2_broker_1_eu))
    output_kafka_tls_1_2_broker_2_eu = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-eu-2.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_EU+" -status")
    logger.debug("Kafka TLS 1_2 check EU broker 2: \n" + str(output_kafka_tls_1_2_broker_2_eu))
except:
    logger.warning("Kafka check broker EU failed")
try:
    logger.debug("## OPENSSL/TLS details - APS \n")
    certificates_folder_APS = os.path.join(os.path.dirname(__file__), "certificates/APS/CARoot.pem")
    output_kafka_tls_1_2_broker_0_aps = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-aps-0.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_APS+" -status")
    logger.debug("Kafka TLS 1_2 check APS broker 0: \n" + str(output_kafka_tls_1_2_broker_0_aps))
    output_kafka_tls_1_2_broker_1_aps = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-aps-1.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_APS+" -status")
    logger.debug("Kafka TLS 1_2 check APS broker 1: \n" + str(output_kafka_tls_1_2_broker_1_aps))
    output_kafka_tls_1_2_broker_2_aps = output_subprocess("echo Q | " + os.environ['_'] + " cmd openssl s_client -connect casnb-aps-2.citrix.com:9094 -tls1_2 -CAfile "+certificates_folder_APS+" -status")
    logger.debug("Kafka TLS 1_2 check APS broker 2: \n" + str(output_kafka_tls_1_2_broker_2_aps))
except:
    logger.warning("Kafka check broker APS failed")

logger.debug("##############################################")
logger.debug("## Network details ")
logger.debug("##############################################")
logger.debug("External IP: " + str(get('https://api.ipify.org').text))
try:
    ### US check ###
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-0.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-0.citrix.com")
    else:
        logger.debug("Connectivity check: NOT Successful to Port 9094 for host casnb-0.citrix.com, connect_ex returned: " + str(result))
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-1.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-1.citrix.com")
    else:
        logger.debug("Connectivity check: NOT Successful to Port 9094 for host casnb-1.citrix.com, connect_ex returned: " + str(result))
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-2.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-2.citrix.com")
    else:
        logger.debug("Connectivity check: NOT Successful to Port 9094 for host casnb-2.citrix.com, connect_ex returned: " + str(result))
    sock.close()
except:
    logger.warning("Telnet US Kafka 9094 broker failed")
try:
    ### EU check ###
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-eu-0.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-eu-0.citrix.com")
    else:
        logger.debug(
            "Connectivity check: NOT Successful to Port 9094 for host casnb-eu-0.citrix.com, connect_ex returned: " + str(
                result))
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-eu-1.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-eu-1.citrix.com")
    else:
        logger.debug(
            "Connectivity check: NOT Successful to Port 9094 for host casnb-eu-1.citrix.com, connect_ex returned: " + str(
                result))
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-eu-2.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-eu-2.citrix.com")
    else:
        logger.debug(
            "Connectivity check: NOT Successful to Port 9094 for host casnb-eu-2.citrix.com, connect_ex returned: " + str(
                result))
    sock.close()
except:
    logger.warning("Telnet EU Kafka 9094 broker failed")
try:
    ### APS check ###
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-aps-0.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-aps-0.citrix.com")
    else:
        logger.debug(
            "Connectivity check: NOT Successful to Port 9094 for host casnb-aps-0.citrix.com, connect_ex returned: " + str(
                result))
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-aps-1.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-aps-1.citrix.com")
    else:
        logger.debug(
            "Connectivity check: NOT Successful to Port 9094 for host casnb-aps-1.citrix.com, connect_ex returned: " + str(
                result))
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)  # 2 Second Timeout
    result = sock.connect_ex(('casnb-aps-2.citrix.com', 9094))
    if result == 0:
        logger.debug("Connectivity check: Successful to Port 9094 for host casnb-aps-2.citrix.com")
    else:
        logger.debug(
            "Connectivity check: NOT Successful to Port 9094 for host casnb-aps-2.citrix.com, connect_ex returned: " + str(
                result))
    sock.close()
except:
    logger.warning("Telnet APS Kafka 9094 broker failed")