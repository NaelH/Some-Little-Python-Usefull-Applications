#!/bin/bash

# csvhtml.sh
# Permet de transformer un fichier CSV en un code HTML
# Usage : ./csv2html.sh [OPTION] [FICHIER CSV]
#			-h : Aide
#			--help : Aide
#			-e : Export en un fichier html
#			--export : Export en un fichier html
#
# Auteur : https://github.com/NaelH
# Version : 1.0.0
#
# Dépendance : Aucune
#
# Limites : Aucune

# Variables importante pour les blindages
exp=0
# Fonctions
# Fonction de sortie en erreur
erreur() {
	echo >&2 "Erreur : $1"
	exit -1
}

# Fonction d'aide
aider() {
	echo "Usage correct : ./csv2html.sh [OPTIONS] [FICHIER CSV]"
	exit 0
}

# Blindage du script

# Vérification du nombre d'argument
[ $# -lt 1 -o $# -gt 3 ] && erreur "Merci de vous fier à notre aide."
[ $1 == "-h" -o $1 == "--help" ] && aider
[ $2 == "-e" -o $2 == "--export" ] && exp=1
[ ! -e $1 ] && erreur "Le fichier $1 n'existe pas."
[ ! -r $1 ] && erreur "Vous n'avez pas le droit de lecture sur $1"
[ ! -s $1 ] && erreur "Le fichier $1 est vide"

# Code 
FICHIER="$1"
NBLIGNE=$( wc -l < "$FICHIER" )
I=0
if [ $exp -eq 0 ]; then
echo "<!DOCTYPE html>"
echo "<html>"
echo "	<head>"
echo "	</head>"
echo "	<body>"
echo "		<table>"
	while [ $I -le $NBLIGNE ]; do
		echo "			<tr>"
		LIGNE=$( cat "$FICHIER" | head -n "$I" | tail -n 1 )
		ANCIENIFS=$IFS
		IFS=";"
		for WORD in $LIGNE; do
			echo "				<td>$WORD</td>"			
		done

		echo "			</tr>"
		(( I++ ))

	done

	echo "		</table>"
	echo "	</body>"
	echo "</html>"
fi

if [ $exp -eq 1 ]; then

	{
		echo "<!DOCTYPE html>"
		echo "<html>"
		echo "	<head>"
		echo "	</head>"
		echo "	<body>"
		echo "		<table>"
		while [ $I -le $NBLIGNE ]; do
			echo "			<tr>"
			LIGNE=$( cat "$FICHIER" | head -n "$I" | tail -n 1 )
			ANCIENIFS=$IFS
			IFS=";"
			for WORD in $LIGNE; do
				echo "				<td>$WORD</td>"			
			done
		
			echo "			</tr>"
			(( I++ ))
		
		done
		
		echo "		</table>"
		echo "	</body>"
		echo "</html>"
	} > "${FICHIER}.html"

	echo "Le fichier $1 a bien été exporté sous le nom : ${1}.html"
fi
