import pathlib

from django.core.exceptions import SuspiciousOperation

from advert.services import set_advert_count


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class XForwardedForMiddleware:
    """
    Set REMOTE_ADDR if it's missing because of a reverse proxy (nginx + gunicorn) deployment.
    https://stackoverflow.com/questions/34251298/empty-remote-addr-value-in-django-application-when-using-nginx-as-reverse-proxy
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META:
            remote_addrs = request.META["HTTP_X_FORWARDED_FOR"].split(",")
            remote_addr = None

            # for some bots, 'unknown' was prepended as the first value: `unknown, ***.***.***.***`
            # in which case the second value actually is the correct one
            for ip in remote_addrs:
                ip = self._validated_ip(ip)
                if ip is not None:
                    remote_addr = ip
                    break

            if remote_addr is None:
                raise SuspiciousOperation("Malformed X-Forwarded-For.")

            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            request.META["REMOTE_ADDR"] = remote_addr

        return self.get_response(request)


class AdvertCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        advert_url = '/api/v1/advert/'
        request_url = request.path
        if request_url is None:
            return self.get_response(request)

        path = pathlib.Path(request_url)
        if str(path.parent) + '/' != advert_url:
            return self.get_response(request)

        client_ip = get_client_ip(request)
        set_advert_count(int(path.name))
        return self.get_response(request)



