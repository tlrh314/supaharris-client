# supaharris-client

**API client for the supaharris.com globular and star cluster database**

[![Software license](http://img.shields.io/badge/license-AGPL3-brightgreen.svg)](https://github.com/tlrh314/supaharris/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/tlrh314/supaharris-client.svg?branch=master)](https://travis-ci.org/tlrh314/supaharris-client)


# Usage

```python
from supaharrisclient.models import SupaHarris

sh = SupaHarris()
sh.set_reference_list()

print("\nRetrieved {0} references".format(len(sh.references)))
print("Reference: {0}".format(sh.references[0]))
```
