#!/usr/bin/env python
# coding=utf-8

"""New Document serializer/deserializer."""

from unittest import TestCase

from bson import ObjectId
import mongoengine as db
from mongoengine_goodjson import GoodJSONEncoder, Document, EmbeddedDocument

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class ToJSONTest(TestCase):
    """Good JSON Encoder invocation test."""

    def setUp(self):
        """Setup the class."""
        class TestDocument(Document):
            title = db.StringField()

        class TestEmbeddedDocument(EmbeddedDocument):
            title = db.StringField()

        self.model_cls = TestDocument
        self.model = TestDocument(title="Test")
        self.model.pk = ObjectId()

        self.emb_cls = TestEmbeddedDocument
        self.emb_model = TestEmbeddedDocument(title="Test")

        self.model.to_mongo = self.emb_model.to_mongo = lambda x: {
            "id": self.model.pk,
            "title": "Test"
        }

    @patch("json.dumps")
    def test_document(self, dumps):
        """self.model.to_json should call encode function."""
        self.model.to_json()
        dumps.assert_called_once_with(
            self.model.to_mongo(True), cls=GoodJSONEncoder
        )

    @patch("json.dumps")
    def test_embdocument(self, dumps):
        """self.emb_model.to_json should call encode function."""
        self.emb_model.to_json()
        dumps.assert_called_once_with(
            self.emb_model.to_mongo(True), cls=GoodJSONEncoder
        )
