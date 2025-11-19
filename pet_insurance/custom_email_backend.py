"""
Custom SMTP email backend that disables SSL certificate verification
for self-signed certificates (common with Plesk mail servers)
"""
import ssl
from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):
    """SMTP backend that doesn't verify SSL certificates"""
    
    def open(self):
        if self.connection:
            return False
        try:
            if self.use_ssl:
                # For SSL (port 465), create connection without SSL first, then wrap
                import socket
                sock = socket.create_connection((self.host, self.port), self.timeout)
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection = self.connection_class(
                    self.host, self.port,
                    local_hostname=self.local_hostname,
                    timeout=self.timeout,
                )
                self.connection.sock = context.wrap_socket(sock, server_hostname=self.host)
            else:
                # For TLS (port 587), use standard connection
                self.connection = self.connection_class(
                    self.host, self.port,
                    local_hostname=self.local_hostname,
                    timeout=self.timeout,
                )
                if self.use_tls:
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

