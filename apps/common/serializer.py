from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        try:
            request = self.context.get('request')
            return request.build_absolute_uri(instance.image.url)
        except (AttributeError, ValueError):
            return None
        except KeyError:
            print(self.parent)
