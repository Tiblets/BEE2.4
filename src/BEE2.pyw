import utils
LOGGER = utils.init_logging('../BEE2-error.log')

from tkinter import messagebox

from multiprocessing import freeze_support
import traceback
import logging

# BEE2_config creates this config file to allow easy cross-module access
from BEE2_config import GEN_OPTS

from tk_tools import TK_ROOT
import UI
import loadScreen
import paletteLoader
import packageLoader
import gameMan
import extract_packages

DEFAULT_SETTINGS = {
    'Directories': {
        'palette': 'palettes/',
        'package': 'packages/',
    },
    'General': {
        'preserve_BEE2_resource_dir': '0',
        'allow_any_folder_as_game': '0',
        'mute_sounds': '0',
        'show_wip_items': '0',
    },
    'Debug': {
        # Show exceptions in dialog box when crash occurs
        'show_errors': '0',
        # Log whenever items fallback to the parent style
        'log_item_fallbacks': '0',
        # Print message for items that have no match for a style
        'log_missing_styles': '0',
        # Print message for items that are missing ent_count values
        'log_missing_ent_count': '0',
        # Warn if a file is missing that a packfile refers to
        'log_incorrect_packfile': '0',
    },
}

if __name__ == '__main__':
    freeze_support()  # Make multiprocessing work correctly when frozen

    if utils.MAC or utils.LINUX:
        import os
        import sys
        # Change directory to the location of the executable
        # Otherwise we can't find our files!
        # The Windows executable does this automatically.
        os.chdir(os.path.dirname(sys.argv[0]))

    loadScreen.main_loader.set_length('UI', 14)
    loadScreen.main_loader.show()

    # OS X starts behind other windows, fix that.
    if utils.MAC:
        TK_ROOT.lift()

    GEN_OPTS.load()
    GEN_OPTS.set_defaults(DEFAULT_SETTINGS)

    show_errors = False

    # Main application - intercept and log all errors
    try:
        UI.load_settings()

        show_errors = GEN_OPTS.get_bool('Debug', 'show_errors')

        gameMan.load()
        gameMan.set_game_by_name(
            GEN_OPTS.get_val('Last_Selected', 'Game', ''),
            )

        LOGGER.info('Loading Packages...')
        pack_data = packageLoader.load_packages(
            GEN_OPTS['Directories']['package'],
            log_item_fallbacks=GEN_OPTS.get_bool(
                'Debug', 'log_item_fallbacks'),
            log_missing_styles=GEN_OPTS.get_bool(
                'Debug', 'log_missing_styles'),
            log_missing_ent_count=GEN_OPTS.get_bool(
                'Debug', 'log_missing_ent_count'),
            log_incorrect_packfile=GEN_OPTS.get_bool(
                'Debug', 'log_incorrect_packfile'),
        )
        UI.load_packages(pack_data)
        LOGGER.info('Done!')

        LOGGER.info('Loading Palettes...')
        UI.load_palette(
            paletteLoader.load_palettes(GEN_OPTS['Directories']['palette']),
            )
        LOGGER.info('Done!')

        LOGGER.info('Loading Item Translations...')
        gameMan.init_trans()
        LOGGER.info('Done')

        LOGGER.info('Initialising UI...')
        UI.init_windows()  # create all windows
        LOGGER.info('Done!')

        loadScreen.main_loader.destroy()

        if GEN_OPTS.get_bool('General', 'preserve_BEE2_resource_dir'):
            extract_packages.done_callback()
        else:
            extract_packages.start_copying(pack_data['zips'])

        TK_ROOT.mainloop()

    except Exception as e:
        # If the loading screen is visible, destroy it so the error can be seen.
        loadScreen.main_loader.destroy()

        err = traceback.format_exc()
        if show_errors:
            # Put it onscreen if desired.
            messagebox.showinfo(
                title='BEE2 Error!',
                message=str(e).strip('".') + '!',
                icon=messagebox.ERROR,
                )

        # Log the error.
        LOGGER.exception('Exception Occurred:')
        logging.shutdown()

        # We still want to crash!
        raise
