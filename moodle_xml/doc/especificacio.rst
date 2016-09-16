Especificació
=============

Directives ReST
---------------

El fitxer :download:`../exemples/e1.rst` conté un exemple de document
`sphinx` amb noves directives per escriure preguntes de test per a
`Moodle`.

.. rst:directive:: .. moodle:question:: title

   Text de la pregunta de `Moodle` amb nom *title*.

   Opcions:

   .. rst:role:: type

      Tipus de pregunta. Pot valdre `multichoice`, `truefalse`,
      `shortanswer`, `matching`, `cloze`, `essay`, `numerical`,
      `description`. Vegeu el format `Moodle XML`_.

   .. rst:role:: single

      Indica que la pregunta té resposta única.

   La directiva :rst:dir:`moodle:question` ha de contenir una o més
   directives :rst:dir:`moodle:answer`.

.. rst:directive:: .. moodle:answer:: perc

   Text de la resposta. El tant per cent de puntuació de la resposta
   és l'argument *perc*. *perc* pot ser positiu, negatiu o zero.

   Opcions:

   .. rst:role:: feedback

      Retroacció associada a la resposta.


.. py:module:: moodle_xml

Mòdul :py:mod:`moodle_xml`
--------------------------

El mòdul :py:mod:`moodle_xml` proporciona el :term:`domain` `moodle`
on es defineixen les directives :rst:dir:`moodle:question` i
:rst:dir:`moodle:answer`.

.. autoclass:: MoodleDomain
   :noindex:

El mòdul :py:mod:`moodle_xml` també proporciona un :term:`builder` per
generar el format `Moodle XML`_.

.. autoclass:: MoodleBuilder
   :noindex:


.. _Moodle XML: https://docs.moodle.org/en/Moodle_XML_format
