#!/usr/bin/env python
from heat.common.template_format import convert_json_to_yaml

json = """
{
"AWSTemplateFormatVersion": "2010-09-09",
"Description": "MonboDB Config Server",
"Mappings": {
    "AWSInstanceType2Arch" : {
      "m1.tiny"    : { "Arch" : "32" },
      "m1.small"    : { "Arch" : "64" },
      "m1.medium"    : { "Arch" : "64" },
      "m1.large"   : { "Arch" : "64" },
      "m1.xlarge"   : { "Arch" : "64" }
    },
    "DistroArch2AMI": {
      "F18"      : { "32" : "F18-i386-cfntools", "64" : "F18-x86_64-cfntools" },
      "F17"      : { "32" : "F17-i386-cfntools", "64" : "F17-x86_64-cfntools" },
      "U10"      : { "32" : "U10-i386-cfntools", "64" : "U10-x86_64-cfntools" },
      "RHEL-6.1" : { "32" : "rhel61-i386-cfntools", "64" : "rhel61-x86_64-cfntools" },
      "RHEL-6.2" : { "32" : "rhel62-i386-cfntools", "64" : "rhel62-x86_64-cfntools" },
      "RHEL-6.3" : { "32" : "rhel63-i386-cfntools", "64" : "rhel63-x86_64-cfntools" }
    }
  }
}
"""

yaml = convert_json_to_yaml(json)
print yaml
