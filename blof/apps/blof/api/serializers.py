import HTMLParser
import random
import re

from django.contrib.auth.models import User
from rest_framework import serializers

from .. import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'email')
        read_only_fields = ('id',)
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostModel
        fields = ('id', 'body', 'date', 'user',)
        read_only_fields = ('date', 'user',)

    IMPACTFUL_WORD = re.compile(r'\b(?P<word>\w+)!')
    PUNCTUATION_IN_QUOTE = re.compile(r'(?P<word>\w+)(?P<punct>[\.,])[\"\']')
    LAZY_PLURAL = re.compile(r'\b(?P<word>\w{4,})s\b')
    LAZY_OWNED = re.compile(r'\b(?P<word>\w{4,})(?P<punct>\')s\b')
    PUNCTUATION_FREE_WORD = re.compile(r'\b(?P<word>\w{2,}) ')

    HtmlParser = HTMLParser.HTMLParser()

    @staticmethod
    def transform_user(obj, value):
        return obj.user.username if value else 'Anonymous'

    @classmethod
    def transform_body(cls, obj, value):
        """ add grammar and spelling mistakes to body """
        # randomly adding incorrect punctuation
        candidates_for_mistakes = list(set(cls.PUNCTUATION_FREE_WORD.findall(value)))
        for mistake in xrange(int(value.count(' ') * 0.05)):
            word = random.choice(candidates_for_mistakes)
            value = value.replace('{0} '.format(word),
                                  '{0}{1} '.format(word, random.choice(';,')))

        # richards --> richard's. using html encoded so LAZY_OWNED not affect
        value = cls.LAZY_PLURAL.sub(r"\1&apos;s", value)
        # richard's --> richards 
        value = cls.LAZY_OWNED.sub(r'\1s', value)
        # richard! --> "richard!"
        value = cls.IMPACTFUL_WORD.sub(r'"\1!"', value)
        # "richard." --> "richard".
        value = cls.PUNCTUATION_IN_QUOTE.sub(r'\1"\2', value)

        return cls.HtmlParser.unescape(value)
