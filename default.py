import sys
from resources.lib.core.initialization import initialize_addon
from resources.lib.core.router import router

addon_handle, my_addon, params, action, traK, TRAKTLOGIN, webC, tmdb, sqlDB = initialize_addon()
router(action, params, traK, TRAKTLOGIN, webC, my_addon, addon_handle, tmdb, sqlDB)
