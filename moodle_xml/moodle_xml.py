"""moodle_xml és una extensió d'sphinx que implementa el
:term:`domain` `moodle` i el :term:`builder` `moodle` que genera el
format Moodle XML

"""

import functools


from docutils import nodes
from docutils.parsers.rst import directives, states


from sphinx.builders.html import SingleFileHTMLBuilder
from sphinx.builders import Builder
from sphinx.domains import Domain, ObjType, Index
from sphinx.locale import l_, _
from sphinx.roles import XRefRole
from sphinx.util.compat import Directive


formatMake = "html"
#
# Nodes del doctree
#

class Question(nodes.General, nodes.Element):
    """Question doctree node"""
    pass

class Name(nodes.General, nodes.Element):
    """Name doctree node"""
    pass

class QAText(nodes.General, nodes.Element):
    """QAText doctree node"""
    pass

class QuestionText(nodes.General, nodes.Element):
    """QuestionText doctree node"""
    pass

class Answer(nodes.General, nodes.Element):
    """Answer doctree node"""
    pass

class Feedback(nodes.General, nodes.Element):
    """Feedback doctree node"""
    pass


#
# Visitor methods
#

def findSections(node):
    totalSection = 0
    while node.tagname != 'document':
        node = node.parent
        if node.tagname == 'section':
            totalSection += 1
    return totalSection+1

def html_visitors(name, formatMake):
    def visit(self, node):
        if formatMake == 'html':
            if node.parent.tagname == 'Name':
                self.body.append('<h' + str(findSections(node)) +'>')
            if node.tagname == 'Feedback' and node.parent.tagname == 'Question':
                if node.parent.get('realimentacio'):
                    self.body.append('<table><tr><th>Retroacció Global:</th><td>')
                else:
                    self.body.append('<!--')
        elif formatMake == 'moodle':
            print(name)
            d = { k: node.attributes[k] for k in node.attributes if node.attributes[k] != [] }
            d.pop('single', None)
            self.body.append(self.starttag(node, '{}'.format(name), **d))

    def depart(self, node):
        if formatMake == 'html':
            if node.tagname == 'Feedback' and node.parent.tagname == 'Question':
                if node.parent.get('realimentacio'):
                    self.body.append('</td></tr></table><br><ol>')
                else:
                    self.body.append('--><ol>')
            # if name == 'questiontext':
                # self.body.append('')
            if node.parent.tagname == 'Name':
                self.body.append('</h' + str(findSections(node)) +'>')
            if node.tagname == 'Answer':
                if node.get('realimentacio'):
                    self.body.append('</td></tr></table></li><br>')
                else:
                    self.body.append('-->')
        elif formatMake == 'moodle':
            self.body.append('</{}>\n'.format(name))

    return visit, depart

def text_visitors(name, formatMake):
    v, d = html_visitors(name, formatMake)

    def visit(self, node):
        v(self, node)
        if formatMake == 'html':
            if node.parent.tagname == 'Answer':
                self.body.append('<li>')
        elif formatMake == 'moodle':
            print(name)
            d = { k: node.attributes[k] for k in node.attributes if node.attributes[k] != [] }
            d.pop('single', None)
            self.body.append(self.starttag(node, '{}'.format(name), **d))

    def depart(self, node):
        # print(node.parent.tagname)
        if formatMake == 'html':
            if node.parent.tagname == 'Answer':
                if node.parent.get('realimentacio'):
                    self.body.append('<table><tr><th>Puntuació:</th>' +
                            '<td>' + str(node.parent.get('fraction')) + '%</td></tr>' +
                            '<tr><th>Retroacció:</th><td>')
                else:
                    self.body.append('<!--')
        elif formatMake == 'moodle':
            self.body.append('</{}>\n'.format(name))
        d(self, node)

    return visit, depart

def question_visitors(name, formatMake):
    visit, d = html_visitors(name, formatMake)

    def depart(self, node):
        if formatMake == 'html':
            # if node.tagname == 'Feedback' and node.parent.tagname == 'Question':
            # print(node.child.tagname)
            # print(node.tagname)
            self.body.append('</ol>')
        d(self, node)

    return visit, depart

# def moodle_visitors(name):
    # def visit(self, node):
        # d = { k: node.attributes[k] for k in node.attributes if node.attributes[k] != [] }
        # d.pop('single', None)
        # self.body.append(self.starttag(node, '{}'.format(name), **d))
    # def depart(self, node):
        # self.body.append('</{}>\n'.format(name))
    # return visit, depart


#
# Directives
#

def opt_type(argument):
    """Conversion function for the "type" option."""
    return directives.choice(argument, ('multichoice', 'truefalse'))

