"""Tests for the enum definitions mapping to MySQL ENUM columns."""

from enum import unique

import pytest
from sqlalchemy import Column, Enum as SAEnum, MetaData, String, Table

from ensembl_orm.enums import EnsemblObjectType, ExternalDbStatus, ExternalDbType, InfoType


class TestEnsemblObjectTypeMembers:
    """Verify EnsemblObjectType exposes the correct members and values."""

    def test_has_exactly_three_members(self):
        """EnsemblObjectType defines three members."""
        assert len(EnsemblObjectType) is 3

    def test_member_names(self):
        """Member names are GENE, TRANSCRIPT, TRANSLATION."""
        assert {m.name for m in EnsemblObjectType} == {"GENE", "TRANSCRIPT", "TRANSLATION"}

    def test_gene_value(self):
        """GENE maps to mixed-case 'Gene' matching the MySQL ENUM."""
        assert EnsemblObjectType.GENE.value == "Gene"

    def test_transcript_value(self):
        """TRANSCRIPT maps to mixed-case 'Transcript'."""
        assert EnsemblObjectType.TRANSCRIPT.value == "Transcript"

    def test_translation_value(self):
        """TRANSLATION maps to mixed-case 'Translation'."""
        assert EnsemblObjectType.TRANSLATION.value == "Translation"

    @pytest.mark.parametrize(
        "member",
        list(EnsemblObjectType),
        ids=[m.name for m in EnsemblObjectType],
    )
    def test_all_values_are_strings(self, member: EnsemblObjectType):
        """Every member's value is a str instance."""
        assert isinstance(member.value, str)


class TestExternalDbStatusMembers:
    """Verify ExternalDbStatus exposes the correct members and values."""

    def test_has_exactly_four_members(self):
        """ExternalDbStatus defines four members."""
        assert len(ExternalDbStatus) is 4

    def test_member_names(self):
        """Member names are KNOWN, XREF, DUMPED, DEPENDENT."""
        assert {m.name for m in ExternalDbStatus} == {"KNOWN", "XREF", "DUMPED", "DEPENDENT"}

    def test_known_value(self):
        assert ExternalDbStatus.KNOWN.value == "KNOWN"

    def test_xref_value(self):
        assert ExternalDbStatus.XREF.value == "XREF"

    def test_dumped_value(self):
        assert ExternalDbStatus.DUMPED.value == "DUMPED"

    def test_dependent_value(self):
        assert ExternalDbStatus.DEPENDENT.value == "DEPENDENT"

    @pytest.mark.parametrize(
        "member",
        list(ExternalDbStatus),
        ids=[m.name for m in ExternalDbStatus],
    )
    def test_all_values_are_strings(self, member: ExternalDbStatus):
        assert isinstance(member.value, str)


class TestInfoTypeMembers:
    """Verify InfoType exposes the correct members and values."""

    def test_has_exactly_eight_members(self):
        assert len(InfoType) is 8

    def test_member_names(self):
        expected = {"NONE", "PROBE", "DEPENDENT", "DIRECT", "INFERRED_PAIR", "PROBE2TRANSCRIPT", "UNMAPPED", "CHECKSUM"}
        assert {m.name for m in InfoType} == expected

    def test_none_value(self):
        assert InfoType.NONE.value == "NONE"

    def test_probe_value(self):
        assert InfoType.PROBE.value == "PROBE"

    def test_dependent_value(self):
        assert InfoType.DEPENDENT.value == "DEPENDENT"

    def test_direct_value(self):
        assert InfoType.DIRECT.value == "DIRECT"

    def test_inferred_pair_value(self):
        assert InfoType.INFERRED_PAIR.value == "INFERRED_PAIR"

    def test_probe2transcript_value(self):
        assert InfoType.PROBE2TRANSCRIPT.value == "PROBE2TRANSCRIPT"

    def test_unmapped_value(self):
        assert InfoType.UNMAPPED.value == "UNMAPPED"

    def test_checksum_value(self):
        assert InfoType.CHECKSUM.value == "CHECKSUM"

    @pytest.mark.parametrize(
        "member",
        list(InfoType),
        ids=[m.name for m in InfoType],
    )
    def test_all_values_are_strings(self, member: InfoType):
        assert isinstance(member.value, str)


class TestExternalDbTypeMembers:
    """Verify ExternalDbType exposes the correct members and values."""

    def test_has_exactly_six_members(self):
        assert len(ExternalDbType) is 6

    def test_member_names(self):
        expected = {"PRIMARY", "SECONDARY", "MISC", "CHECKSUM", "DEPENDENT", "IMAGE_DEPICTION"}
        assert {m.name for m in ExternalDbType} == expected

    def test_primary_value(self):
        assert ExternalDbType.PRIMARY.value == "PRIMARY"

    def test_secondary_value(self):
        assert ExternalDbType.SECONDARY.value == "SECONDARY"

    def test_misc_value(self):
        assert ExternalDbType.MISC.value == "MISC"

    def test_checksum_value(self):
        assert ExternalDbType.CHECKSUM.value == "CHECKSUM"

    def test_dependent_value(self):
        assert ExternalDbType.DEPENDENT.value == "DEPENDENT"

    def test_image_depiction_value(self):
        assert ExternalDbType.IMAGE_DEPICTION.value == "IMAGE_DEPICTION"

    @pytest.mark.parametrize(
        "member",
        list(ExternalDbType),
        ids=[m.name for m in ExternalDbType],
    )
    def test_all_values_are_strings(self, member: ExternalDbType):
        assert isinstance(member.value, str)


