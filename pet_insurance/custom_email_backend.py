"""
Custom SMTP email backend that disables SSL certificate verification
for self-signed certificates (common with Plesk mail servers)
"""
import ssl
import smtplib
import socket
from django.core.mail.backends.smtp import EmailBackend


class CustomSMTP_SSL(smtplib.SMTP_SSL):
    """Custom SMTP_SSL class that doesn't verify SSL certificates"""
    
    def __init__(self, host='', port=0, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, context=None):
        if context is None:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        self.context = context
        self.timeout = timeout
        self.esmtp_features = {}
        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            self.local_hostname = socket.getfqdn()
        if source_address:
            self.source_address = source_address
        else:
            self.source_address = None
        smtplib.SMTP_SSL.__init__(self, host, port, local_hostname, timeout, source_address, context)
    
    def _get_socket(self, host, port, timeout):
        new_socket = socket.create_connection((host, port), timeout, source_address=self.source_address)
        try:
            return self.context.wrap_socket(new_socket, server_hostname=host)
        except:
            new_socket.close()
            raise


class CustomEmailBackend(EmailBackend):
    """SMTP backend that doesn't verify SSL certificates"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the connection class for SSL
        if self.use_ssl:
            self.connection_class = CustomSMTP_SSL
    
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(
                self.host, self.port,
                local_hostname=self.local_hostname,
                timeout=self.timeout,
            )
            if not self.use_ssl and self.use_tls:
                # For TLS (port 587), disable certificate verification
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection.starttls(context=context)
            
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise

