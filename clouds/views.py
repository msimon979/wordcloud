import redis
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from clouds.models import SubmittedUrls, Words

validate = URLValidator()
DEFAULT_LIMIT = 3
MAX_LIMIT = 20
# Setting an hour for now
CACHE_EXPIRE = 60 * 60
REDIS = redis.Redis(host="redis", port=6379)


# move out of view if you have time
def url_exists(url):
    if REDIS.get(url):
        return True
    return False


def is_valid_url(url: str) -> bool:
    """returns bool if a valid url

    Args:
        url (str): url

    Returns:
        bool: returns bool based off value
    """
    try:
        validate(url)
    except:
        return False
    return True


class SubmitUrlView(APIView):
    http_method_names = ["post", "head", "options"]

    def post(self, request):
        if url := request.data.get("url"):
            # Move this logic and create to serializer if time
            if is_valid_url(url):

                if url_exists(url):
                    return JsonResponse(
                        {"results": "url already exists"},
                        status=status.HTTP_204_NO_CONTENT,
                    )

                try:
                    submitted_url = SubmittedUrls.objects.create(url=url)
                    REDIS.set(url, 1, CACHE_EXPIRE)
                except:
                    # Add logging here
                    print("Url was not created")
                    return JsonResponse(
                        {"error": f"database issue, url not created"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                # Accepted
                return JsonResponse(
                    model_to_dict(submitted_url), status=status.HTTP_202_ACCEPTED
                )

            # Invalid url
            return JsonResponse(
                {"error": f"invalid url: {url}"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Missing url in payload
        return JsonResponse(
            {"error": f"missing url in data"}, status=status.HTTP_400_BAD_REQUEST
        )


class WordsView(APIView):
    http_method_names = ["get", "head", "options"]

    def get(self, request):
        limit = DEFAULT_LIMIT

        # Move this logic and create to serializer if time
        if limit_param := request.query_params.get("limit"):
            try:
                limit = int(limit_param)

                # Prevent returning data over MAX_LIMIT. Move this logic somewhere
                # else if you have time
                limit = limit if limit <= MAX_LIMIT else DEFAULT_LIMIT
            except ValidationError:
                print(f"Unable to cast param to int, using {DEFAULT_LIMIT}")

        qs = Words.objects.all().order_by("-count")[:limit]

        results = [model_to_dict(q) for q in qs]

        return JsonResponse({"results": results}, status=status.HTTP_200_OK)
