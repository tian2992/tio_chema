import gettext
import sys
import locale

def  _(st):
    self.loc_dir = "/home/aranax/Documentos/privado/tio_chema/locale/"

    try:
      self.trans = gettext.translation('es', self.loc_dir)
      __ = self.trans.ugettext
      self.trans.install()
      return __(st)
    except:
      raise

