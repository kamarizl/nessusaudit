# nessusaudit
Convert nessus audit file python object.

sample nessus audit file (`file0.audit`):
```
  <custom_item>
   type         : REGISTRY_SETTING
   description  : "2.3.11.5 Configure 'Network Access: Named Pipes that can b.."
   info         : "Limiting named pipes that can be accessed anonymously will.."
   reference    : "LEVEL|1S"
   see_also     : "https://benchmarks.cisecurity.org/tools2/windows/CIS_Micro.."
   solution     : "To establish the recommended configuration via GP, set the.."
Impact: This configuration will disable null session access over named pipes,.."
   value_type   : POLICY_MULTI_TEXT
   reg_key      : "HKLM\System\CurrentControlSet\Services\LanManServer\Paramet.."
   reg_item     : "NullSessionPipes"
   value_data   : "@ANON_NAMED_PIPES@"
  </custom_item>

  <custom_item>
   type         : REGISTRY_SETTING
   description  : "2.3.11.6 Set 'Network access: Remotely accessible registr..."
   info         : "The registry is a database that contains computer configu..."
   reference    : "LEVEL|1S"
   see_also     : "https://benchmarks.cisecurity.org/tools2/windows/CIS_Micr..."
   solution     : "To implement the recommended configuration state, set the..."
Impact: Remote management tools such as the Microsoft Baseline Security Anal..."
   value_type   : POLICY_MULTI_TEXT
   reg_key      : "HKLM\System\CurrentControlSet\Control\SecurePipeServers\W..."
   reg_item     : "Machine"
   value_data   : "System\CurrentControlSet\Control\ProductOptions" && "Syst..."
  </custom_item>
```

Usage:
```python

import json
import NessusAudit

auditFile = NessusAudit("file0.audit")
data = auditFile.array()

for _dict in data:
  print json.dumps(_dict, indent=4)

```

Result:
```
{
    "info": "Limiting named pipes that can be accessed anonymously will..", 
    "reg_item": "NullSessionPipes", 
    "value_data": "@ANON_NAMED_PIPES@", 
    "description": "Configure 'Network Access: Named Pipes that can b..", 
    "reference": "LEVEL|1S", 
    "type": "REGISTRY_SETTING", 
    "solution": "To establish the recommended configuration via GP, set the..", 
    "value_type": "POLICY_MULTI_TEXT", 
    "see_also": "https://benchmarks.cisecurity.org/tools2/windows/CIS_Micro..", 
    "ref": "2.3.11.5", 
    "reg_key": "HKLM\\System\\CurrentControlSet\\Services\\LanManServer\\Paramet.."
}
{
    "info": "The registry is a database that contains computer configu...", 
    "reg_item": "Machine", 
    "value_data": "System\\CurrentControlSet\\Control\\ProductOptions\" && \"Syst...", 
    "description": "Set 'Network access: Remotely accessible registr...", 
    "reference": "LEVEL|1S", 
    "type": "REGISTRY_SETTING", 
    "solution": "To implement the recommended configuration state, set the...", 
    "value_type": "POLICY_MULTI_TEXT", 
    "see_also": "https://benchmarks.cisecurity.org/tools2/windows/CIS_Micr...", 
    "ref": "2.3.11.6", 
    "reg_key": "HKLM\\System\\CurrentControlSet\\Control\\SecurePipeServers\\W..."
}

```
