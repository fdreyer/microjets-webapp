from flask_wtf import Form
from wtforms import widgets, SelectMultipleField, BooleanField, SelectField

all_lines = set(['NLO','NLO_mult','NLO.LLR_mB','NNLO.LLR_multB','pseudo_NNLO','NNLO_mult','NLOPS','NLOPS_hw6'])

def rmbold(text):
    return '<div style=\'font-weight:normal\'>%s</div>' % (text)

class Params():
    lines = set()
    ymin = 0.0
    K = 1.0
    R = 0.2
    narrowband = False
    highpt = False

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget()
    # widget = widgets.ListWidget(prefix_label=False) #alternative format
    option_widget = widgets.CheckboxInput()

class PlotForm(Form):
    lines = [('NLO', rmbold('NLO')),
             ('NLO_mult', rmbold('NLO mult')),
             ('NLO.LLR_mB', rmbold('NLO + LL<sub>R</sub>')),
             ('pseudo_NNLO', rmbold('NNLO<sub>R</sub>')),
             ('NNLO_mult',rmbold('NNLO<sub>R</sub> mult.')),
             ('NNLO.LLR_multB', rmbold('NNLO<sub>R</sub> + LL<sub>R</sub>')),
             ('NLOPS', rmbold('POWHEG + Pythia 8&nbsp;')),
             ('NLOPS_hw6', rmbold('POWHEG + Herwig 6&nbsp;'))]
    choice_lines = MultiCheckboxField(choices = lines,
                                      default = ['NLO', 'NLO.LLR_mB','NNLO.LLR_multB'])
    # choice_lines = SelectMultipleField(choices = lines, default = ['NLO', 'NLO.LLR','NNLO.LLR'])

    # NLOline      = BooleanField('NLO',       default = True)
    # NLOmultline  = BooleanField('NLO_mult',  default = False)
    # NLOLLRline   = BooleanField('NLO.LLR',   default = True)
    # NLOPSline    = BooleanField('NLOPS',     default = False)
    # NLOPShw6line = BooleanField('NLOPS_hw6', default = False)
    # NNLOline     = BooleanField('NNLOR',     default = False)
    # NNLOmultline = BooleanField('NNLO_mult', default = False)
    # NNLOLLRline  = BooleanField('NNLO.LLR',  default = True)
    
    choice_R = SelectField('Item_Rval',
                           choices = [('0.03','R = 0.03'),
                                      ('0.05','R = 0.05'),
                                      ('0.1','R = 0.1'),
                                      ('0.2','R = 0.2'),
                                      ('0.4','R = 0.4'),
                                      ('0.6','R = 0.6'),
                                      ('1.0','R = 1.0')],
                           default = '0.2')
    
    choice_rap = SelectField('Item_rap',
                             choices = [('0.0','|y| < 0.5'),
                                        ('0.5','0.5 < |y| < 1.0'),
                                        ('1.0','1.0 < |y| < 1.5'),
                                        ('1.5','1.5 < |y| < 2.0'),
                                        ('2.0','2.0 < |y| < 2.5'),
                                        ('2.5','2.5 < |y| < 3.0')],
                             default = '0.0')
    
    choice_scalevar = SelectField('Item_scalevar',
                             choices = [('uncorrel','Uncorrelated'),
                                        ('correl'  ,'Correlated')],
                             default = 'fullpt')
    
    choice_ptbin = SelectField('Item_ptbin',
                             choices = [('fullpt','full pt range'),
                                        ('highpt','high pt bin'),],
                             default = 'fullpt')
    
    choice_K = SelectField('Item_Kval',
                           choices = [('1.00','K = 1.00'),
                                      ('1.05','K = 1.05'),
                                      ('1.10','K = 1.10'),
                                      ('1.15','K = 1.15')],
                           default = '1.00')
