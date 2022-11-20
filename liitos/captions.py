#!/usr/bin/env python3
# sucht innerhalb von longtable's nach
# \caption{...}\tabularnewline und verschiebt
# diesen Text an das Tabellenende

import sys

modus = 'copy'
for line in sys.stdin:
    if modus == 'copy':
        if line.startswith(r'\begin{longtable}'):
            # eine neue Tabelle startet, Text zwischenspeichern
            modus = 'table'
            table = line
            caption = ''
        else:
            # im Copy-Modus Zeile einfach wieder ausgeben
            sys.stdout.write(line)

    elif modus == 'table':
        if line.startswith(r'\caption{'):
            # Beginn der Überschrift gefunden, zwischenspeichern
            caption = line
            if not caption.strip().endswith(r'}\tabularnewline'):
                # Überschrift geht noch weiter
                modus = 'caption'
        elif line.startswith(r'\end{longtable}'):
            # Ende der Tabelle gefunden
            sys.stdout.write(table)
            sys.stdout.write(r'\rowcolor{white}')
            sys.stdout.write(caption)
            sys.stdout.write(line)
            modus = 'copy'
        else:
            # Tabelle geht weiter
            table += line

    elif modus == 'caption':
        caption += line
        if line.strip().endswith(r'}\tabularnewline'):
            # Überschrift ist fertig
            modus = 'table'
