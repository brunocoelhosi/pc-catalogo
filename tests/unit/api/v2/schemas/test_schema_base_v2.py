import pytest
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import ValidationError

from app.api.v2.schemas.base import (
    ModelSchema,
    UuidMixinSchema,
    TimestampMixinSchema
)

class TestModelSchema:
    
    def test_model_schema_is_base_model(self):
        """Testa se ModelSchema é um alias para BaseModel"""
        from pydantic import BaseModel
        assert ModelSchema == BaseModel

    def test_model_schema_can_be_used_as_base_class(self):
        """Testa se ModelSchema pode ser usado como classe base"""
        class TestModel(ModelSchema):
            name: str
            age: int
        
        # Act
        model = TestModel(name="João", age=30)
        
        # Assert
        assert model.name == "João"
        assert model.age == 30


class TestUuidMixinSchema:

    def test_uuid_mixin_schema_with_valid_uuid(self):
        """Testa UuidMixinSchema com UUID válido"""
        # Arrange
        test_uuid = uuid4()
        
        # Act
        model = UuidMixinSchema(id=test_uuid)
        
        # Assert
        assert model.id == test_uuid
        assert isinstance(model.id, UUID)

    def test_uuid_mixin_schema_with_uuid_string(self):
        """Testa UuidMixinSchema com string UUID válida"""
        # Arrange
        test_uuid = uuid4()
        uuid_string = str(test_uuid)
        
        # Act
        model = UuidMixinSchema(id=uuid_string)
        
        # Assert
        assert model.id == test_uuid
        assert isinstance(model.id, UUID)

    def test_uuid_mixin_schema_with_none(self):
        """Testa UuidMixinSchema com valor None (padrão)"""
        # Act
        model = UuidMixinSchema()
        
        # Assert
        assert model.id is None

    def test_uuid_mixin_schema_with_none_explicit(self):
        """Testa UuidMixinSchema com None explícito"""
        # Act
        model = UuidMixinSchema(id=None)
        
        # Assert
        assert model.id is None

    def test_uuid_mixin_schema_with_invalid_uuid_string(self):
        """Testa UuidMixinSchema com string UUID inválida"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UuidMixinSchema(id="invalid-uuid")
        
        assert "Input should be a valid UUID" in str(exc_info.value)

    def test_uuid_mixin_schema_with_invalid_type(self):
        """Testa UuidMixinSchema com tipo inválido"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UuidMixinSchema(id={"invalid": "dict"})
        
        assert "UUID input should be a string, bytes or UUID object" in str(exc_info.value)

    def test_uuid_mixin_schema_field_description(self):
        """Testa se o campo id tem a descrição correta"""
        # Act
        schema = UuidMixinSchema.model_json_schema()
        
        # Assert
        assert schema["properties"]["id"]["description"] == "Identificador do objeto"

    def test_uuid_mixin_schema_inheritance(self):
        """Testa herança de UuidMixinSchema"""
        class TestModel(UuidMixinSchema):
            name: str
        
        test_uuid = uuid4()
        
        # Act
        model = TestModel(id=test_uuid, name="Teste")
        
        # Assert
        assert model.id == test_uuid
        assert model.name == "Teste"


