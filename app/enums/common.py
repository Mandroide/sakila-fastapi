from enum import StrEnum


class Tags(StrEnum):
    countries = "countries"
    films = "films"
    customers = "customers"
    staff = "staff"
    languages = "languages"
    categories = "categories"
    actors = "actors"


class Prefix(StrEnum):
    countries = "/countries"
    films = "/films"
    customers = "/customers"
    staff = "/staff"
    languages = "/languages"
    categories = "/categories"
    actors = "/actors"
