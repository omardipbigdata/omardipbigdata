import jsonref

schema = jsonref.loads('''{
  "$id": "https://example.com/nested-schema.json",
  "title": "nested-schema",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "required": [
    "EmploymentInformation",
    "EmployeePartyID",
    "Age"
  ],
  "properties": {
    "EmployeePartyID": {
      "type": "string",
      "minLength": 1,
      "maxLength": 3
    },
    "EmploymentInformation": {
      "$ref": "#/definitions/EmploymentInformation"
    },
    "Age": {
      "type": "integer",
      "minimum": 16,
      "maximum": 80
    }
  },
  "definitions": {
    "EmploymentInformation": {
      "type": "object",
      "required": [
        "OriginalHireDate"
      ],
      "properties": {
        "OriginalHireDate": {
          "type": "string",
          "format": "date"
        },
        "Beneficiary": {
          "$ref": "#/definitions/DependantInformation"
        }
      }
    },
    "DependantInformation": {
      "type": "object",
      "required": [
        "Name"
      ],
      "properties": {
        "Name": {
          "type": "string",
          "minLength": 5
        }
      }
    }
  },
  "description": "nested-schema"
}''')


def get_type_for_key_path(schema: dict, key_path: str) -> str:

    def nestedJson(schema: dict, key_path: str):
        nonlocal rtnValue
        d = "definitions"
        p = "properties"
        t = "type"
        s = '.'
        key = key_path.split(s)
        k = key[0]
        if len(key)>1:
            if d in schema:
                if k in schema[d]:
                    key.pop(0)
                    nestedJson(schema[d][k],s.join(key))
            elif p in schema:
                if k in schema[p] and len(key)>1:
                    key.pop(0)
                    nestedJson(schema[p][k], s.join(key))
                else :
                    rtnValue=schema[p][k][t]
        elif len(key)==1: rtnValue=schema[p][k][t]
        else: rtnValue=None

    rtnValue = None
    nestedJson(schema, key_path)
    return rtnValue


assert(get_type_for_key_path(schema, "Age") == "integer")
assert(get_type_for_key_path(schema, "EmploymentInformation.OriginalHireDate") == "string")
assert(get_type_for_key_path(schema, "EmploymentInformation.Beneficiary.Name") == "string")
assert(get_type_for_key_path(schema, "foo.bar") == None)