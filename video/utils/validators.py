from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator(object):
    def __init__(self, max_size: int, min_size: int = None):
        assert max_size is not None, "You should set max_size parameter"
        assert isinstance(max_size, int), "max_size parameter should be an integer indicating maximum desired byte size"
        assert min_size is None or isinstance(min_size, int), \
            "min_size should be an integer indicating minimum desired byte size"

        self.max_size = max_size
        self.max_size_text = self.human_readable_size(self.max_size)

        self.min_size = min_size
        self.min_size_text = min_size and self.human_readable_size(self.min_size)

    def __call__(self, file_obj: File) -> None:
        if file_obj.size > self.max_size:
            raise ValidationError(
                f'File too large, file size should not exceed {self.max_size_text}s.'
            )
        if self.min_size is not None and file_obj.size < self.min_size:
            raise ValidationError(
                f'File too small, file size should be more than {self.min_size_text})s.'
            )

    @staticmethod
    def human_readable_size(value: int) -> str:
        """ Simple kb/mb/gb size snippet for templates"""
        if value < 512000:
            value = value / 1024.0
            ext = 'KB'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'MB'
        else:
            value = value / 1073741824.0
            ext = 'GB'
        return f'{int(value)} {ext}'
