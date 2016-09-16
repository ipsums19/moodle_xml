Introducció
===========


Motivació
---------

Resulta pràctic usar sphinx_ per tota la documentació relacionada amb
una assignatura: material pels alumnes, material de coordinació per
als professors, exàmens... També seria pràctic poder usar sphinx_ per
escriure les preguntes dels exàmens tipus test de moodle_.

.. _sphinx: http://www.sphinx-doc.org/
.. _moodle: https://moodle.org/


Objectiu
--------

Desenvolupar l'extensió d'sphinx_ :py:mod:`moodle_xml` que

#. incorpori noves directives ReST_ per escriure tests i preguntes de test, i

#. afegeixi el builder_ `moodle` que ha de generar les preguntes de
   test en format `Moodle XML`_.

.. _ReST: http://docutils.sourceforge.net/rst.html
.. _builder: http://www.sphinx-doc.org/en/stable/builders.html
.. _Moodle XML: https://docs.moodle.org/en/Moodle_XML_format


Requisits
---------

- Cal programar en python3_.

- Cal documentar en sphinx_.

- Usarem mercurial_ con a sistema de control de versions i treballarem
  amb el gestor de dipòsits allotjat a http://jocs.cs.upc.edu:5000.
  
- Produïm `programari lliure`_ amb llicència `GNU GPLv3`_.

- Tot el programari usat en el desenvolupament ha de ser lliure.
  
.. _python3: https://docs.python.org/3/
.. _sphinx: http://www.sphinx-doc.org/
.. _programari lliure: http://www.gnu.org/philosophy/free-sw.ca.html
.. _GNU GPLv3: http://www.gnu.org/licenses/quick-guide-gplv3.ca.html
.. _mercurial: https://www.mercurial-scm.org/