class TestTimestampMixinSchema:

    def test_timestamp_mixin_schema_with_datetime(self):
        """Testa TimestampMixinSchema com datetime válido"""
        # Arrange
        now = datetime.now()
        
        # Act
        model = TimestampMixinSchema(created_at=now, updated_at=now)
        
        # Assert
        assert model.created_at == now
        assert model.updated_at == now
        assert isinstance(model.created_at, datetime)
        assert isinstance(model.updated_at, datetime)

    def test_timestamp_mixin_schema_with_none(self):
        """Testa TimestampMixinSchema com valores None (padrão)"""
        # Act
        model = TimestampMixinSchema()
        
        # Assert
        assert model.created_at is None
        assert model.updated_at is None

    def test_timestamp_mixin_schema_with_none_explicit(self):
        """Testa TimestampMixinSchema com None explícito"""
        # Act
        model = TimestampMixinSchema(created_at=None, updated_at=None)
        
        # Assert
        assert model.created_at is None
        assert model.updated_at is None

    def test_timestamp_mixin_schema_with_iso_string(self):
        """Testa TimestampMixinSchema com string ISO datetime"""
        # Arrange
        iso_string = "2023-12-25T10:30:00"
        expected_datetime = datetime.fromisoformat(iso_string)
        
        # Act
        model = TimestampMixinSchema(created_at=iso_string, updated_at=iso_string)
        
        # Assert
        assert model.created_at == expected_datetime
        assert model.updated_at == expected_datetime

    def test_timestamp_mixin_schema_with_partial_data(self):
        """Testa TimestampMixinSchema com dados parciais"""
        # Arrange
        now = datetime.now()
        
        # Act
        model = TimestampMixinSchema(created_at=now)
        
        # Assert
        assert model.created_at == now
        assert model.updated_at is None

    def test_timestamp_mixin_schema_with_invalid_datetime(self):
        """Testa TimestampMixinSchema com datetime inválido"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TimestampMixinSchema(created_at="invalid-datetime")
        
        assert "Input should be a valid datetime" in str(exc_info.value)

    def test_timestamp_mixin_schema_with_invalid_type(self):
        """Testa TimestampMixinSchema com tipo inválido"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TimestampMixinSchema(created_at=object())
        
        # Verifica se há erro de validação relacionado a datetime
        error_message = str(exc_info.value)
        assert any(phrase in error_message for phrase in [
            "Input should be a valid datetime",
            "datetime input should be"
        ])

    def test_timestamp_mixin_schema_field_descriptions(self):
        """Testa se os campos têm as descrições corretas"""
        # Act
        schema = TimestampMixinSchema.model_json_schema()
        
        # Assert
        assert schema["properties"]["created_at"]["description"] == "Data e hora da criação"
        assert schema["properties"]["updated_at"]["description"] == "Data e hora da atualização"

    def test_timestamp_mixin_schema_inheritance(self):
        """Testa herança de TimestampMixinSchema"""
        class TestModel(TimestampMixinSchema):
            name: str
        
        now = datetime.now()
        
        # Act
        model = TestModel(name="Teste", created_at=now, updated_at=now)
        
        # Assert
        assert model.name == "Teste"
        assert model.created_at == now
        assert model.updated_at == now


class TestCombinedMixins:

    def test_combined_mixins_inheritance(self):
        """Testa herança combinada de ambos os mixins"""
        class TestModel(UuidMixinSchema, TimestampMixinSchema):
            name: str
        
        test_uuid = uuid4()
        now = datetime.now()
        
        # Act
        model = TestModel(
            id=test_uuid,
            name="Teste",
            created_at=now,
            updated_at=now
        )
        
        # Assert
        assert model.id == test_uuid
        assert model.name == "Teste"
        assert model.created_at == now
        assert model.updated_at == now

    def test_combined_mixins_with_partial_data(self):
        """Testa mixins combinados com dados parciais"""
        class TestModel(UuidMixinSchema, TimestampMixinSchema):
            name: str
        
        # Act
        model = TestModel(name="Teste")
        
        # Assert
        assert model.id is None
        assert model.name == "Teste"
        assert model.created_at is None
        assert model.updated_at is None

    def test_combined_mixins_json_schema(self):
        """Testa schema JSON dos mixins combinados"""
        class TestModel(UuidMixinSchema, TimestampMixinSchema):
            name: str
        
        # Act
        schema = TestModel.model_json_schema()
        
        # Assert
        properties = schema["properties"]
        assert "id" in properties
        assert "created_at" in properties
        assert "updated_at" in properties
        assert "name" in properties
        assert properties["id"]["description"] == "Identificador do objeto"
        assert properties["created_at"]["description"] == "Data e hora da criação"
        assert properties["updated_at"]["description"] == "Data e hora da atualização"

    def test_combined_mixins_model_serialization(self):
        """Testa serialização de modelo com mixins combinados"""
        class TestModel(UuidMixinSchema, TimestampMixinSchema):
            name: str
        
        test_uuid = uuid4()
        now = datetime.now()
        
        # Act
        model = TestModel(
            id=test_uuid,
            name="Teste",
            created_at=now,
            updated_at=now
        )
        
        # Serializa para dict
        model_dict = model.model_dump()
        
        # Assert
        assert model_dict["id"] == test_uuid
        assert model_dict["name"] == "Teste"
        assert model_dict["created_at"] == now
        assert model_dict["updated_at"] == now

    def test_combined_mixins_model_deserialization(self):
        """Testa deserialização de modelo com mixins combinados"""
        class TestModel(UuidMixinSchema, TimestampMixinSchema):
            name: str
        
        test_uuid = uuid4()
        now = datetime.now()
        
        # Arrange
        data = {
            "id": str(test_uuid),
            "name": "Teste",
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        # Act
        model = TestModel(**data)
        
        # Assert
        assert model.id == test_uuid
        assert model.name == "Teste"
        assert model.created_at == now
        assert model.updated_at == now