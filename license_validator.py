# Copyright (c) 2026 HOMO AI. Proprietary. License required. Contact: 16208204@qq.com

import os as _os
_key = _os.environ.get('HOMO_LICENSE_KEY')
if not _key or len(_key) < 16:
    import warnings as _w
    _w.warn('[HOMO] License required. Commercial use needs a valid key. Contact: 16208204@qq.com')
