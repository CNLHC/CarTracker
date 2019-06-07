
import sys,os
sys.path.append('/home/curry/Project/grossular/grossular-sphinx')

sys.path.append(os.path.abspath("../../openmv"))
sys.path.append('.')
sys.path.append('..')
sys.path.append('../..')

project = '小车追踪DEMO'
copyright = '2019, CNLHC'
author = 'CNLHC'
version = ''
release = '0.0'
extensions = [
    'sphinx.ext.autodoc',
    'grossularsphinx.usecase',
    'sphinx.ext.todo',
    'sphinxcontrib.plantuml',
    'sphinx.ext.graphviz',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
]
class_members_toctree = False
grossular_server = "http://ali.cnworkshop.xyz:3000"
grossular_project= "cartracker"
plantuml_output_format = "svg"
# templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'zh_CN'
exclude_patterns = []
pygments_style = None
html_theme = 'alabaster'
html_static_path = ['_static']
latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    'fncychap': '',
    'figure_align': 'H',
    'extraclassoptions': 'openany,oneside',
    'maketitle': r'''\shattuckitemaketitle
\newpage
    ''',
    'releasename': "版本",
    'fontpkg': r'''
''',
    "preamble":open('./texPre.latex','r').read()
}
latex_documents = [
    (master_doc, 'DEMO.tex', '小车追踪DEMO 文档',
     'CNLHC', 'manual'),
]
html_theme = "sphinx_rtd_theme"
plantuml_latex_output_format = "pdf"
autodoc_default_options = {
    'undoc-members': True,
    'exclude-members': 'sensor,pyb'
}

autodoc_mock_imports = ["sensor","pyb","image","usocket","network","ustruct","ubinascii","openmv.main"]