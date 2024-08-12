from rest_framework import serializers, exceptions


class CoreSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)

    @classmethod
    def get_model(cls):
        """This method returns the Django model associated
        with this serializer. If no model is specified in the serializer's Meta class, it returns None.
        """
        return cls.Meta.model or None

    @classmethod
    def get_model_fields(cls):
        """This method returns a list of all fields in the
        associated model."""
        return cls.get_model()._meta.fields  # type: ignore

    @classmethod
    def get_updateable_fields(cls):
        """This method returns a list of all fields in the
        associated model."""
        return cls.Meta.updateable_fields  # type: ignore

    @classmethod
    def get_field_defaults(cls, field_name):
        """This method returns the default value of a
        field in the associated model."""
        return cls.get_model()._meta.get_field(field_name).get_default()  # type: ignore

    def create(self, validated_data: dict):
        """When creating a new object, this method is called.
        It iterates over all fields in the model, checks if the field
        is in the Meta.fields list, and adds it to the validated_data
        dictionary with its default value if it's not provided.
        Then, it creates a new object using the validated_data
        dictionary."""
        if isinstance(validated_data, dict):
            new_validated_data = {}
            for field in self.get_model_fields():
                if field.name in self.Meta.fields:
                    new_validated_data[f"{field.name}"] = validated_data.get(
                        field.name, self.get_field_defaults(field.name)
                    )
            return self.get_model().objects.create(**new_validated_data)  # type: ignore

    def update(self, instance, validated_data):
        """When updating an object, this method is called.
        It iterates over all fields in the model, checks if the field
        is in the Meta.fields list, and updates the instance with the
        new value if it's provided in the validated_data dictionary.
        Then, it saves the instance."""
        if hasattr(self.Meta, "updateable_fields"):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        else:
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance

    @classmethod
    def get_object_instance(cls, instance):
        return cls(instance)

    @classmethod
    def get_object_data(cls, instance):
        return cls.get_object_instance(instance).data


class CoreReadOnlySerializer(CoreSerializer):

    def __init__(self, *args, **kwargs):
        """This method is called when initializing the serializer.
        It iterates over all fields in the serializer, sets the read_only
        attribute to True, and sets the required attribute to False.
        This means that all fields in the serializer are read-only and
        are not required."""
        super().__init__(*args, **kwargs)
        for key in self.get_fields():
            self.fields[key].read_only = True
            self.fields[key].required = False

    def update(self, instance, validated_data):
        """This method is called when updating an object.
        It raises an exception because the method is not allowed for
        read-only serializer."""
        raise exceptions.MethodNotAllowed(
            "Method 'update' is not allowed for read-only serializer."
        )

    def create(self, validated_data: dict):
        """This method is called when creating a new object.
        It raises an exception because the method is not allowed for
        read-only serializer."""
        raise exceptions.MethodNotAllowed(
            "Method 'create' is not allowed for read-only serializer."
        )
