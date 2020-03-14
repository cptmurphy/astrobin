from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet, Q

from astrobin.models import Image
from toggleproperties.models import ToggleProperty


class UserService:
    user = None  # type: User

    def __init__(self, user):
        # type: (User) -> None
        self.user = user

    def _corrupted_query(self):
        # type: () -> Q
        return Q(corrupted=True, is_final=True) | \
               Q(revisions__corrupted=True, revisions__is_final=True)

    def get_all_images(self):
        # type: () -> QuerySet
        return Image.objects_including_wip.filter(user=self.user)

    def get_corrupted_images(self):
        # type: () -> QuerySet
        return self.get_all_images().filter(self._corrupted_query())

    def get_public_images(self):
        # type: () -> QuerySet
        return Image.objects \
            .filter(user=self.user) \
            .exclude(self._corrupted_query())

    def get_wip_images(self):
        # type: () -> QuerySet
        return Image.wip \
            .filter(user=self.user) \
            .exclude(self._corrupted_query())

    def get_deleted_images(self):
        # type: () -> QuerySet
        return Image.all_objects \
            .filter(user=self.user) \
            .exclude(deleted=None)

    def get_bookmarked_images(self):
        # type: () -> QuerySet
        image_ct = ContentType.objects.get_for_model(Image)  # type: ContentType
        bookmarked_pks = [x.object_id for x in \
                          ToggleProperty.objects.toggleproperties_for_user("bookmark", self.user).filter(
                              content_type=image_ct)
                          ]  # type: List[int]

        return Image.objects \
            .filter(pk__in=bookmarked_pks) \
            .exclude(self._corrupted_query())

    def get_liked_images(self):
        # type: () -> QuerySet
        image_ct = ContentType.objects.get_for_model(Image)  # type: ContentType
        liked_pks = [
            x.object_id for x in \
            ToggleProperty.objects.toggleproperties_for_user("like", self.user).filter(content_type=image_ct)
        ]  # type: List[int]

        return Image.objects \
            .filter(pk__in=liked_pks) \
            .exclude(self._corrupted_query())

    def get_image_numbers(self):
        return {
            'public_images_no': self.get_public_images().count(),
            'wip_images_no': self.get_wip_images().count(),
            'corrupted_no': self.get_corrupted_images().count(),
            'bookmarked_no': self.get_bookmarked_images().count(),
            'liked_no': self.get_liked_images().count(),
        }