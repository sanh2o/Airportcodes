import os
import requests

from dataflows import Flow, load, add_computed_field, delete_fields
from dataflows import validate, update_resource, add_metadata, dump_to_path

def readme(fpath='README.md'):
    if os.path.exists(fpath):
        return open(fpath).read()


dialing_info_cldr = Flow(
    load('archive/data.csv', name='airport-codes'),
    add_metadata(
        name= "airport-codes",
        title= "Airport Codes",
        description = """Data contains the list of all airport codes,
the attributes are listed in the table schema. Some of the columns
contain attributes identifying airport locations,
other codes (IATA, local if exist) that are relevant to
identification of an airport.""",
        version= "0.2.0",
        has_premium= True,
        collection= "reference-data",
        has_solutions= ["global-country-region-reference-data"],
        homepage= "http://www.ourairports.com/",
        licenses=[
            {
              "id": "odc-pddl",
              "path": "http://opendatacommons.org/licenses/pddl/",
              "title": "Open Data Commons Public Domain Dedication and License v1.0",
              'name': "open_data_commons_public_domain_dedication_and_license_v1.0"
            }
        ],
        sources= [
            {
              "name": "Our Airports",
              "path": "http://ourairports.com/data/",
              "title": "Our Airports"
            }
        ],
        readme=readme()
    ),
    add_computed_field([{
        "operation": "format",
        "target": "coordinates",
        "with": "{latitude_deg}, {longitude_deg}"
    }]),
    delete_fields(fields=[
        "id","longitude_deg","latitude_deg",
        "scheduled_service","home_link","wikipedia_link","keywords"
    ]),
    update_resource('airport-codes', **{'path':'data/airport-codes.csv'}),
    validate(),
    dump_to_path()
)


def flow(parameters, datapackage, resources, stats):
    return dialing_info_cldr


if __name__ == '__main__':
    dialing_info_cldr.process()
