from django.conf import settings

class aRequest:
    request: dict = {}

    def get_image_path_insert(self, url: str) -> str:
        """
        Removes the base URL from a full URL, returning the relative path.
        """
        return url.replace(settings.BASE_URL, '')

    def get_image_path(self, url: str) -> str:
        """
        Returns the full URL for the image path if the input is a relative path,
        otherwise returns the input URL if it's already an absolute URL.
        """
        if isinstance(url, str):
            if url.lower().startswith("http"):  # Case insensitive comparison
                return url
            else:
                return settings.BASE_URL + url
        return ""