class TestStringComparisonEquality:
    """Verify enum members compare equal to their string values (critical for SQLAlchemy queries)."""

    @pytest.mark.parametrize(
        "member",
        list(EnsemblObjectType),
        ids=[m.name for m in EnsemblObjectType],
    )
    def test_ensembl_object_type_equals_string(self, member: EnsemblObjectType):
        assert member == member.value

    @pytest.mark.parametrize(
        "member",
        list(ExternalDbStatus),
        ids=[m.name for m in ExternalDbStatus],
    )
    def test_external_db_status_equals_string(self, member: ExternalDbStatus):
        assert member == member.value

    @pytest.mark.parametrize(
        "member",
        list(InfoType),
        ids=[m.name for m in InfoType],
    )
    def test_info_type_equals_string(self, member: InfoType):
        assert member == member.value

    @pytest.mark.parametrize(
        "member",
        list(ExternalDbType),
        ids=[m.name for m in ExternalDbType],
    )
    def test_external_db_type_equals_string(self, member: ExternalDbType):
        assert member == member.value


class TestConstructionFromValidStrings:
    """Verify enums can be constructed from their string values."""

    def test_ensembl_object_type_from_string(self):
        assert EnsemblObjectType("Gene") is EnsemblObjectType.GENE
        assert EnsemblObjectType("Gene").value == "Gene"

    def test_external_db_status_from_string(self):
        assert ExternalDbStatus("KNOWN") is ExternalDbStatus.KNOWN
        assert ExternalDbStatus("KNOWN").value == "KNOWN"

    def test_info_type_from_string(self):
        assert InfoType("DIRECT") is InfoType.DIRECT
        assert InfoType("DIRECT").value == "DIRECT"

    def test_external_db_type_from_string(self):
        assert ExternalDbType("PRIMARY") is ExternalDbType.PRIMARY
        assert ExternalDbType("PRIMARY").value == "PRIMARY"


class TestInvalidValueHandling:
    """Verify ValueError is raised for invalid enum values."""

    @pytest.mark.parametrize(
        "enum_class",
        [EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType],
        ids=["EnsemblObjectType", "ExternalDbStatus", "InfoType", "ExternalDbType"],
    )
    def test_invalid_string_raises_value_error(self, enum_class: type):
        with pytest.raises(ValueError):
            enum_class("INVALID")

    def test_wrong_case_raises_value_error(self):
        with pytest.raises(ValueError):
            EnsemblObjectType("gene")

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            EnsemblObjectType("")


class TestIteration:
    """Verify enums support iteration and return all members."""

    def test_ensembl_object_type_iteration(self):
        members = list(EnsemblObjectType)
        assert len(members) is 3
        assert EnsemblObjectType.GENE in members

    def test_external_db_status_iteration(self):
        members = list(ExternalDbStatus)
        assert len(members) is 4
        assert ExternalDbStatus.KNOWN in members

    def test_info_type_iteration(self):
        members = list(InfoType)
        assert len(members) is 8
        assert InfoType.NONE in members

    def test_external_db_type_iteration(self):
        members = list(ExternalDbType)
        assert len(members) is 6
        assert ExternalDbType.PRIMARY in members


class TestUniqueEnforcement:
    """Verify @unique decorator prevents duplicate values within each enum."""

    @pytest.mark.parametrize(
        "enum_class",
        [EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType],
        ids=["EnsemblObjectType", "ExternalDbStatus", "InfoType", "ExternalDbType"],
    )
    def test_no_duplicate_values(self, enum_class: type):
        values = [m.value for m in enum_class]
        assert len(set(values)) == len(values)


class TestSQLAlchemyEnumIntegration:
    """Verify enums work with SQLAlchemy's Enum column type."""

    @pytest.mark.parametrize(
        "enum_class",
        [EnsemblObjectType, ExternalDbStatus, InfoType, ExternalDbType],
        ids=["EnsemblObjectType", "ExternalDbStatus", "InfoType", "ExternalDbType"],
    )
    def test_sa_enum_instantiates(self, enum_class: type):
        """sqlalchemy.Enum(EnumClass) can be instantiated without error."""
        sa_enum = SAEnum(enum_class)
        assert sa_enum is not None

    def test_column_definition_with_ensembl_object_type(self):
        """Enum can be used in a SQLAlchemy Column definition."""
        metadata = MetaData()
        table = Table(
            "test_table",
            metadata,
            Column("id", String(10), primary_key=True),
            Column("object_type", SAEnum(EnsemblObjectType)),
        )
        assert "object_type" in table.c
        assert isinstance(table.c.object_type.type, SAEnum)


class TestPublicApiReExport:
    """Verify enums are re-exported from the main ensembl_orm package."""

    def test_import_from_package_root(self):
        from ensembl_orm import EnsemblObjectType as RootEOT
        from ensembl_orm import ExternalDbStatus as RootEDS
        from ensembl_orm import InfoType as RootIT
        from ensembl_orm import ExternalDbType as RootEDT

        assert RootEOT is EnsemblObjectType
        assert RootEDS is ExternalDbStatus
        assert RootIT is InfoType
        assert RootEDT is ExternalDbType
