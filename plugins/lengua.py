import gettext
import sys
import locale

def _(st):
  loc_dir = "locale/"

  try:
    #TODO obtener lenguaje de archivo de configuracion
    trans = gettext.translation('en', loc_dir)
    __ = trans.ugettext
    trans.install()
    return __(st)
  except:
    raise


