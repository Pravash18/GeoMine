"""Configuration for GeoMine."""
import os


class Config:
    DATABASE = os.getenv("GEOMINE_DATABASE", os.path.join(os.getcwd(), "geomine.sqlite3"))
    TESTING = False
    JSON_SORT_KEYS = False
