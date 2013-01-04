import gettext
import sys
import locale

def _(st):
  loc_dir = "locale/"

  try:
    #TODO get config-file lang
    trans = gettext.translation('en', loc_dir)
    __ = trans.ugettext
    trans.install()
    return __(st)
  except:
    #TODO: Log exception
    return st