class MoodleQuestion(Directive):
    """:rst:dir:`Question directive <moodle:question>`.

    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'type': opt_type,
        'feedback': directives.unchanged,
        'single': directives.flag,
    }
    has_content = True

    def run(self):
        env = self.state.document.settings.env  # sphinx.environment.BuildEnvironment
        config = env.config                     # sphinx.config.Config
        if 'realimentacio' in config:
            realimentacio = config['realimentacio']
        else:
            realimentacio = False


        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        # Creem un node question, que acabarà de farcir la crida a
        # `nested_parse`.
        question_node = Question()
        question_node['type'] = self.options['type']
        question_node['single'] = 'single' in self.options
        question_node['realimentacio'] = realimentacio
        # Extraiem el títol i l'afegim a un node name
        title_text = self.arguments[0].strip()
        text_nodes, messages = self.state.inline_text(title_text,
                                                      self.lineno)
        name_node = Name()
        text_node = QAText()
        text_node += text_nodes + messages
        name_node += text_node
        # Afegim el node name al node question
        question_node += name_node
        # Parse the directive contents.
        question_text_node = QuestionText()
        # question_text_node['format'] = 'html'
        textqt_node = QAText()
        self.state.nested_parse(self.content, self.content_offset,
                                textqt_node)
        question_text_node += textqt_node
        question_node += question_text_node
        if 'feedback' in self.options:
            feedback_node = Feedback()
            # feedback_node['format'] = 'html'
            feedback_node['fraction'] = self.arguments[0].strip()
            textf_node = QAText()
            text_nodes, messages = self.state.inline_text(self.options['feedback'], self.lineno)
            textf_node += text_nodes + messages
            feedback_node += textf_node
            question_node += feedback_node
        return [question_node]


class MoodleAnswer(Directive):
    """rst:dir:`Answer directive <moodle:question>`"""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'feedback': directives.unchanged,
    }
    has_content = True

    def run(self):
        env = self.state.document.settings.env  # sphinx.environment.BuildEnvironment
        config = env.config                     # sphinx.config.Config
        if 'realimentacio' in config:
            realimentacio = config['realimentacio']
        else:
            realimentacio = False

        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)
        # Creem un node answer
        answer_node = Answer()
        answer_node['fraction'] = self.arguments[0].strip()
        # answer_node['format'] = 'html'
        answer_node['realimentacio'] = realimentacio
        # Creem un node feedback
        # Parse the directive contents.
        texta_node = QAText()
        self.state.nested_parse(self.content, self.content_offset,
                                texta_node)
        answer_node += texta_node
        if 'feedback' in self.options:
            feedback_node = Feedback()
            # feedback_node['format'] = 'html'
            feedback_node['fraction'] = self.arguments[0].strip()
            textf_node = QAText()
            text_nodes, messages = self.state.inline_text(self.options['feedback'], self.lineno)
            textf_node += text_nodes + messages
            feedback_node += textf_node
            answer_node += feedback_node
        return [answer_node]


#
# Dominis
#

class MoodleDomain(Domain):
    """Moodle XML language domain."""
    name = 'moodle'
    label = 'Moodle XML'
    object_types = {
        'question':  ObjType(l_('question'),  'quest'),
    }

    directives = {
        'question': MoodleQuestion,
        'answer':   MoodleAnswer,
    }
    roles = {
        'quest':   XRefRole(),
    }
    initial_data = {
        'questions': {},     # questname -> docname, questtype
    }
    indices = [
        # MoodleQuestionIndex,
    ]

    def clear_doc(self, docname):
        for questname, (fn, _) in self.data['questions'].items():
            if fn == docname:
                del self.data['questions'][questname]

    def get_objects(self):
        for questname, (docname, questtype) in self.data['questions'].items():
            yield (questname, questname, questtype, docname, questname, 1)


#
# Builders
#

class MoodleBuilder(SingleFileHTMLBuilder):
    """This builder produces Moodle XML format"""

    name = 'moodle'
    format = 'moodle'
    out_suffix = '.xml'


#
# doctree-read handler
#

def doctree_read_handler(app, doctree):
    for node in doctree.traverse(Answer):
        node.parent.remove(node)
        node.parent.parent.parent += node

#
# Inicialització
#

def setup(app):
    app.add_config_value('realimentacio', False, True)

    app.add_builder(MoodleBuilder)
    app.add_domain(MoodleDomain)

    # global formatMake
    # formatMake= app.buildername

    app.add_node(Question, html=question_visitors('question', app.buildername))
    app.add_node(Name, html=html_visitors('name', app.buildername))
    app.add_node(QAText, html=text_visitors('text', app.buildername))
    app.add_node(QuestionText, html=html_visitors('questiontext', app.buildername))
    app.add_node(Answer, html=html_visitors('answer', app.buildername))
    app.add_node(Feedback, html=html_visitors('feedback', app.buildername))

    # app.add_node(Question, moodle=moodle_visitors('question'))
    # app.add_node(Name, moodle=moodle_visitors('name'))
    # # app.add_node(QAText, moodle=moodle_visitors('text'))
    # app.add_node(QuestionText, moodle=moodle_visitors('questiontext'))
    # app.add_node(Answer, moodle=moodle_visitors('answer'))
    # app.add_node(Feedback, moodle=moodle_visitors('feedback'))

    app.connect('doctree-read', doctree_read_handler)
