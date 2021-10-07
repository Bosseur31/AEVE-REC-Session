#!/bin/bash


#Dossier de base
dir=/srv/aeve-rec-session/data/temp ;
dir_timestamp=/srv/aeve-rec-session/back/temp_var ;
filename="$dir_timestamp/timestamp.txt" ;

if [ ! -f $filename ]
then
    touch $filename
fi

#Récupération du dernier timestamp de transfer

timestamp_modif=$(cat "$filename") ;

if [ "$timestamp_modif" == '' ]
then
    echo "1577833200" > "$filename" ;
    timestamp_modif=$(cat "$filename") ;
fi

for video in $dir/*
do
   #Nom du fichier apres son répertoire
   destVideo=$(basename "$video");
   #Nom du répertoire
   srcVideo=$(dirname $video);

   #Récupération du timestamp de dérniere modif de la vidéo
   timestamp=$(stat -c '%Y' "$dir/$destVideo") ;

   if [ "$timestamp" -lt "$timestamp_modif" ] 
   then
      echo "Vidéo deja traité"
      break
   fi
  
   jour=$(date -d @"$(echo $timestamp)" +'%Y-%m-%d') ;
   mois=$(date -d @"$(echo $timestamp)" +'%m.%y') ;
   semaine=$(date --date=$jour +"%V") ;
   annee=$(date -d @"$(echo $timestamp)" +'%Y')
  
   #Debug
   echo "Timestamp de la derniére modification de la vidéo: "$timestamp
   echo "Timestamp du dernier transfer: "$timestamp_modif
   echo "Nom video : "$destVideo
   echo "$destVideo"|sed -e 's/ /%20/g'
   echo "Chemin complet : "$video
   echo "La semaine : "$semaine
   echo "Le mois annee : "$mois
   echo "L'année: "$annee
   
   #Chemin de la destination et debug
   destnext="https://cloud.aymeric-mai.fr/remote.php/dav/files/simon/Simon/Vidéos-Simon/$(echo "$annee")/Semaine-$semaine%20le%20$mois/$(echo "$destVideo"|sed -e 's/ /%20/g')"
   echo "Destination finale : "$destnext

   #Execution de la commande de transfert
   log=$(curl -u simon:tchaik01 -T "$video" "https://cloud.aymeric-mai.fr/remote.php/dav/files/simon/Simon/Vidéos-Simon/$(echo "$annee")/Semaine-$semaine%20le%20$mois/$(echo "$destVideo"|sed -e 's/ /%20/g')")
   echo $log

   #Ecriture du timestamp 
   timestamp_modif=$(date +%s) ;
   echo "$timestamp_modif" > "$filename" ;
done
