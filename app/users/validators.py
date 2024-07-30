from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator as BaseUserAttributeSimilarityValidator,
    MinimumLengthValidator as BaseMinimumLengthValidator,
    CommonPasswordValidator as BaseCommonPasswordValidator,
    NumericPasswordValidator as BaseNumericPasswordValidator,
)


class UserAttributeSimilarityValidator(BaseUserAttributeSimilarityValidator):
    def __call__(self, *args, **kwargs):
        return self.validate(*args, **kwargs)


class MinimumLengthValidator(BaseMinimumLengthValidator):
    def __call__(self, *args, **kwargs):
        return self.validate(*args, **kwargs)


class CommonPasswordValidator(BaseCommonPasswordValidator):
    def __call__(self, *args, **kwargs):
        return self.validate(*args, **kwargs)


class NumericPasswordValidator(BaseNumericPasswordValidator):
    def __call__(self, *args, **kwargs):
        return self.validate(*args, **kwargs)
