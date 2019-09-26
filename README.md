# supaharris-client

**API client for the supaharris.com globular and star cluster database**

[![Software license](http://img.shields.io/badge/license-AGPL3-brightgreen.svg)](https://github.com/tlrh314/supaharris/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/tlrh314/supaharris-client.svg?branch=master)](https://travis-ci.org/tlrh314/supaharris-client)


# Usage with https://www.supaharris.com

```python
from supaharrisclient.models import SupaHarris

sh = SupaHarris()
sh.set_all_data()

sh.print_parameters()
sh.print_astro_object_classifications()
sh.print_astro_objects()

print("\nRetrieved {0} references".format(len(sh.references)))
print("\nReference 0\n  {0:<25s}{1}".format("Key", "Value"))
for k, v in sh.references[0].items():
    print("  {0:<25s}{1}".format(k, v))
```

# Usage with local development setup
```python

from supaharrisclient.models import SupaHarris

sh = SupaHarris(base_url="https://nginx/api/v1/", verify=False)

sh.set_parameter_list()
sh.print_parameters()
```
