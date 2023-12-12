from ninja import Schema
from typing import List


class DataYearSchema(Schema):
    year: int


class DataSourceSchema(Schema):
    title: str = None
    url: str = None
    year: DataYearSchema = None
    public_label: str = None


class RegionSchema(Schema):
    id: int
    name: str = None
    insee: str = None
    siren: str = None
    years: List[DataYearSchema]


class DepartementSchema(Schema):
    id: int
    name: str = None
    insee: str = None
    siren: str = None
    region: RegionSchema = None
    years: List[DataYearSchema] = None


class EpciSchema(Schema):
    id: int
    name: str = None
    siren: str = None
    years: List[DataYearSchema] = None


class CommuneSchema(Schema):
    id: int
    name: str = None
    insee: str = None
    siren: str = None
    epci: EpciSchema = None
    departement: DepartementSchema = None
    population: int = None
    years: List[DataYearSchema] = None


class RegionDataSchema(Schema):
    id: int
    year: DataYearSchema = None
    datacode: str = None
    value: str = None
    label: str = None
    datatype: str = None
    source: DataSourceSchema = None
    region: RegionSchema = None


class DepartementDataSchema(Schema):
    id: int
    year: DataYearSchema = None
    datacode: str = None
    value: str = None
    label: str = None
    datatype: str = None
    source: DataSourceSchema = None
    departement: DepartementSchema = None


class EpciDataSchema(Schema):
    id: int
    year: DataYearSchema = None
    datacode: str = None
    value: str = None
    label: str = None
    datatype: str = None
    source: DataSourceSchema = None
    epci: EpciSchema = None


class CommuneDataSchema(Schema):
    id: int
    year: DataYearSchema = None
    datacode: str = None
    value: str = None
    label: str = None
    datatype: str = None
    source: DataSourceSchema = None
    commune: CommuneSchema = None
