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
    
    @property
    def connection_class(self):
        """Override connection class for SSL"""
        if self.use_ssl:
            return CustomSMTP_SSL
        return super().connection_class
    
    def open(self):
        if self.connection:
            return False
        try:
            # Use the property to get the correct connection class
            conn_class = self.connection_class
            # Get local_hostname safely
            local_hostname = getattr(self, 'local_hostname', None)
            timeout = getattr(self, 'timeout', None)
            
            self.connection = conn_class(
                self.host, self.port,
                local_hostname=local_hostname,
                timeout=timeout,
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
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Email connection error: {e}")
            if not self.fail_silently:
                raise
            return False

